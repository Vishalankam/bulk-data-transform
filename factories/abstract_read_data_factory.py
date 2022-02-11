from abc import ABC, abstractmethod

"Abstract factory to create classes for reading data for multiple connectors "
class AbstractReadDataFactory(ABC):

    @abstractmethod
    def get_path_to_data(self):
        pass

    @abstractmethod
    def format_data(self):
        pass
    
    @abstractmethod
    def get_destination_address(self):
        pass