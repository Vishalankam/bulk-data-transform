"Concrete product for salesforce connector"

from connectors.salesforce.salesforce_authentication import SalesforceAuthentication
from factories.abstract_connector_factory import AbstractConnectorFactory


class SalesforceConnector(AbstractConnectorFactory):
    def authentication(self):
        auth = SalesforceAuthentication()
        auth.get_auth_token()
        return super().authentication()

    def read_data(self):
        return super().read_data()

    def upload_data(self):
        return super().upload_data()