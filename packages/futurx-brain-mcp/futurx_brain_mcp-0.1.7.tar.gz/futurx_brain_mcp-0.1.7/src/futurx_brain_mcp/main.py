from mcp.server.fastmcp import FastMCP
import os
import requests

API_KEY = os.getenv("FUTURX_BRAIN_API_KEY") or ""
BASE_URL = os.getenv("FUTURX_BRAIN_BASE_URL") or "http://localhost:8081"
# TODO: get host id from the api key
HOST_ID = os.getenv("FUTURX_BRAIN_HOST_ID") or ""

class Brain:
  def __init__(self):
    print("Brain initialized")

  def knowledge_training(self, file_path: str) -> dict:
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

  def retrieval(self, query: str) -> dict:
    '''
    Retrieve the knowledge, memory and etc from the brain
    '''

    url = f"{BASE_URL}/v1/brainmanager/retrieval"


mcp = FastMCP("Futurx Brain MCP")

brain = Brain()

@mcp.tool()
def knowledge_training(file_path: str):
    '''
    Upload a local file to the brain service and start the knowledge training
    '''
    try:
        brain.knowledge_training(file_path)
    except Exception as e:
        return f"Failed to train the file: {e}"

    return f"Successfully trained the file: {file_path}, please wait for the training to complete"

if __name__ == "__main__":
    if not API_KEY or not HOST_ID:
        raise Exception("API_KEY and HOST_ID are not set")

    mcp.run(transport="stdio")
