import json
from venv import create
import requests
from factories.abstract_upload_data_factory import AbstractUploadDataFactory
from utils.constants import SALESFORCE_API_VERSION


class SalesforceUploadData(AbstractUploadDataFactory):

    def __init__(self, host_uri, session_id) -> None:
        self.host_uri = host_uri
        self.session_id = session_id
        self.dest_object =None
        self.content_url = None
        self.job_id = None
        super().__init__()


    def take_destination_address(self):
        dest = input("Insert the destination salesforce object:")
        if (dest):
            self.dest_object = dest


    def create_job(self):
        if not self.dest_object:
            self.take_destination_address()
            if not self.dest_object:
                except_code = 'INVALID SALESFORCE OBJECT NAME'
                except_msg = (
                    'You must submit valid salesforce objest name to upload the data.'
                )
                raise Exception({except_code, except_msg})

        uri = "https://{0}/services/data/v{1}/jobs/ingest/".format(self.host_uri, SALESFORCE_API_VERSION)
        headers ={
                "Authorization":"""Bearer {}""".format(self.session_id),
                "Content-Type": "application/json; charset=UTF-8",
                "Accept": "application/json"
                }
        data = {
            "object" : self.dest_object,
            "contentType" : "CSV",
            "operation" : "insert",
            "lineEnding" : "LF"

            }

        resp = requests.post(uri, data=json.dumps(data) , headers=headers)
        if resp.status_code >= 400:
            msg = "Bulk API HTTP Error result: {0}".format(resp.text)
            raise Exception(msg, resp.status_code)

        response = json.loads(resp.content)
        print("🚀 ~ file: salesforce_upload_data.py ~ line 57 ~ resp.status_code", response)
        self.content_url = response['contentUrl']
        self.job_id = response['id']

        return resp


   
    def upload_batch(self, data_generator):
        uri = "https://{0}/{1}".format(self.host_uri, self.content_url)
        headers ={
                "Authorization":"""Bearer {}""".format(self.session_id),
                "Content-Type": "text/csv",
                'Accept-Encoding': "gzip",               
                 }
        resp = requests.put(uri, data=data_generator, headers=headers)
        print("🚀 ~ file: salesforce_upload_data.py ~ line 59 ~ resp", resp)
        if resp.status_code >= 400:
             msg = "Bulk API HTTP Error result: {0}".format(resp.text)
             raise Exception(msg, resp.status_code)

        print("Uploading the batch..!")
        return resp.status_code


    def upload_data(self):
        uri = "https://{0}/services/data/v{1}/jobs/ingest/{2}".format(self.host_uri,SALESFORCE_API_VERSION, self.job_id)
        headers ={
                "Authorization":"""Bearer {}""".format(self.session_id),
                "Content-Type": "application/json; charset=UTF-8",
                'Accept-Encoding': "application/json",               
                 }
        data ={ "state" : "UploadComplete"}
        resp = requests.patch(uri, data = json.dumps(data),  headers=headers)
        print("🚀 ~ file: salesforce_upload_data.py ~ line 59 ~ resp", resp)
        if resp.status_code >= 400:
             msg = "Bulk API HTTP Error result: {0}".format(resp.text)
             raise Exception(msg, resp.status_code)

        print("🚀 ~ file: salesforce_upload_data.py ~ line 85 ~ resp.state", resp.content)
        response = json.loads(resp.content)
        print("🚀 ~ file: salesforce_upload_data.py ~ line 57 ~ resp.status_code", response)
        state = response['state']
        # print("Uploaded the data..!")
        return state


    def check_job_status(self):
        uri = "https://{0}/services/data/v{1}/jobs/ingest/{2}".format(self.host_uri,SALESFORCE_API_VERSION, self.job_id)
        headers ={
                "Authorization":"""Bearer {}""".format(self.session_id),
                "Content-Type": "text/csv",
                'Accept-Encoding': "gzip",               
                 }
        resp = requests.get(uri,  headers=headers)
        print("🚀 ~ file: salesforce_upload_data.py ~ line 59 ~ resp", resp)
        if resp.status_code >= 400:
             msg = "Bulk API HTTP Error result: {0}".format(resp.text)
             raise Exception(msg, resp.status_code)

        print("🚀 ~ file: salesforce_upload_data.py ~ line 85 ~ resp.state", resp.content)
        response = json.loads(resp.content)
        print("🚀 ~ file: salesforce_upload_data.py ~ line 57 ~ resp.status_code", response)
        state = response['state']
        # print("Uploaded the data..!")
        return state