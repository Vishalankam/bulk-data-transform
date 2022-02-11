import requests

from . import CLIENT_ID, API_VERSION, CONNECTOR_NAME
from factories.abstract_authentication_factory import AbstractAuthenticationFactory
from utils.helpers import getUniqueElementValueFromXmlString

class Authentication(AbstractAuthenticationFactory):

    def __init__(self) -> None:
        self.username = None
        self.password = None
        self.domain = "test"
        self.connector_name = CONNECTOR_NAME
        super().__init__()

    def get_credentials_input(self):
        
        self.username = input("Please enter your {} username:".format(self.connector_name))
        self.password = input("Please enter your {} password and security token at the end of the password:".format(self.connector_name))
        domain_name = input("Please enter your {} domain name:".format(self.connector_name))
        if domain_name:
            self.domain = domain_name


    def authenticate_user(self):
        soap_url = 'https://{domain}.salesforce.com/services/Soap/u/{sf_version}' #Partner WSDL
        # soap_url = 'https://{domain}.salesforce.com/services/Soap/c/{sf_version}' #Enterprise WSDL:
        
        soap_url = soap_url.format(domain=self.domain,
                                   sf_version=API_VERSION)
        # pylint: disable=E0012,deprecated-method
        username = self.username 
        password = self.password
    
        if username is not None and password is not None:
            login_soap_request_body = """<?xml version="1.0" encoding="utf-8" ?>
            <soapenv:Envelope
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:urn="urn:partner.soap.sforce.com">
                <soapenv:Header>
                    <urn:CallOptions>
                        <urn:client>{client_id}</urn:client>
                        <urn:defaultNamespace>sf</urn:defaultNamespace>
                    </urn:CallOptions>
                </soapenv:Header>
                <soapenv:Body>
                    <urn:login>
                        <urn:username>{username}</urn:username>
                        <urn:password>{password}</urn:password>
                    </urn:login>
                </soapenv:Body>
            </soapenv:Envelope>""".format(
                username=username, password=password, client_id=CLIENT_ID)

        else:
            except_code = 'INVALID AUTH'
            except_msg = (
                'You must submit either a Username, Password and Security token for '
                'authentication'
            )
            raise Exception({except_code, except_msg})

        login_soap_request_headers = {
            'content-type': 'text/xml',
            'charset': 'UTF-8',
            'SOAPAction': 'login'
        }

        return self.login(soap_url, login_soap_request_body,
            login_soap_request_headers)


    def login(self, soap_url, request_body, headers):
        response = requests.post(
            soap_url, request_body, headers=headers)
    
        if response.status_code != 200:
            except_code = getUniqueElementValueFromXmlString(
                response.content, 'sf:exceptionCode')
            except_msg = getUniqueElementValueFromXmlString(
                response.content, 'sf:exceptionMessage')
            raise Exception(except_code, except_msg)
    
        session_id = getUniqueElementValueFromXmlString(
            response.content, 'sessionId')
        server_url = getUniqueElementValueFromXmlString(
            response.content, 'serverUrl')
    
        sf_instance = (server_url
                       .replace('http://', '')
                       .replace('https://', '')
                       .split('/')[0]
                       .replace('-api', ''))
    
        return session_id, sf_instance
