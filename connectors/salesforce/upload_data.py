import json
import requests

from . import API_VERSION, CONNECTOR_NAME
from factories.abstract_upload_data_factory import AbstractUploadDataFactory
from utils.helpers import log_details

class UploadData(AbstractUploadDataFactory):

    def __init__(self, host_uri, auth_token, dest_object) -> None:
        self.host_uri = host_uri
        self.auth_token = auth_token
        self.dest_object = dest_object
        self.content_url = None
        self.job_id = None
        super().__init__()


    def create_job(self):
        if not self.dest_object:
            self.get_destination_address()
            if not self.dest_object:
                except_code = 'INVALID SALESFORCE OBJECT NAME'
                except_msg = (
                    'You must submit valid salesforce objest name to upload the data.'
                )
                raise Exception({except_code, except_msg})

        uri = "https://{0}/services/data/v{1}/jobs/ingest/".format(self.host_uri, API_VERSION)
        headers ={
                "Authorization":"""Bearer {}""".format(self.auth_token),
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
        self.content_url = response['contentUrl']
        self.job_id = response['id']

        return resp


   
    def upload_batch(self, data_batch):
        uri = "https://{0}/{1}".format(self.host_uri, self.content_url)
        headers ={
                "Authorization":"""Bearer {}""".format(self.auth_token),
                "Content-Type": "text/csv",
                'Accept-Encoding': "gzip",               
                 }
        resp = requests.put(uri, data=data_batch, headers=headers)
        if resp.status_code >= 400:
             msg = "Bulk API HTTP Error result: {0}".format(resp.text)
             raise Exception(msg, resp.status_code)

        log_details(CONNECTOR_NAME, "UploadData", "upload_batch", "Uploading the batch..!")
        return resp.status_code


    def start_upload(self):
        uri = "https://{0}/services/data/v{1}/jobs/ingest/{2}".format(self.host_uri, API_VERSION, self.job_id)
        headers ={
                "Authorization":"""Bearer {}""".format(self.auth_token),
                "Content-Type": "application/json; charset=UTF-8",
                'Accept-Encoding': "application/json",               
                 }
        data ={ "state" : "UploadComplete"}
        resp = requests.patch(uri, data = json.dumps(data),  headers=headers)
        if resp.status_code >= 400:
             msg = "Bulk API HTTP Error result: {0}".format(resp.text)
             raise Exception(msg, resp.status_code)

        response = json.loads(resp.content)
        state = response['state']
        log_details(CONNECTOR_NAME, "UploadData", "start_upload", "Uploaded the batch data..!")
        return state


    def check_job_status(self):
        uri = "https://{0}/services/data/v{1}/jobs/ingest/{2}".format(self.host_uri,API_VERSION, self.job_id)
        headers ={
                "Authorization":"""Bearer {}""".format(self.auth_token),
                "Content-Type": "text/csv",
                'Accept-Encoding': "gzip",               
                 }
        resp = requests.get(uri,  headers=headers)
        if resp.status_code >= 400:
             msg = "Bulk API HTTP Error result: {0}".format(resp.text)
             raise Exception(msg, resp.status_code)

        response = json.loads(resp.content)
        print("file: upload_data.py ~ line 57 ~ resp.status_code", response)
        state = response['state']
        return state, response['numberRecordsFailed']