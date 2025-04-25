from fatkun import Fatkun


fatkun = Fatkun()
url = 'http://sns-na-i2.xhscdn.com/1040g00831g8rgina1u004b43duem6ilnicrgu98?imageView2/2/w/540/format/heif/q/46;imageMogr2/strip&redImage/frame/0&ap=11&sc=HF_PRV'
fatkun.pre_url_process(url, 'heif')
content = fatkun.get_requests()
file_dir = r'D:\files\example'
fatkun.save_file(content, file_dir)