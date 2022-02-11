from abc import ABC, abstractmethod

"Abstract factory to create multiple connectors "
class AbstractConnectorFactory(ABC):

    @abstractmethod
    def authentication(self):
        pass

    @abstractmethod
    def read_and_upload_data(self):
        pass
