"Concrete product for salesforce connector"

from asyncore import read
from time import sleep
from connectors.salesforce.salesforce_authentication import SalesforceAuthentication
from connectors.salesforce.salesforce_read_data import SalesforceReadData
from connectors.salesforce.salesforce_upload_data import SalesforceUploadData
from factories.abstract_connector_factory import AbstractConnectorFactory


class SalesforceConnector(AbstractConnectorFactory):
    def __init__(self) -> None:
        self.session_id = None
        self.host_uri = None
        self.data =None
        super().__init__()

    def authentication(self):
        auth = SalesforceAuthentication()
        auth.take_credentials_input()
        self.session_id, self.host_uri = auth.authenticate_user()
        print(self.session_id, self.host_uri)
        return super().authentication()

    def read_data(self):
        read_data = SalesforceReadData()
        read_data.get_path_to_data()
        self.data = read_data.format_data()
        return super().read_data()

    def upload_data(self):
        upload = SalesforceUploadData(self.host_uri, self.session_id)
        upload.take_destination_address()
        upload.create_job()
        # no_more_batches_to_upload = False

        # while not no_more_batches_to_upload:
        status = upload.upload_batch(self.data)
        # if not status >=400:
            # upload_another_batch = input("Do you want to upload another batch? (type yes or no)")
            # if upload_another_batch == 'yes':
                # self.read_data()
            # else:
                # no_more_batches_to_upload = True
        upload.upload_data()


        flag = True
        while flag:
            state = upload.check_job_status()
            if state == "JobComplete" or state == "Failed":
                flag = False
            sleep(60)

        return super().upload_data()