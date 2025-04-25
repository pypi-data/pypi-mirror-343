import requests


def requests_linker(url,head):
    try:
        res = requests.get(url,headers=head)
        st_code = str(res.status_code)
        if st_code.startswith('2'):
            content = res.content
            return content
        else:
            return None
    except Exception as e:
        print('except:',e.args)
        return None

