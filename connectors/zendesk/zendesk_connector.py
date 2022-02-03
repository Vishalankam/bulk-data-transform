"Concrete product for salesforce connector"

from factories.abstract_connector_factory import AbstractConnectorFactory


class ZendeskConnector(AbstractConnectorFactory):
    def authentication(self):
        return super().authentication()

    def read_data(self):
        return super().read_data()

    def upload_data(self):
        return super().upload_data()