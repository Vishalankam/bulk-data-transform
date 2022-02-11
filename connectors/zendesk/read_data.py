
from time import sleep
import csv

from . import BATCH_LIMIT, CONNECTOR_NAME
from connectors.zendesk.upload_data import UploadData
from factories.abstract_read_data_factory import AbstractReadDataFactory
from utils.helpers import get_dic_from_arrays, log_details, log_exception


class ReadData(AbstractReadDataFactory):
    def __init__(self, auth_token, host_uri) -> None:
        self.path_to_file = None
        self.auth_token = auth_token
        self.host_uri = host_uri
        self.dest_object = None
        super().__init__()
        
    def get_path_to_data(self):
        while not self.path_to_file:
            path = input("Enter the csv file path:")
            if path:
                self.path_to_file = path
            else:
                self.path = None 

    def get_destination_address(self):
        while not self.dest_object:
            dest = input("Enter the destination {} object (Available objects [tickets, organizations, users]):".format(CONNECTOR_NAME))
            if (dest):
                self.dest_object = dest
            else:
                self.dest_object = None

    def format_data(self):
        if not self.path_to_file:
            except_code = 'INVALID FILE PATH'
            except_msg = (
                'You must submit valid file path to the csv file.'
            )
            raise Exception({except_code, except_msg})
        
        file = open(self.path_to_file,'r', newline='')
        csv.register_dialect('unixpwd', delimiter=',', quoting=csv.QUOTE_NONE)
        reader = list(csv.reader(file))
        total_records  = len(reader)
        batch_start = 0

        while batch_start <= total_records:
            data_batch = []
            row_count = 0
            limit = BATCH_LIMIT 
            records_available = total_records - batch_start
            if records_available < BATCH_LIMIT:
                limit = records_available

            headers = reader[0]

            while row_count < limit:
                if batch_start != 0 or row_count != 0:
                    values = reader[row_count + batch_start]
                    json_obj = get_dic_from_arrays(headers, values)
                    
                    data_batch.append(json_obj)
                row_count += 1

            print(data_batch)

            state = self.upload_data(data_batch)

            if state == "completed":
                log_details(CONNECTOR_NAME, "ReadData", "format_data","{0} records uploaded successfully! ".format(batch_start+limit ))
            elif state =="failed":
                log_details(CONNECTOR_NAME, "ReadData", "format_data", "{0} records (from {1} to {2}) failed to upload! ".format(limit, batch_start, batch_start + limit))

            batch_start = batch_start + BATCH_LIMIT

        return data_batch



    def upload_data(self, data):
        upload = UploadData(self.host_uri, self.auth_token, self.dest_object)

        try:
            upload.upload_batch(data)
        except Exception as e:
            log_exception(CONNECTOR_NAME, "ReadData", "format_data", e)
        
        stop_checking_status = False
        while not stop_checking_status:
            try:
                state = upload.check_job_status()
                if state == "completed" or state == "failed" or state == "killed":
                    stop_checking_status = True
                else:
                    sleep(60*3)
            except Exception as e:
                log_exception(CONNECTOR_NAME, "ReadData", "format_data", e)
                sleep(60*2)

        return state