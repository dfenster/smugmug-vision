import sys

def main(smugmug):
	another = True
	while another:
		image = smugmug.fetch_random_image()
		print(image["WebUri"])
		print("Enter a category to classify the photo: ")
		category = sys.stdin.readline().strip()
		if category:
			smugmug.download_and_classify_image(image, category=category)
		print("Another (y/n)? ")
		another_str = sys.stdin.readline().strip().lower()
		if another_str == "y":
			another = True
		elif another_str == "n":
			another = False
