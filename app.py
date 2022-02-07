from abc import ABC, abstractmethod
from selectors import SelectSelector

from connectors.salesforce.salesforce_connector import SalesforceConnector
from connectors.zendesk.zendesk_connector import ZendeskConnector


def read_connector():
    connectorDetails ={
        "salesforce": SalesforceConnector(),
        "zendesk": ZendeskConnector()
    }

    while True:
        print("Welcome to *Bulk-data-transfer*")
        selectedConnector = input("Select the connector to transfer the data to..[Available Connectors: salesforce, zendesk]")
        if selectedConnector in connectorDetails:
            return connectorDetails[selectedConnector] 

class main():
    connector = read_connector()
    connector.authentication()
    connector.read_data()
    connector.upload_data()
    
            
            