import requests
import random
import json
from rauth import OAuth1Service, OAuth1Session
import os
from dotenv import load_dotenv
from yarl import URL
import sys
from smugmug import SmugMugClient
import pprint

SMUGMUG_SECRETS_FILE="./smugmug.env"

load_dotenv()
load_dotenv(SMUGMUG_SECRETS_FILE)

access_token=os.environ.get("SMUGMUG_ACCESS_TOKEN")
access_token_secret=os.environ.get("SMUGMUG_ACCESS_TOKEN_SECRET")
api_key = os.environ["SMUGMUG_API_KEY"]
api_secret = os.environ["SMUGMUG_API_SECRET"]

smugmug = SmugMugClient(access_token=access_token, access_token_secret=access_token_secret)
access_token, access_token_secret = smugmug.authenticate(api_key=api_key, api_secret=api_secret)
with open(SMUGMUG_SECRETS_FILE, "w") as smugmug_secrets:
  smugmug_secrets.write(f"SMUGMUG_ACCESS_TOKEN='{access_token}'\n")
  smugmug_secrets.write(f"SMUGMUG_ACCESS_TOKEN_SECRET='{access_token_secret}'\n")

image = smugmug.fetch_random_image()
print(image["WebUri"])