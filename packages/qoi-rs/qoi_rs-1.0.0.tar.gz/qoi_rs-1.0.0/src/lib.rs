use pyo3::prelude::*;

#[derive(FromPyObject)]
enum Data {
    Channel4(Vec<(u8, u8, u8, u8)>),
    Channel3(Vec<(u8, u8, u8)>),
    Bytes(Vec<u8>),
}

impl From<Data> for Box<[u8]> {
    fn from(data: Data) -> Self {
        match data {
            Data::Channel4(items) => {
                if items.iter().all(|pixel| pixel.3 == 0) {
                    items
                        .into_iter()
                        .flat_map(|(a, b, c, _)| [a, b, c])
                        .collect()
                } else {
                    items
                        .into_iter()
                        .flat_map(|(a, b, c, d)| [a, b, c, d])
                        .collect()
                }
            }
            Data::Channel3(items) => items.into_iter().flat_map(|(a, b, c)| [a, b, c]).collect(),
            Data::Bytes(items) => items.into_boxed_slice(),
        }
    }
}

#[pymodule]
mod _qoi {
    use std::borrow::Cow;

    use pyo3::exceptions::{PyAssertionError, PyValueError};
    use pyo3::{PyErr, PyResult, pyclass, pyfunction, pymethods};
    use qoi::{Channels, ColorSpace, Decoder, Encoder};

    use crate::Data;

    #[inline]
    fn to_py_error(error: qoi::Error) -> PyErr {
        use qoi::Error::*;
        match &error {
            InvalidChannels { .. }
            | InvalidColorSpace { .. }
            | InvalidImageDimensions { .. }
            | InvalidImageLength { .. }
            | InvalidMagic { .. }
            | InvalidPadding
            | UnexpectedBufferEnd => PyValueError::new_err(format!("{error:?}")),
            OutputBufferTooSmall { .. } | IoError(_) => {
                PyAssertionError::new_err(format!("{error:?}"))
            }
        }
    }

    #[pyfunction]
    #[pyo3(signature = (data, /, *, width, height))]
    fn encode(data: Data, width: u32, height: u32) -> PyResult<Cow<[u8], 'static>> {
        let data: Box<[u8]> = data.into();

        let encoder = Encoder::new(&data, width, height).map_err(to_py_error)?;

        encoder.encode_to_vec().map(Into::into).map_err(to_py_error)
    }

    #[pyclass(eq)]
    #[derive(PartialEq)]
    struct Image {
        #[pyo3(get)]
        width: u32,
        #[pyo3(get)]
        height: u32,
        #[pyo3(get)]
        data: Cow<[u8], 'static>,
        channels: Channels,
        colorspace: ColorSpace,
    }

    #[pymethods]
    impl Image {
        #[getter]
        fn mode(&self) -> &'static str {
            match self.channels {
                Channels::Rgb => "RGB",
                Channels::Rgba => "RGBA",
            }
        }

        #[getter]
        fn channels(&self) -> u8 {
            self.channels.as_u8()
        }

        #[getter]
        fn color_space(&self) -> &'static str {
            match self.colorspace {
                ColorSpace::Srgb => "SRGB",
                ColorSpace::Linear => "linear",
            }
        }

        fn __repr__(&self) -> PyResult<String> {
            let mode = self.mode();
            let Self { width, height, .. } = self;
            let color_space = self.color_space();
            let id = self as *const Self;
            Ok(format!(
                "<qoi_rs._qoi.Image color_space={color_space} mode={mode} size={width}x{height} at {id:?}>"
            ))
        }
    }

    #[pyfunction]
    #[pyo3(signature = (data, /))]
    fn decode(data: Cow<[u8], '_>) -> PyResult<Image> {
        let mut decoder = Decoder::new(&data).map_err(to_py_error)?;

        let header = decoder.header();

        Ok(Image {
            width: header.width,
            height: header.height,
            channels: header.channels,
            colorspace: header.colorspace,
            data: decoder.decode_to_vec().map_err(to_py_error)?.into(),
        })
    }
}
