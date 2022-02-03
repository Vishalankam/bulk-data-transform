

from factories.abstract_authentication_factory import AbstractAuthenticationFactory


class SalesforceAuthentication(AbstractAuthenticationFactory):
    def get_auth_token(self):
        print("gettingAuthToken")
        return super().get_auth_token()
    
    def get_method_of_authentication(self):
        return super().get_method_of_authentication() 

    def validate(self):
        return super().validate()