import requests
import xmltodict
import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
from secretkeys import SECRETS
django.setup()
from main.models import Product
from datetime import datetime

def parse_product():
    key = SECRETS['API_KEY']
    start = str(datetime.today().strftime('%Y%m%d'))
    end = str(int(start)+10000)
    url1 = 'http://www.kopis.or.kr/openApi/restful/pblprfr?service='+ key +'&stdate='+start+'&eddate='+end+'&rows=100&cpage=1&shcate=AAAA&signgucode=11'
    url2 = 'http://www.kopis.or.kr/openApi/restful/pblprfr?service='+ key +'&stdate='+start+'&eddate='+end+'&rows=100&cpage=1&shcate=AAAB&signgucode=11'
    url3 = 'http://www.kopis.or.kr/openApi/restful/pblprfr?service='+ key +'&stdate='+start+'&eddate='+end+'&rows=100&cpage=1&shcate=AAAA&signgucode=41'
    url4 = 'http://www.kopis.or.kr/openApi/restful/pblprfr?service='+ key +'&stdate='+start+'&eddate='+end+'&rows=100&cpage=1&shcate=AAAB&signgucode=41'

    req1 = requests.get(url1).text
    req2 = requests.get(url2).text
    req3 = requests.get(url3).text
    req4 = requests.get(url4).text
    xmlObject1 = xmltodict.parse(req1)
    xmlObject2 = xmltodict.parse(req2)
    xmlObject3 = xmltodict.parse(req3)
    xmlObject4 = xmltodict.parse(req4)
    data1 = xmlObject1['dbs']['db']
    data2 = xmlObject2['dbs']['db']
    data3 = xmlObject3['dbs']['db']
    data4 = xmlObject4['dbs']['db']
    allData = data1 + data2 + data3 + data4
    return allData

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
## python parserim.py
if __name__=='__main__':
    product_dict = parse_product()
    for i in range(len(product_dict)):
        pdts = Product.objects.filter(pID=product_dict[i]['mt20id'])
        if  not pdts:
            p_data = Product()
            p_data.pID = product_dict[i]['mt20id']
            p_data.title = product_dict[i]['prfnm']
            # p_data.img = product_dict[i]['poster']
            p_data.save()