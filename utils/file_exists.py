import os

def file_exists(filename):
	os.path.exists(f"static/{filename}")