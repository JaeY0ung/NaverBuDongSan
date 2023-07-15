from crawler import naver_crawler
from FileTransform.fileTransform import csv_to_excel

# 삼성동 = 'https://new.land.naver.com/offices?ms=37.517408,127.047313,15&a=SG:SMS:GJCG:APTHGJ:GM:TJ&e=RETAIL'
신사동 = 'https://new.land.naver.com/offices?ms=37.524142,127.0229,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL'
area = '신사동'
if __name__ == "__main__":
    print("main에서 실행")
    naver_crawler(신사동)
    csv_to_excel(area)