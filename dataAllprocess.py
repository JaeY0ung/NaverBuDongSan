from Budongsan_crwaler.crawler_sample import naver_crawler
from FileTransform.fileTransform import csv_to_excel

# 크롤링하여 데이터 엑셀과 csv로 저장

# 신사동 = 'https://new.land.naver.com/offices?ms=37.524142,127.0229,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL'
# 도산공원이 가운데
if __name__ == "__main__":
    print("main에서 실행")
    try:
        naver_crawler('https://new.land.naver.com/offices?ms=37.5245000,127.0353000,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL')
        print('크롤링 성공!')
    except:
        print('크롤링 실패일수도?')
    csv_to_excel('신사동')
    print('csv -> excel 파일 생성!')