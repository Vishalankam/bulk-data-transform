import json
import requests

from . import API_VERSION
from connectors.salesforce import CONNECTOR_NAME
from factories.abstract_upload_data_factory import AbstractUploadDataFactory
from utils.helpers import log_details


class UploadData(AbstractUploadDataFactory):

    def __init__(self, host_uri, auth_token, dest_object) -> None:
        self.host_uri = host_uri
        self.auth_token = auth_token
        self.dest_object = dest_object
        self.content_url = None
        self.job_id = None
        self.zendesk_endpoints = {
            "users": "users/create_many",
            "tickets": "imports/tickets/create_many",
            "organizations": "organizations/create_many"
        }
        super().__init__()

    def get_headers(self):
        return {
            "Authorization": "Basic {0}".format(self.auth_token),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


    def upload_batch(self, data_batch):
        uri = """{0}api/v{1}/{2}""".format(self.host_uri, API_VERSION, self.zendesk_endpoints[self.dest_object])
        headers = self.get_headers()
        data = {"{}".format(self.dest_object) : data_batch}
        response = requests.post(uri, data=json.dumps(data),  headers=headers)        
        if response.status_code >= 400:
             msg = "Bulk API HTTP Error result: {0}".format(response.text)
             raise Exception(msg, response.status_code)
       
        resp =  json.loads(response.content)
        self.content_url = resp['job_status']['url']

        log_details(CONNECTOR_NAME, "UploadData","upload_batch", "Uploading the batch..!")
        print("You can view the status on url - {0}".format(self.content_url))
        return response.status_code


    def check_job_status(self):
        if self.content_url: 
            uri = self.content_url 
            resp = requests.get(uri,  headers=self.get_headers())
            if resp.status_code >= 400:
                 msg = "Bulk API HTTP Error result: {0}".format(resp.text)
                 raise Exception(msg, resp.status_code)

            response = json.loads(resp.content)
            state = response['job_status']['status']
            log_details(CONNECTOR_NAME, "UploadData","check_job_status",  state)
            return state
        else:
            return "killed"