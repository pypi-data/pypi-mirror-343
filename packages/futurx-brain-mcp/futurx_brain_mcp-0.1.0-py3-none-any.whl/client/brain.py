import requests

from src.common.secret import BASE_URL, API_KEY, HOST_ID

def knowledge_training(file_path: str) -> dict:
  '''
  Upload a file to the brain and get an URL for future training
  '''

  url = f"{BASE_URL}/v1/brainmanager/knowledge/training/file"
  headers = {
    "Authorization": f"Bearer {API_KEY}"
  }
  files = {"file": open(file_path, "rb")}

  # Send the request with multipart/form-data
  data = {
    "host_id": HOST_ID,
  }
  response = requests.post(url, headers=headers, data=data, files=files)

  print(response.json())
  
  if response.status_code != 200:
    raise Exception(f"Failed to upload file: {response.status_code} {response.text}")

  return response.json()


def retrieval(query: str) -> dict:
  '''
  Retrieve the knowledge, memory and etc from the brain
  '''

  url = f"{BASE_URL}/v1/brainmanager/retrieval"

