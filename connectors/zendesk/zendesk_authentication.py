

from factories.abstract_authentication_factory import AbstractAuthenticationFactory


class ZendeskAuthentication(AbstractAuthenticationFactory):
    def get_auth_token(self):
        return super().get_auth_token()
    
    def get_method_of_authentication(self):
        return super().get_method_of_authentication() 
