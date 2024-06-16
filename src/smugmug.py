import random
from rauth import OAuth1Service, OAuth1Session
from dotenv import load_dotenv
from yarl import URL
import sys
from pprint import pprint
from pathlib import Path

OAUTH_ORIGIN = 'https://secure.smugmug.com'
REQUEST_TOKEN_URL = OAUTH_ORIGIN + '/services/oauth/1.0a/getRequestToken'
ACCESS_TOKEN_URL = OAUTH_ORIGIN + '/services/oauth/1.0a/getAccessToken'
AUTHORIZE_URL = OAUTH_ORIGIN + '/services/oauth/1.0a/authorize'
API_ORIGIN = 'https://api.smugmug.com'
BASE_URL = API_ORIGIN + "/api/v2"

class SmugMugClient():
	def __init__(self, access_token, access_token_secret):
		self.access_token = access_token
		self.access_token_secret = access_token_secret
		
	def authenticate(self, api_key, api_secret):
		oauth = OAuth1Service(consumer_key=api_key, consumer_secret=api_secret, request_token_url=REQUEST_TOKEN_URL, access_token_url=ACCESS_TOKEN_URL,authorize_url=AUTHORIZE_URL, base_url=BASE_URL)
		if not self.access_token or not self.access_token_secret:
			request_token, request_token_secret = oauth.get_request_token(params={"oauth_callback": "oob"})
			auth_url = str(URL(oauth.get_authorize_url(request_token)).update_query({"Access": "Full", "Permissions": "Modify"}))
			sys.stdout.write(f"Go to {auth_url}, then enter the 6 digit code here: ")
			sys.stdout.flush()
			verifier = sys.stdin.readline().strip()
			self.access_token, self.access_token_secret = oauth.get_access_token(request_token, request_token_secret, params={"oauth_verifier": verifier})
		self.session = OAuth1Session(oauth.consumer_key, oauth.consumer_secret, access_token=self.access_token, access_token_secret=self.access_token_secret)
		authuser = self.get("!authuser")
		self.username = authuser["User"]["NickName"]
		return (self.access_token, self.access_token_secret)
	
	def base_url(self):
		return BASE_URL
	
	def full_url(self, path):
		return f"{API_ORIGIN}{path}"
	
	def get_user_data(self, path, params = {}):
		path = f"/user/{self.username}{path}"
		return self.get(path, params)
	
	def get(self, path, params = {}):
		response = self.session.get(f"{BASE_URL}{path}", headers={"Accept": "application/json", "Content-Type": "application/json"}, params=params)
		if response.status_code == 200:
			data = response.json()
			return data["Response"]
		else:
			response.raise_for_status()

	def get_albums(self):
			albums = self.get_user_data("!albums")["Album"]
			return albums

	def get_folder(self):
		folder = self.get(f"/folder/user/{self.username}")
		return folder

	def get_images(self,album_key, params = {}):
			response = self.get(f"/album/{album_key}!images", params)
			return response["AlbumImage"]

	def fetch_random_image(self):
			albums = self.get_albums()
			if not albums:
					print("No albums found.")
					return
			
			total = sum(album["ImageCount"] for album in albums)
			random_index = random.randrange(0, total - 1)
			index = 0
			random_image = None

			for album in albums:
				if index + album["ImageCount"] > random_index: 
					index = random_index - index
					images = self.get_images(album["AlbumKey"], {"start": index, "count": 1})
					random_image = images[0]
					return random_image
				else:
					index += album["ImageCount"]

			return None
	
	def download_and_classify_image(self, image, category, size="Medium", file_path="import"):
		size_url = image["Uris"]["LargestImage"]["Uri"]
		response = self.session.get(f"{API_ORIGIN}{size_url}", params={"s": size})
		response.raise_for_status()

		directory = Path(f"{file_path}/{category}")
		directory.mkdir(parents=True, exist_ok=True)

		with open(f"{file_path}/{category}/{image["FileName"]}", 'wb') as file:
			file.write(response.content)
