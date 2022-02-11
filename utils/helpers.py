import xml.dom.minidom
import base64

def getUniqueElementValueFromXmlString(xmlString, elementName):
       """
       Extracts an element value from an XML string.
       For example, invoking
       getUniqueElementValueFromXmlString(
           '<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>', 'foo')
       should return the value 'bar'.
       """
       xmlStringAsDom = xml.dom.minidom.parseString(xmlString)
       elementsByName = xmlStringAsDom.getElementsByTagName(elementName)
       elementValue = None
       if len(elementsByName) > 0:
           elementValue = (
               elementsByName[0]
               .toxml()
               .replace('<' + elementName + '>', '')
               .replace('</' + elementName + '>', '')
           )
       return elementValue

def get_base64_encoded_string(string_value):
        creds_bytes = string_value.encode("utf-8") 
        encoded_creds = base64.b64encode(creds_bytes)
        return encoded_creds

def get_dic_from_arrays(key_arr, value_arr):
    json_obj = {}
    for index in range(len(value_arr)):  
        json_obj[key_arr[index]] = value_arr[index]
    return json_obj


def log_exception(connector, classname, function_name, exception_detail):
    print("Exception occurred - in {0}/{1} class, inside function {2}, details are \n{3}\n".format(connector, classname, function_name, exception_detail))

def log_details(connector, classname, function_name, output):
    print("Details - In {0}/{1} class, inside function {2}, details are - \n{3}\n".format(connector, classname, function_name, output))