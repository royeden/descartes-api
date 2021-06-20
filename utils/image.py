from PIL import Image

from config import IMAGE_SIZE

def image_resize(image: Image.Image, size: int) -> Image.Image:
	return image.copy().resize((size, size), Image.NEAREST)

def image_crop(image: Image.Image) -> Image.Image:
	square = image.width == image.height
	if square:
		return image.copy().resize((IMAGE_SIZE, IMAGE_SIZE))
	landscape = image.width > image.height
	
	adjustment_percentage = (IMAGE_SIZE / float(image.width if landscape else image.height))
	adjusted_size = int(float(image.height if landscape else image.width) * float(adjustment_percentage))

	multiplier = 1

	while adjusted_size * multiplier < IMAGE_SIZE:
		multiplier += 1

	resized = image.copy().resize((
		multiplier * (IMAGE_SIZE if landscape else adjusted_size),
		multiplier * (adjusted_size if landscape else IMAGE_SIZE)
	), Image.NEAREST)

	left = int((resized.width - IMAGE_SIZE) / 2)
	top = int((resized.height - IMAGE_SIZE) / 2)
	right = int((resized.width + IMAGE_SIZE) / 2)
	bottom = int((resized.height + IMAGE_SIZE) / 2)

	# Crop the center of the image
	crop = resized.copy().crop((left, top, right, bottom))

	return crop.resize((IMAGE_SIZE, IMAGE_SIZE), Image.NEAREST)

def new_image_crop(image: Image.Image) -> Image.Image:
	if image.size[0] < image.size[1]:
			wpercent = (IMAGE_SIZE / float(image.size[0]))
			hsize = int((float(image.size[1]) * float(wpercent)))
			wsize = IMAGE_SIZE
	else:
			hpercent = (IMAGE_SIZE / float(image.size[1]))
			wsize = int((float(image.size[0]) * float(hpercent)))
			hsize = IMAGE_SIZE

	image = image.resize((wsize, hsize), Image.ANTIALIAS)

	# crop
	return image.crop([image.size[0] / 2 - IMAGE_SIZE / 2, image.size[1] / 2 - IMAGE_SIZE / 2, image.size[0] / 2 + IMAGE_SIZE / 2, image.size[1] / 2 + IMAGE_SIZE / 2])