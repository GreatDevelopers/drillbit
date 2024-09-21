import requests
import json
import time
import jwt
import os
from requests.exceptions import RequestException


class DrillbitAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.jwt_token = None
        self.jwt_expiry = 0

    def authenticate(self, username, password, frappe):
        url = f"{self.base_url}/authentication/authenticate"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            response_data = response.json()
            self.jwt_token = response_data['jwt']
            self.jwt_expiry = jwt.decode(self.jwt_token, options={"verify_signature": False})['exp']

            print("Authentication successful.")
            frappe.msgprint("Auth Success!")
            print(f"JWT token: {self.jwt_token}")
            print(f"Expires at: {time.ctime(self.jwt_expiry)}")

        except RequestException as e:
            print(f"Failed to authenticate: {e}")
            print(response.json() if response else "No response data")

    def is_token_valid(self):
        if self.jwt_token is None or self.jwt_expiry < time.time():
            return False
        return True

    def create_folder(self, folder_name):
        url = f"{self.base_url}/pro/folder"
        headers = self.get_headers()
        data = {
            "folder_name": folder_name,
            "exclude_reference": "NO",
            "exclude_quotes": "NO",
            "exclude_small_sources": "YES",
            "grammar_check": "NO",
            "db_studentpaper": "YES",
            "db_publications": "YES",
            "db_internet": "YES",
            "institution_repository": "YES",
            "exclude_phrases": "YES",
            "phrases": {
                "p1": "phrases 1",
                "p2": "phrases 2",
                "p3": "Phrases 3"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            response_data = response.json()
            status = response_data['status']
            message = response_data['message']
            timestamp = response_data['timeStamp']

            print(f"Folder creation status: {status}")
            print(f"Message: {message}")
            print(f"Timestamp: {timestamp}")

        except RequestException as e:
            print(f"Failed to create folder: {e}")

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.jwt_token}'
        }

    def upload_file(self, folder_id, file_path, author_name, title, document_type):
        url = f"{self.base_url}/files/folder/{folder_id}/singleFile"
        headers = {'Authorization': f'Bearer {self.jwt_token}'}
        files = {
            'authorName': (None, author_name),
            'title': (None, title),
            'documentType': (None, document_type),
            'plagiarismCheck': (None, 'YES'),
            'grammarCheck': (None, 'NO'),
            'file': (os.path.basename(file_path), open(file_path, 'rb'))
        }

        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()

            response_data = response.json()
            status = response_data['status']
            message = response_data['message']

            print(f"File upload status: {status}")
            print(f"Message: {message}")

        except RequestException as e:
            print(f"Failed to upload file: {e}")

    def create_submission(self, folder_id, submission_id, name, title, assignment_id, doc_type, file_path):
        url = f"{self.base_url}/pro/folder/{folder_id}/submission/{submission_id}"
        headers = self.get_headers()
        files = {
            'name': (None, name),
            'title': (None, title),
            'assignment_id': (None, assignment_id),
            'doc_type': (None, doc_type),
            'file': (os.path.basename(file_path), open(file_path, 'rb'))
        }

        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()

            response_data = response.json()
            paper_id = response_data['paper_id']

            print(f"Submission created successfully with paper ID: {paper_id}")

        except RequestException as e:
            print(f"Failed to create submission: {e}")

    def download_file(self, paper_id, d_key):
        url = f"{self.base_url}/analysis-gateway/api/download2/{paper_id}/{d_key}"
        headers = {'Authorization': f'Bearer {self.jwt_token}'}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            with open(f"{paper_id}.pdf", 'wb') as file:
                file.write(response.content)

            print(f"File downloaded successfully as {paper_id}.pdf")

        except RequestException as e:
            print(f"Failed to download file: {e}")

    def get_folders_list(self, page=0, size=25, field='ass_id', order_by='desc'):
        url = f"{self.base_url}/pro/folders?page={page}&size={size}&field={field}&orderBy={order_by}"
        headers = self.get_headers()

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            print("Folders list retrieved successfully.")
            print(json.dumps(response_data, indent=4))

        except RequestException as e:
            print(f"Failed to get folders list: {e}")

    def get_submissions_list(self, folder_id, page=0, size=25, field='paper_id', order_by='desc'):
        url = f"{self.base_url}/pro/folder/{folder_id}/submissions?page={page}&size={size}&field={field}&orderBy={order_by}"
        headers = self.get_headers()

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            print("Submissions list retrieved successfully.")
            print(json.dumps(response_data, indent=4))

        except RequestException as e:
            print(f"Failed to get submissions list: {e}")

    def delete_folder(self, folder_id):
        url = f"{self.base_url}/pro/folder/{folder_id}"
        headers = self.get_headers()

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            print(f"Folder deleted successfully. Message: {response_data['message']}")

        except RequestException as e:
            print(f"Failed to delete folder: {e}")

    def edit_folder(self, folder_id, folder_name):
        url = f"{self.base_url}/pro/folder/{folder_id}"
        headers = self.get_headers()
        data = {
            "folder_name": folder_name,
            "exclude_reference": "NO",
            "exclude_quotes": "NO",
            "exclude_small_sources": "NO",
            "grammar_check": "NO",
            "db_studentpaper": "YES",
            "db_publications": "YES",
            "db_internet": "YES",
            "institution_repository": "YES",
            "exclude_phrases": "YES",
            "phrases": {
                "p1": "phrases 1",
                "p2": "phrases 2",
                "p3": "Phrases 3"
            }
        }

        try:
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()

            response_data = response.json()
            status = response_data['status']
            message = response_data['message']
            timestamp = response_data['timeStamp']

            print(f"Folder edit status: {status}")
            print(f"Message: {message}")
            print(f"Timestamp: {timestamp}")

        except RequestException as e:
            print(f"Failed to edit folder: {e}")

    def delete_submission(self, folder_id, paper_id):
        url = f"{self.base_url}/pro/folder/{folder_id}/submissions?paperId={paper_id}"
        headers = self.get_headers()

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            print(f"Submission deleted successfully. Message: {response_data['message']}")

        except RequestException as e:
            print(f"Failed to delete submission: {e}")

if __name__ == "__main__":
    base_url = "https://s1.drillbitplagiarismcheck.com"
    api = DrillbitAPI(base_url)

    username = os.getenv("DRILLBIT_USERNAME")
    password = os.getenv("DRILLBIT_PASSWORD")

    api.authenticate(username, password)

    if api.is_token_valid():
        # Example usage
        folder_name = "Pro folder"
        api.create_folder(folder_name)
        # Add more method calls as needed for testing
    else:
        print("Unable to proceed, authentication failed.")
