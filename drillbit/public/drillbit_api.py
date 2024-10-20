import requests
import json
import time
import jwt
import os
from requests.exceptions import RequestException


class DrillbitAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.jwt_token = " "
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
            self.jwt_token = response_data['token']
            self.jwt_expiry = jwt.decode(self.jwt_token, options={"verify_signature": False})['exp']

            print("Authentication successful.")
            # frappe.msgprint("Auth Success!")
            print(f"JWT token: {self.jwt_token}")
            print(f"Expires at: {time.ctime(self.jwt_expiry)}")

        except RequestException as e:
            print(f"Failed to authenticate: {e}")
            print(response.json() if response else "No response data")

    def is_token_valid(self):
        if self.jwt_token is None or self.jwt_expiry < time.time():
            return False
        return True

    def create_folder(
                    self,
                    folder_name,
                    exclude_reference="NO",
                    exclude_quotes="NO",
                    exclude_small_sources="NO",
                    grammar_check="NO",
                    exclude_phrases="NO",
                    db_studentpaper="YES",
                    db_publications="YES",
                    db_internet="YES",
                    institution_repository="YES",
                    email_notifications="NO",
                    exclude_threshold=14,
                    phrases=None
                ):
        url = f"{self.base_url}/pro/folder"
        headers = self.get_headers()
        
        data = {
            "folder_name": folder_name,
            "exclude_reference": exclude_reference,
            "exclude_quotes": exclude_quotes,
            "exclude_small_sources": exclude_small_sources,
            "grammar_check": grammar_check,
            "exclude_phrases": exclude_phrases,
            "db_studentpaper": db_studentpaper,
            "db_publications": db_publications,
            "db_internet": db_internet,
            "institution_repository": institution_repository,
            "email_notifications": email_notifications,
            "exclude_threshold": exclude_threshold,
        }

        if exclude_phrases == "YES" and phrases:
            data["phrases"] = phrases

        # Dump the entire request
        request_info = f"""
        Request URL: {url}
        Request Headers: {json.dumps(headers, indent=2)}
        Request Data: {json.dumps(data, indent=2)}
        """
        print(request_info)

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses

            return response

        except RequestException as e:
            print(f"Failed to create folder: {e}")
            if response is not None:
                # Dump the error response
                error_response_info = f"""
                Response Status Code: {response.status_code}
                Response Headers: {json.dumps(dict(response.headers), indent=2)}
                Response Body: {response.text}
                """
                print(error_response_info)
                return response

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://www.drillbitplagiarismcheck.com',
            'Referer': 'https://www.drillbitplagiarismcheck.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'authorization': f'Bearer {self.jwt_token}',
            'sec-ch-ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def upload_file(self, author_name, title, document_type, guide_email, guide_name, plagiarism_check, grammar_check, language, file_path, folder_id):
        url = f"{self.base_url}/files/folder/{folder_id}/singleFile"
        
        # Prepare the files and data for the request
        files = {
            'file': open(file_path, 'rb')  # Open the file in binary mode
        }
        data = {
            'authorName': author_name,
            'title': title,
            'documentType': document_type,
            'guide_email': guide_email,
            'guide_name': guide_name,
            'plagiarismCheck': plagiarism_check,
            'grammarCheck': grammar_check,
            'language': language,
        }
        
        # Set headers
        headers = {
            'Accept': 'application/json',
            'Connection': 'keep-alive',
            'Origin': 'https://www.drillbitplagiarismcheck.com',
            'Referer': 'https://www.drillbitplagiarismcheck.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'authorization': f'Bearer {self.jwt_token}',
        }

        # Debugging output
        print("----------------------------------------------------------------------------------------")
        print("Request URL:", url)
        print("Request Headers:", headers)
        print("Request Data:", data)
        print("Request Files:", files)
        print("----------------------------------------------------------------------------------------")

        # Make the POST request
        response = requests.post(url, headers=headers, data=data, files=files)
        
        # Debugging output for response
        print("----------------------------------------------------------------------------------------")
        print("Response Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Body:", response.text)
        print("----------------------------------------------------------------------------------------")
        
        # Handle the response
        return response.json()  # Assuming the API returns JSON
        # if response.status_code == 200:
        # else:
        #     response.raise_for_status()  # Raise an error for bad responses


    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.jwt_token}'
        }

    def debug_request(self, request):
        print("=== Request ===")
        print(f"URL: {request.url}")
        print(f"Method: {request.method}")
        print(f"Headers: {request.headers}")
        if request.body:
            print(f"Body: {request.body}")
        print("================")

    def debug_response(self, response):
        print("=== Response ===")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Body: {response.text}")
        print("================")
        
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

    def download_file(self, paper_id, d_key, folder_path):
        url = f"{self.base_url}/analysis-gateway/api/download2/{paper_id}/{d_key}"
        headers = {'Authorization': f'Bearer {self.jwt_token}'}

        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            return None
        file_path = os.path.join(folder_path, f"{paper_id}.pdf")
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully as {file_path}")
        return file_path



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

    def get_submissions_list(self, folder_id, paper_id):
        url = f"{self.base_url}/pro/folder/{folder_id}/submissions?paperId={paper_id}"
        headers = self.get_headers()

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            print("Submissions list retrieved successfully.")
            print(json.dumps(response_data, indent=4))
            return response_data

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

    def edit_folder(
                    self,
                    folder_id,
                    folder_name,
                    exclude_reference="NO",
                    exclude_quotes="NO",
                    exclude_small_sources="NO",
                    grammar_check="NO",
                    exclude_phrases="NO",
                    db_studentpaper="YES",
                    db_publications="YES",
                    db_internet="YES",
                    institution_repository="YES",
                    email_notifications="NO",
                    exclude_threshold=14,
                    phrases=None

                ):
        
        url = f"{self.base_url}/pro/folder/{folder_id}"
        headers = self.get_headers()
        
        data = {
            "folder_name": folder_name,
            "exclude_reference": exclude_reference,
            "exclude_quotes": exclude_quotes,
            "exclude_small_sources": exclude_small_sources,
            "grammar_check": grammar_check,
            "exclude_phrases": exclude_phrases,
            "db_studentpaper": db_studentpaper,
            "db_publications": db_publications,
            "db_internet": db_internet,
            "institution_repository": institution_repository,
            "email_notifications": email_notifications,
            "exclude_threshold": exclude_threshold,
        }
        if exclude_phrases == "YES" and phrases:
            data["phrases"] = phrases

        # Dump the entire request
        request_info = f"""
        Request URL: {url}
        Request Headers: {json.dumps(headers, indent=2)}
        Request Data: {json.dumps(data, indent=2)}
        """
        print(request_info)

        try:
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses

            # response_data = response.json()
            # # Dump the response
            # response_info = f"""
            # Response Status Code: {response.status_code}
            # Response Headers: {json.dumps(dict(response.headers), indent=2)}
            # Response Body: {json.dumps(response_data, indent=2)}
            # """
            # print(response_info)
            return response

        except RequestException as e:
            print(f"Failed to edit folder: {e}")
            if response is not None:
                # Dump the error response
                error_response_info = f"""
                Response Status Code: {response.status_code}
                Response Headers: {json.dumps(dict(response.headers), indent=2)}
                Response Body: {response.text}
                """
                print(error_response_info)
                return response

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
