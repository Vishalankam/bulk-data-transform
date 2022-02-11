from connectors.salesforce.connector import Connector as SalesforceConnector
from connectors.zendesk.connector import Connector as ZendeskConnector



def read_connector():
    connectorDetails ={
        "salesforce": SalesforceConnector(),
        "zendesk": ZendeskConnector()
    }

    while True:
        print("Welcome to *Bulk-data-transfer*")
        selectedConnector = input("Select the connector to transfer the data to...(Available Connectors: {})".format(connectorDetails.keys()))
        if selectedConnector in connectorDetails:
            return connectorDetails[selectedConnector] 

class main():
    connector = read_connector()
    connector.authentication()
    connector.read_and_upload_data()
    # connector.upload_data()
    
            
            