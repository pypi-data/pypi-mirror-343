from abc import abstractmethod
from urllib.parse import urlparse
from url_lib import url_gen,content_gen


class Converter:
    def __init__(self):
        self.head = {}
        self.url = ''
        self.file_type = ''
        self.file_name = ''


    @abstractmethod
    def url_key_gen(self,url):
        pass
    @abstractmethod
    def gen_file_name(self,url):
        pass

    def pre_url_process(self,url,file_type):
        parsed = urlparse(url)
        hostname = parsed.hostname
        if 'xhscdn' in hostname:
            self.url,self.file_type = url_gen(url)
        else:
            self.url = url
        self.file_name = self.gen_file_name(url)

    def file_convert(self,content,url,file_type):
        content,url = content_gen(content,url,file_type)
        return content,url


