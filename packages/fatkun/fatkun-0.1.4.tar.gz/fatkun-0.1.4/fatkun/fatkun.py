import hashlib
import os.path

import requests
from fatkun.converter import Converter


class Fatkun(Converter):
    def __init__(self):
        super().__init__()
        self.head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}


    def url_key_gen(self,url):
        return super().url_key_gen(url)

    def gen_file_name(self,url):
        file_name = hashlib.md5(url.encode('utf8')).hexdigest()
        if 'xhscdn' in url:
            file_name = file_name + self.file_type
        elif 'xiaohongshu' in url:
            file_name = file_name + self.file_type
        else:
            file_name = file_name + self.file_type
        return file_name

    def get_requests(self):
        try:
            res = requests.get(url = self.url,headers=self.head)
            st_code = str(res.status_code)
            if st_code.startswith('2'):
                content = res.content
                return content
            else:
                return None
        except Exception as e:
            print('except:',e.args)
            return None

    def save_file(self,content,file_dir):
        content,url = self.file_convert(content,self.url,self.file_type)
        if content:
            file_pth = os.path.join(file_dir,self.file_name)
            print('文件保存路径：',file_pth)
            f = open(file_pth,'wb')
            f.write(content)
            f.close()
        else:
            print('内容为空未保存')



