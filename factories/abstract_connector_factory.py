from abc import ABC, abstractmethod

"Abstract factory to create multiple connectors "
class AbstractConnectorFactory(ABC):

    @abstractmethod
    def authentication(self):
        pass

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def upload_data(self):
        pass