from abc import ABC, abstractmethod

"Abstract factory to create authentication classes for multiple connectors "
class AbstractAuthenticationFactory(ABC):

    @abstractmethod
    def take_credentials_input(self):
        pass

    @abstractmethod
    def authenticate_user(self):
        pass
