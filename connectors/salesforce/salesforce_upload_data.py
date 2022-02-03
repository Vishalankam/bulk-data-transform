
from factories.abstract_upload_data_factory import AbstractUploadDataFactory


class SalesforceUploadData(AbstractUploadDataFactory):
    def upload_data(self):
        return super().upload_data()