import argparse
import sys
import os
from dotenv import load_dotenv


# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, project_root)

from scripts import sm_import
from smugmug import SmugMugClient

scripts = {"import": sm_import.main}

SMUGMUG_SECRETS_FILE = "./smugmug.env"

load_dotenv()
load_dotenv(SMUGMUG_SECRETS_FILE)


def main():
	access_token = os.environ.get("SMUGMUG_ACCESS_TOKEN")
	access_token_secret = os.environ.get("SMUGMUG_ACCESS_TOKEN_SECRET")
	api_key = os.environ["SMUGMUG_API_KEY"]
	api_secret = os.environ["SMUGMUG_API_SECRET"]

	smugmug = SmugMugClient(access_token=access_token, access_token_secret=access_token_secret)
	access_token, access_token_secret = smugmug.authenticate(api_key=api_key, api_secret=api_secret)
	with open(SMUGMUG_SECRETS_FILE, "w") as smugmug_secrets:
		smugmug_secrets.write(f"SMUGMUG_ACCESS_TOKEN='{access_token}'\n")
		smugmug_secrets.write(f"SMUGMUG_ACCESS_TOKEN_SECRET='{access_token_secret}'\n")

	parser = argparse.ArgumentParser(description="SmugMug Vision CLI")
	parser.add_argument("script", help="The name script in scripts/ to run")
	args, script_args = parser.parse_known_args()
	args = vars(args)
	script = scripts[args.pop("script")]
	script(**args, smugmug=smugmug)


if __name__ == "__main__":
	main()
