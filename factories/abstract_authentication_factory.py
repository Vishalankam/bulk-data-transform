from abc import ABC, abstractmethod

"Abstract factory to create authentication classes for multiple connectors "
class AbstractAuthenticationFactory(ABC):

    @abstractmethod
    def get_method_of_authentication(self):
        pass

    @abstractmethod
    def get_auth_token(self):
        pass

    @abstractmethod
    def validate(self):
        pass