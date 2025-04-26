#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "qoi-rs",
#   "pillow",
# ]
# [tool.uv.sources]
# qoi-rs = { path = "." }
# ///

from pathlib import Path

import qoi_rs

from PIL import Image

IMAGES_DIR = Path(__file__).absolute().parent / "qoi_test_images"

for file in ("dice", "testcard"):
    qoi_image_path = IMAGES_DIR / f"{file}.qoi"
    png_image_path = IMAGES_DIR / f"{file}.png"

    image = qoi_rs.decode(qoi_image_path.read_bytes())
    assert isinstance(image, qoi_rs.types.Image)
    png_image = Image.open(png_image_path)
    pil_qoi_image = Image.open(qoi_image_path)


    assert image.width == png_image.width == pil_qoi_image.width
    assert image.height == png_image.height == pil_qoi_image.height
    assert image.mode == pil_qoi_image.mode

    for img in png_image, pil_qoi_image:
        encoded = qoi_rs.encode(img.getdata(), width=img.width, height=img.height)
        assert isinstance(encoded, bytes)
        decoded = qoi_rs.decode(encoded)
        assert image.width == decoded.width
        assert image.height == decoded.height
        assert image.color_space == decoded.color_space
        assert image.mode == decoded.mode
        assert image.channels == image.channels
        assert image == decoded

    png_image.close()
    pil_qoi_image.close()
