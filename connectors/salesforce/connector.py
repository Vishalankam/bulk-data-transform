from connectors.salesforce import CONNECTOR_NAME
from connectors.salesforce.authentication import Authentication
from connectors.salesforce.read_data import ReadData
from factories.abstract_connector_factory import AbstractConnectorFactory
from utils.helpers import log_details, log_exception

"Concrete product for salesforce connector"

class Connector(AbstractConnectorFactory):
    def __init__(self) -> None:
        super().__init__()
        self.auth_token = None
        self.host_uri = None
        self.user_authenticated = False

    def authentication(self):
        auth = Authentication()
        while not self.user_authenticated:
            try:
               auth.get_credentials_input()
               self.auth_token, self.host_uri = auth.authenticate_user()
               self.user_authenticated = True
               log_details(CONNECTOR_NAME, "Connector", "authentication", "User logged in successfully..!")
            except Exception as e:
                self.user_authenticated = False
                log_exception(CONNECTOR_NAME, "Connector", "authentication", e)
                log_details(CONNECTOR_NAME, "Connector", "authentication","Login failed: You need to login again.")

        print(self.auth_token, self.host_uri)

    def read_and_upload_data(self):
        read_data = ReadData(self.auth_token, self.host_uri)

        try:
            read_data.get_path_to_data()
            read_data.get_destination_address()
            read_data.format_data()
        except Exception as e:
            log_exception(CONNECTOR_NAME, "Connector", "read_and_upload_data", e)

   