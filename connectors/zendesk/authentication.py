from . import CONNECTOR_NAME
from factories.abstract_authentication_factory import AbstractAuthenticationFactory
from utils.helpers import  get_base64_encoded_string

class Authentication(AbstractAuthenticationFactory):

    def __init__(self) -> None:
        self.username = None
        self.password = None  #"Q7UTIeeGMVuLi582lutXtYqsJsXURUyRLS4mD4zE"
        self.domain = None
        self.connector_name = CONNECTOR_NAME
        super().__init__()

    def get_credentials_input(self):
        
        print("Note: If you have API token - then add '/token' after username (eg: joy@abc.com/token) and paste your token as password")
        self.username = input("Please enter your {} username:".format(self.connector_name))
        self.password = input("Please enter your {} password:".format(self.connector_name))
        domain_name = input("Please enter your {} domain name:".format(self.connector_name))
        if domain_name:
            self.domain = domain_name


    def authenticate_user(self):
        host_uri = "https://{0}.zendesk.com/".format(self.domain)
        username = self.username 
        password = self.password
        # token = "Q7UTIeeGMVuLi582lutXtYqsJsXURUyRLS4mD4zE"
    
        if username is not None and password is not None:
            encoded_creds = get_base64_encoded_string("{0}:{1}".format(username, password))
            auth_token = "{}".format(encoded_creds).split("'")[1]

        else:
            except_code = 'INVALID AUTH'
            except_msg = (
                'You must submit either a Username, Password or API token for authentication'
            )
            raise Exception({except_code, except_msg})

        return auth_token, host_uri


