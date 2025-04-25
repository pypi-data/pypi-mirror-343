from ..constants.HEADER_KEYS import HEADER_KEYS
from ..constants.HEADER_KEYS_ALIASES import HEADER_KEYS_ALIASES

class Headers():
    @staticmethod
    def __init__(self):
        self.headers_dict = {}
        headers_dict = {}
        for header_key, header_key_alias in zip(HEADER_KEYS, HEADER_KEYS_ALIASES):
            headers_dict[header_key] = [0, 1, 2, 3, 4]
            self.headers_dict[header_key_alias] = headers_dict[header_key]

    @staticmethod
    def getAllHeaders(self):
        return self.headers_dict
    
    @staticmethod
    def getHeadersByIndex(self, index):
        # retorna dicionário {'ep': 10, 'tracf': 40}
        single_trace_headers_dict = {}
        for key, value in self.headers_dict.items():
            single_trace_headers_dict[key] = value[index]
        return single_trace_headers_dict
    
    @staticmethod
    def getHeadersByName(self, header_name):

        # retorna lista [30, 40, 50, 60, 70]
        return self.headers_dict[header_name]
