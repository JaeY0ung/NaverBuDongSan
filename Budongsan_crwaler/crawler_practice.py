from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# 페이지의 맨 밑까지 스크롤 (맥 + 34인치 모니터 기준/ 한페이지에 55개 상점 정보)
def scroll_down(crawler):
    for _ in range(10):
        body = crawler.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    return

# 내 방 네트워크 환경에서 맥북 에어를 이용하여 합정 5페이지 크롤링에 걸린 시간: 12분
def naver_crawler(url):
    null = "정보 없음"

    # chrome_crawler 설정
    chrome_options = Options() # 브라우저 꺼짐 방지
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #불필요한 에러 메세지 삭제
    service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service = service, options = chrome_options)

    # 크롤링할 url로 이동
    crawler.get(url) # 웹페이지 해당 주소 이동
    crawler.implicitly_wait(5) # 로딩이 끝날동안 기다리기

    # 크롤링한 상점들의 정보를 담는 리스트
    crawl_data = []

    # 스크롤 가능하도록 body 중 아무 동작 없는 곳 클릭
    crawler.find_element(By.CLASS_NAME, "list_contents").click()
    crawler.implicitly_wait(2)

    # 페이지의 맨 밑까지 스크롤
    # scroll_down(crawler)

    fieldnames = ['name', 'type', 'price', '소재지', '매물특징', '계약/전용면적', '해당층/총층', '융자금', 
                 '월관리비', '방향', '입주가능일', '주차가능여부', '총사무실수', '총주차대수', 
                 '난방(방식/연료)', '사용승인일', '건축물 용도', '매물번호', '매물설명', '중개사', 
                 '중개보수', '상한요율', '주구조', '현재업종', '추천업종', '용도지역', '권리금', '사용검사일']
    # 사무실 프레임들 가져오기
    samusils = crawler.find_elements(By.CLASS_NAME, 'item_link')

    # 제일 안쪽의 map : #article_map > div:nth-child(1) > div
    # map_cluster--mix is-outside : 내가 선택한 동 밖
    # map_cluster--mix is-length2 : 내가 선택한 동의 원크기가 2인 것(작은 것)
    # map_cluster--mix is-length3 : 내가 선택한 동의 원크기가 3인 것(큰 것)


    # 가게들 정보 크롤링 시작
    for samusil in samusils:
        samusil_dict = dict()
        for fieldname in fieldnames:
            samusil_dict[fieldname] = null

        samusil.click()
        crawler.implicitly_wait(1)

        # 이름
        try:
            name = crawler.find_elements(By.CLASS_NAME, 'info_title_name')[1].text
        except:
            name = null
        print(f'name: {name}')
        samusil_dict['name'] = name
        crawler.implicitly_wait(2)

        # 종류
        try:
            type = crawler.find_element(By.CLASS_NAME, 'type').text
        except:
            type = null
        print(f'type: {type}')
        samusil_dict['type'] = type
        crawler.implicitly_wait(2)

        # 가격
        try:
            price = crawler.find_element(By.CLASS_NAME, 'price').text
        except:
            price = null
        print(f'price: {price}')
        samusil_dict['price'] = price
        crawler.implicitly_wait(2)

        # 중개보수까지의 테이블 데이터
        infos = crawler.find_elements(By.CLASS_NAME, 'info_table_item')
        for row in infos:
            data_keys = row.find_elements(By.CLASS_NAME, 'table_th')
            data_values = row.find_elements(By.CLASS_NAME, 'table_td')

            if len(data_keys) == 0: # 상한요율만 table_th 속성 없음
                samusil_dict['상한요율'] = data_values[0].text[4:]
                print(f'상한요율: {data_values[0].text[4:]}')
            elif data_keys[0].text == '매물설명':
                data_key = data_keys[0].text
                data_value = data_values[0].text
                data_value = data_value.replace('\n','')
                samusil_dict[data_key] = data_value
                print(f'{data_key}: {data_value}')
            else:
                for j in range(len(data_keys)):
                    data_key = data_keys[j].text
                    data_value = data_values[j].text
                    samusil_dict[data_key] = data_value
                    print(f'{data_key}: {data_value}')

        crawler.implicitly_wait(2)
        crawl_data.append(samusil_dict)
        print('--------------------------------------------------------------------')

    crawler.quit()

    with open(f'./csv/신사동.csv', 'w', encoding= 'UTF-8') as file:
        csvWriter = csv.DictWriter(file, fieldnames=fieldnames)
        csvWriter.writeheader()
        for row in crawl_data:
            csvWriter.writerow(row)