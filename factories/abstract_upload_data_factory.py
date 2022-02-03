from abc import ABC, abstractmethod

"Abstract factory to create classes for uploading data for multiple connectors "
class AbstractUploadDataFactory(ABC):

    @abstractmethod
    def upload_data(self):
        pass