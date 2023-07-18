from crawler_sample import naver_crawler
from FileTransform.fileTransform import csv_to_excel

# 신사동 = 'https://new.land.naver.com/offices?ms=37.524142,127.0229,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL'

# 도산공원이 가운데

if __name__ == "__main__":
    print("main에서 실행")
    naver_crawler('https://new.land.naver.com/offices?ms=37.5245000,127.0353000,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL')
    csv_to_excel('신사동')