import os
import _read_config_text
'''      
#The environ_name can be either production, development, testing, or a custom
#set of URLs that can be adjust in the human readable pyGDP_URLs.txt file.
#The .txt path is currently set to point wherever this script is executed from.

URL_file = os.path.join(os.path.split(_read_config_text.__file__)[0], 'pyGDP_URLs.txt')
environ_name = 'production'

#URLs are read out from the dictionary created from the .txt file.
#Here they are prepared to be sent to pyGDP.
class pyGDP_URLs():
    def __init__():
        self.URL_file = pyGDP_Namespaces.URL_file
    def get_URLs(URL_file):
        urls = _read_config_text.get_urls(URL_file, environ_name)
        return urls    
    urls=get_URLs(URL_file)
    WFS_URL    = urls['WFS_URL']
    upload_URL = urls['upload_URL']
    WPS_URL    = urls['WPS_URL']
    WPS_Service= urls['WPS_Service']
    CSWURL     = urls['CSWURL']
'''

#The environ_name can be either production, development, testing, or a custom
#set of URLs that can be adjust in the human readable pyGDP_URLs.txt file.
#The .txt path is currently set to point wherever this script is executed from.

URL_file = os.path.join(os.path.split(_read_config_text.__file__)[0], 'pyGDP_URLs.txt')
environ_name = 'production'

#URLs are read out from the dictionary created from the .txt file.
#Here they are prepared to be sent to pyGDP.e
def get_URLs():
    urls = _read_config_text.get_urls(URL_file, environ_name)
    return urls    
urls=get_URLs()
WFS_URL    = urls['WFS_URL']
upload_URL = urls['upload_URL']
WPS_URL    = urls['WPS_URL']
WPS_Service= urls['WPS_Service']
CSWURL     = urls['CSWURL']
