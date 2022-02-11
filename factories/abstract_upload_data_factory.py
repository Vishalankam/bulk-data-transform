from abc import ABC, abstractmethod

"Abstract factory to create classes for uploading data for multiple connectors "
class AbstractUploadDataFactory(ABC):

    @abstractmethod
    def upload_batch(self):
        pass

    @abstractmethod
    def check_job_status(self):
        pass
