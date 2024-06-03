def main(smugmug):
	image = smugmug.fetch_random_image()
	print(image["WebUri"])
