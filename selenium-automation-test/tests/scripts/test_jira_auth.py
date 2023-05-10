from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import base64

class JiraAPICall:
    def __init__(self):
        load_dotenv()
        self.jira_email = os.environ.get("JIRA_EMAIL")
        self.jira_token = os.environ.get("JIRA_TOKEN")
        self.base_url = os.environ.get("BASE_URL")
        self.search_api_url = os.environ.get("SEARCH_API_URL")
        self.auth = HTTPBasicAuth(self.jira_email, self.jira_token)
        self.headers = {'Content-Type': 'application/json;charset=iso-8859-1'}
        self.jql_query = "project = AT"

    #def is_authenticated_to_jira():


    def get_issue_list(self):
        # Define the JQL query to retrieve all issues
        jql_query = self.jql_query
        # Define the fields to be included in the response
        fields = ["summary", "description", "issuetype", "assignee", "status", "attachment"]
        # Send the HTTP request to retrieve all issues
        res = requests.post(
            self.base_url + self.search_api_url,
            headers=self.headers,
            auth=self.auth,
            json={
                "jql": jql_query,
                "fields": fields
            }
        )
        if res.status_code == 200:
            issues = res.json()['issues']
            for issue in issues:
                print(f"Issue Key: {issue['key']}")
                print(f"Issue Summary: {issue['fields']['summary']}")
                print(f"Issue Status: {issue['fields']['status']['name']}")
                
                if len(issue['fields']['attachment']) > 0:
                    print(f"Issue Attachment: {issue['fields']['attachment']}")
                else:
                    print("No Attachment") 
            return issues
        else:
            print("Failed to fetch issues from Jira")
            print(f"Response: {res.content}")  
        return None
    
    
    def get_issue_attachments(self, issue_key):
        # Define the JQL query to retrieve the specified issue and its attachments
        jql_query = f"{self.jql_query} AND key={issue_key}"
        # Define the fields to be included in the response
        fields = ["attachment"]
        # Send the HTTP request to retrieve the specified issue
        res = requests.post(
            self.base_url + self.search_api_url,
            headers=self.headers,
            auth=self.auth,
            json={
                "jql": jql_query,
                "fields": fields
            }
        )
        if res.status_code == 200:
            issue = res.json()['issues'][0]
            attachments = issue['fields']['attachment']
            if len(attachments) > 0:
                print(f"Attachments for Issue Key {issue_key}:")
            else:
                print(f"No attachments for Issue Key {issue_key}")
            return attachments
        else:
            print(f"Failed to fetch issue {issue_key} from Jira")
            print(f"Response: {res.content}")
        return None
    
    
    def open_file(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                contents = file.read()
                print("File exist")
            return True
        else:
            print(f"File {file_path} does not exist.")
            
    
    def attach_file_to_jira_issue(self, issue_key, test_result_data):
        # Construct the JIRA API endpoint URL
        api_url = f"{self.base_url}/rest/api/3/issue/{issue_key}/attachments"
        # Define the headers for the request
        self.headers = {
            'X-Atlassian-Token': 'no-check',
        }
        # Extract the only filename from the path
        test_result_filename = os.path.basename(test_result_data)
        
        # Access file content for duplication checking
        if self.compare_attachment(test_result_filename, issue_key) == False:
            # Define the data for the request
            files = {
                'file': (f'{issue_key}-{test_result_filename}', open(test_result_data, "rb"))
            }
            # Send the request to attach the test result data to the JIRA issue
            res = requests.post(
                api_url,
                files=files,
                auth=self.auth,
                headers=self.headers
            )
            # print(f"res: {res}")
            # Check if the request was successful
            if res.status_code != 200:
                raise Exception(f"Failed to upload {test_result_data} to JIRA issue {issue_key}. Error: {res}")
            print(f"Successfully uploaded {test_result_data} to JIRA issue '{issue_key}'")
        else:
            print(f"Failed to upload result as {test_result_data} found duplication content to the attachment of JIRA issue '{issue_key}'")
        
        
    #def delete_file_exist_from_jira_issue(self, issue_key):
    
    
    #def update_file_in_jira_issue(self, issue_key):
    
    
    #def is_file_exist_in_jira(self, issue_key):
    
    
    #def is_issue_exist_in_jira(self, issue_key):
    
    
    def compare_attachment(self, file_name, issue_key):
        # Define the JQL query to retrieve the issue by key
        jql_query = f"key = {issue_key}"
        # Define the fields to be included in the response
        fields = ["attachment"]
        # Send the HTTP request to retrieve the issue
        res = requests.post(
            self.base_url + self.search_api_url,
            headers=self.headers,
            auth=self.auth,
            json={
                "jql": jql_query,
                "fields": fields
            }
        )
        if res.status_code == 200:
            if self.is_any_attachment_exist_in_jira(issue_key) == True:
                issue = res.json()['issues'][0]
                duplication_no = 0
                for attachment in issue['fields']['attachment']:
                    if attachment['filename'] == f"{issue_key}_{file_name}":
                        duplication_no += 1
                        #print(f"Found attachment with name {file_name}")
                        attachment_data = attachment['content']
                        # Decode attachment data
                        attachment_bytes = base64.b64decode(attachment_data)
                        # Read local file
                        with open(file_name, 'rb') as f:
                            local_bytes = f.read()
                        # Compare file contents
                        if attachment_bytes == local_bytes:
                            print("The contents of the files are the same")
                            return True
                        else:
                            print("The contents of the files are different")
                            return False
                    else:
                        print(f"No same attachment content found with name {file_name} in issue {issue_key}.")
                if duplication_no > 0:
                    print(f"Found {duplication_no} attachments has duplicated content with name {file_name}")
        else:       
            print(f"No attachment found with name {file_name} in {issue_key}.")
            return False
    
    
    def is_any_attachment_exist_in_jira(self, issue_key):
        # Define the JQL query to retrieve the issue by key
        jql_query = f"key = {issue_key}"
        # Define the fields to be included in the response
        fields = ["attachment"]
        # Send the HTTP request to retrieve the issue
        res = requests.post(
            self.base_url + self.search_api_url,
            headers=self.headers,
            auth=self.auth,
            json={
                "jql": jql_query,
                "fields": fields
            }
        )
        if res.status_code == 200:
            issue = res.json()['issues'][0]
            if len(issue['fields']['attachment']) > 0:
                print(f"Issue {issue_key} has {len(issue['fields']['attachment'])} attachments.")
                return True
            else:
                print(f"Issue {issue_key} has no attachments.")
                return False
        else:
            print(f"Failed to fetch issue {issue_key} from Jira")
            print(f"Response: {res.content}")
            return False


if __name__ == "__main__":
    jira = JiraAPICall()
    #jira.get_issue_list()
    # Example usage of post_test_result_to_jira method
    issue_key = "AT-1"
    filepath = "../../reports/20230506/test_login-20230506_231631_report.html"
    #jira.open_file(filepath)
    
    #jira.get_issue_attachments(issue_key)
    
    # attachment
    jira.attach_file_to_jira_issue(issue_key, filepath)
    #jira.delete_file_exist_from_jira_issue(issue_key, filepath)
    #jira.update_file_in_jira_issue(issue_key, filepath)
    #jira.is_any_attachment_exist_in_jira(issue_key)
    # attach description
    
    # issue
    # issue_story_summary = "new summary"
    # issue_story_type = ""
    # jira.create_issue(summary)

   