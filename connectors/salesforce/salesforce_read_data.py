
from factories.abstract_read_data_factory import AbstractReadDataFactory


class SalesforceReadData(AbstractReadDataFactory):
    def get_path_to_data(self):
        return super().get_path_to_data()