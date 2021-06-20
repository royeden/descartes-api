import os
from config import basedir, db
from models.resource import Resource

from PIL import Image
import numpy as np
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras import Model
import umap
import tqdm

LAYER=1
SIZE=300
MODEL_FILENAME="umap-model.model"
BATCH_SIZE=32

def calculate_position(p: int):
	multiplier = 5 # Delimits space between elements
	difference = (multiplier / 2) * 10
	return int(p * multiplier - difference)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def images_to_grid(filenames, size=SIZE, layer=LAYER, batch_size=BATCH_SIZE, n_neighbors=30, min_dist=0.5):
	layer_num = layer

	global imgs
	imgs = []

	for filename in tqdm.tqdm(filenames):
		try:
			# abre imagen
			img = Image.open(filename).resize((1024, 1024))

			# convertir de modo por las dudas
			img = img.convert(mode='RGBA')

			# resize
			if img.size[0] < img.size[1]:
				wpercent = (size / float(img.size[0]))
				hsize = int((float(img.size[1]) * float(wpercent)))
				wsize = size
			else:
				hpercent = (size / float(img.size[1]))
				wsize = int((float(img.size[0]) * float(hpercent)))
				hsize = size

			img = img.resize((wsize, hsize), Image.ANTIALIAS)

			# crop
			img = img.crop([img.size[0] / 2 - size / 2, img.size[1] / 2 - size / 2, img.size[0] / 2 + size / 2, img.size[1] / 2 + size / 2])

			# transformar a array de numpy y descartar el alpha
			img = np.array(img)[:, :, 0:3]
			imgs.append(img)

		except:
			pass

	imgs = np.array(imgs)

	model = VGG16(weights='imagenet', include_top=False)

	if layer < 1 and layer > 5:
		layer = 1

	layer = 'block{}_pool'.format(layer)

	model = Model(inputs=model.input, outputs=model.get_layer(layer).output)


	imgsPreprocessed = []
	for img in tqdm.tqdm(imgs):
		imgsPreprocessed.append(preprocess_input(img))

	vgg_features = []
	for img in tqdm.tqdm(chunks(imgsPreprocessed,batch_size)):
        # extraigo descriptores de la red neuronal
		temp = model.predict(np.array(img))
		vgg_features.append(temp.mean(1).mean(1))

	vgg_features = np.vstack(vgg_features)

	columns = int(np.ceil(np.sqrt(len(imgs))))
	# now = time.strftime("%Y%m%d-%H%M%S")
	print('Number of colums', columns)

	#sin ordenar
	global data2d
	data3d = []
	for x in range(len(imgs)):
		data3d.append( [ x, 0 ])

	umap3d = umap.UMAP(n_components=3, n_neighbors=n_neighbors, min_dist=min_dist) # 3D y exportar como CSV o JSON
	# data3d = umap3d.fit_transform(imgs.mean(1).mean(1)) # data 3d de las imagenes
	data3d = umap3d.fit_transform(vgg_features) # data 3d de las imagenes
	
	import joblib
	umap_model = MODEL_FILENAME

	joblib.dump(umap3d, os.path.join(basedir, umap_model))

	return data3d

def fit_image(filename):
	size = SIZE
	layer = LAYER
	batch_size = BATCH_SIZE

	global imgs
	imgs = []

	try:
		# abre imagen
		img = Image.open(filename).resize((1024, 1024))

		# convertir de modo por las dudas
		img = img.convert(mode='RGBA')

		if img.size[0] < img.size[1]:
			wpercent = (size / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			wsize = size
		else:
			hpercent = (size / float(img.size[1]))
			wsize = int((float(img.size[0]) * float(hpercent)))
			hsize = size

		img = img.resize((wsize, hsize), Image.ANTIALIAS)

		# crop
		img = img.crop([img.size[0] / 2 - size / 2, img.size[1] / 2 - size / 2, img.size[0] / 2 + size / 2, img.size[1] / 2 + size / 2])

		# transformar a array de numpy y descartar el alpha
		img = np.array(img)[:, :, 0:3]
		imgs.append(img)
	
	except:
		pass

	imgs = np.array(imgs)

	model = VGG16(weights='imagenet', include_top=False)

	if layer < 1 and layer > 5:
		layer = 1

	layer = 'block{}_pool'.format(layer)

	model = Model(inputs=model.input, outputs=model.get_layer(layer).output)

	imgsPreprocessed = []
	for img in tqdm.tqdm(imgs):
		imgsPreprocessed.append(preprocess_input(img))

	vgg_features = []
	for img in tqdm.tqdm(chunks(imgsPreprocessed,batch_size)):
        # extraigo descriptores de la red neuronal
		temp = model.predict(np.array(img))
		vgg_features.append(temp.mean(1).mean(1))

	vgg_features = np.vstack(vgg_features)

	import joblib
	loaded_umap = joblib.load(MODEL_FILENAME)
	position = loaded_umap.transform(vgg_features)[0]
	return map(calculate_position, position)

def build_map():
	resources = Resource.query.order_by(Resource.resource_id).all()
	path = os.path.join(basedir, "storage")
	# remember to rescale all images to the same size before attempting anything

	filenames = map(lambda resource: path + "/" + resource.filename, resources)
	points = images_to_grid(filenames=filenames, n_neighbors=7, min_dist=0.77)

	for i, point in enumerate(points):
		[x, y, z] = point
		resource = resources[i]

		resource.x = calculate_position(x)
		resource.y = calculate_position(y)
		resource.z = calculate_position(z)

		db.session.merge(resource)
		db.session.commit()

	return {}, 200

