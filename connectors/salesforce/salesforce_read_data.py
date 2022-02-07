
from factories.abstract_read_data_factory import AbstractReadDataFactory
import csv
from utils.csv_adapter import CsvDictsAdapter

class SalesforceReadData(AbstractReadDataFactory):
    def __init__(self) -> None:
        self.path_to_file = None
        super().__init__()
        
    def get_path_to_data(self):
        path = input("Enter the csv file path:")
        if path:
            self.path_to_file = path 
        return super().get_path_to_data()

    def format_data(self):
        if not self.path_to_file:
            except_code = 'INVALID FILE PATH'
            except_msg = (
                'You must submit valid file path to the csv file.'
            )
            raise Exception({except_code, except_msg})
        
        file = open(self.path_to_file,'r', newline='')
        print(file)
        csv.register_dialect('unixpwd', delimiter=',', quoting=csv.QUOTE_NONE)
        reader = csv.reader(file)
        print("🚀 ~ file: salesforce_read_data.py ~ line 9 ~ reader", reader)
        formated_data = ""
        for row in reader:
            print("🚀 ~ file: salesforce_read_data.py ~ line 29 ~ row", row)
            formated_data = """{0} {1} \n""".format(formated_data, ",".join(row)) 

        print("🚀 ~ file: salesforce_read_data.py ~ line 11 ~ formated_data", formated_data)
        return formated_data