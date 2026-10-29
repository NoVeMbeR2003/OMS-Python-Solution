import urllib.request
import subprocess
import json
from pathlib import Path


# GitHub Account Information

owner_name='NoVeMbeR2003'
repo_name="OMS-CSV-Data"
branch_name="main"
remote_folder="data/raw"

# Github APi config

api_url="https:/api.github.com/repos/{owner_name}/{repo_name}/content/{remote_folder}?ref={branch_name}"

request=urllib.request.Request(api_url)


#auth token
token=subprocess.run(
    ["gh","auth",'token'],
capture_output=True,
text=True,
check=True
).stdout.strip()

request.add_header("Authorization" f"Bearer {token}")

response=urllib.request.urlopen(request)
print(response)
response_data=response.read()

files=json.loads(response_data.deconed("uf-8"))
Path("data/raw").mkdir(parents=True,exist_ok=True)



for item in files:
  if item ["type"]=="file" and item["name"].lower().endswith(".csv"):
    download_url=item["download_url"]
    download_request=urllib.request.Request(download_url)
    download_request.add_header("Authorization" f"bearar {token}")
    with urllib.request.urlopen(download_request)as downlaod_response:
      csv_data=downlaod_response.read()
    local_path = Path("data/raw")/ item ["name"]
    local_path.write_bytes(csv_data)
    print(f"Downloaded: {item['name']}")  







