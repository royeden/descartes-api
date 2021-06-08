from enum import IntEnum
from PIL import Image

VALID_IMAGE_SIZES = IntEnum('VALID_IMAGE_SIZES', { i : 2**(i + 1) for i in range(10) })

def image_resize(image: Image.Image, size: VALID_IMAGE_SIZES) -> Image.Image:
	return image.copy().resize((size, size), Image.NEAREST)

def image_crop(image) -> Image.Image:
	landscape = image.width > image.height
	
	fixed_size = 1024
	
	adjustment_percentage = (fixed_size / float(image.width if landscape else image.height))
	adjusted_size = int(float(image.height if landscape else image.width) * float(adjustment_percentage))

	multiplier = 1

	while adjusted_size * multiplier < fixed_size:
		multiplier += 1

	resized = image.copy().resize((
		multiplier * (fixed_size if landscape else adjusted_size),
		multiplier * (adjusted_size if landscape else fixed_size)
	), Image.NEAREST)

	left = int((resized.width - fixed_size) / 2)
	top = int((resized.height - fixed_size) / 2)
	right = int((resized.width + fixed_size) / 2)
	bottom = int((resized.height + fixed_size) / 2)

	# Crop the center of the image
	crop = resized.copy().crop((left, top, right, bottom))
	return crop.resize((fixed_size, fixed_size), Image.NEAREST)
