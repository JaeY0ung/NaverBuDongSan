from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
from calculator.cal_distance import distance

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

    # https://stackoverflow.com/questions/71885891/urllib3-exceptions-maxretryerror-httpconnectionpoolhost-localhost-port-5958
    # To evade the detection as a bot -> 여전히 같은 증상
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #불필요한 에러 메세지 삭제
    service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 최신 버전 자동 설치 후 서비스 만들기
    crawler = webdriver.Chrome(service = service, options = chrome_options)

    # 크롤링할 url로 이동
    crawler.get(url) # 웹페이지 해당 주소 이동
    time.sleep(5)
    crawler.maximize_window()
    time.sleep(5) # 로딩이 끝날동안 기다리기 ( crawler.implicitly_wait(5)은 갑자기 안됨/ 바로 나온줄 알고 실행돼서 그런 것 같음)

    circles = crawler.find_elements(By.CSS_SELECTOR, '#article_map > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div > div:nth-child(1) > a')
    print(f'예상 총 탐색 circle 수: {len(circles)}')

    fieldnames = ['매물종류', '거래방식', '가격', '위치', '거리', '소재지', '매물특징', '계약/전용면적', '해당층/총층', '융자금', 
                '월관리비', '방향', '입주가능일', '주차가능여부', '총사무실수', '총주차대수', 
                '난방(방식/연료)', '사용승인일', '건축물 용도', '매물번호', '매물설명', '중개사', 
                '중개보수', '상한요율']
    
    file = open(f'./csv/신사동.csv', 'w', encoding= 'UTF-8')
    csvWriter = csv.DictWriter(file, fieldnames=fieldnames)
    csvWriter.writeheader()

    num_circle, num_proper_circle, num_circle_empty, num_circle_error = 0, 0, 0, 0
    num_samusil = 0
    for circle in circles:
        # 원 안에 있는 samusil 수 초기화
        num_samusil_in_this_circle = 0
        num_circle += 1
        print(f'지금까지 탐색한 원의 수: {num_circle}/{len(circles)}')
        try:
            # print(f'circle.text: {circle.text}')
            if len(circle.text) > 4: # ex) 174\n개 매물
                num_in_circle = int(circle.text[:-4].strip('\n'))
            else: # ex) 174
                num_in_circle = int(circle.text.strip('\n'))
            num_proper_circle += 1
        except:
            if circle.text == '':
                num_circle_empty += 1
            else:
                num_circle_error += 1
                # print(f'[ERROR] circle.text: {circle.text}') 디버깅용: 0이 나와야 함
            continue # 그 circle 패스
        # 화면상 위치 검색
        button_style = circle.get_attribute('style') # ex) width: 48.1483px; height: 48.1483px; top: -9357.65px; left: -3266.62px;
        style = button_style.replace(';','').replace(': ',':').split(' ')
        top = float(style[2][4:][:-2])
        left = float(style[3][5:][:-2])
        loc_circle = (top, left) # top, left 정보를 소수로 가져오기 (창 크기 바꾼다고 달라지지 않음/ 화면을 드래그해서 시점을 바꾸면 바뀜)
        dis = distance(loc_circle) # dis output 단위: m
        # circle과 도산공원과 800m 이상 떨어져 있으면 일단 한번 거르기
        if dis > 600:
            print(f'원의 거리: {dis}m -> 제외')
            continue  # 건너뛰기
        print(f'원의 거리: {dis}m -> 탐색')

        # 원 버튼(a 태그) 클릭 (circle.click() : 실패)
        circle.send_keys('\n') # 성공! 출처: https://blog.naver.com/PostView.nhn?blogId=kiddwannabe&logNo=221430636045

        # 스크롤 가능하도록 body 중 아무 동작 없는 곳 클릭
        crawler.find_element(By.CLASS_NAME, "list_contents").click()
        crawler.implicitly_wait(2)

        # 페이지의 맨 밑까지 스크롤
        # scroll_down(crawler)

        # 사무실들 가져오기
        samusils = crawler.find_elements(By.CLASS_NAME, 'item_link')
        crawler.implicitly_wait(2)

        # 가게들 정보 크롤링 시작
        for samusil in samusils:
            num_samusil_in_this_circle += 1
            num_samusil += 1
            # 초기화
            samusil_dict = dict()
            for fieldname in fieldnames:
                samusil_dict[fieldname] = null

            # 사무실(samusil) 위에 커서 대고 그때 생기는 핀 위치 (클래스네임: btn_current_position) 가져오기
            ActionChains(crawler).move_to_element(samusil).perform()
            btn_current_position = crawler.find_element(By.CLASS_NAME, 'btn_current_position')
            crawler.implicitly_wait(3)
            current_position = btn_current_position.get_attribute('style')
            crawler.implicitly_wait(3)
            position = current_position.replace('left: ','').replace('top: ','').replace('px','').strip(';').split(';')
            left = float(position[0])
            top = float(position[1])
            dis = distance((top, left))
            if dis > 500:
                print(f'매물의 거리: {dis}m -> 제외')
                continue  # 건너뛰기
            print(f'매물의 거리: {dis}m -> 추가')

            # 좌표
            samusil_dict['위치'] = (top, left)
            # 중심(도산공원)과의 거리
            samusil_dict['거리'] = dis
        
            # 사무실 이름 클릭하여 세부 정보 확인
            samusil.click()
            crawler.implicitly_wait(3)

            # 이름
            try:
                매물종류 = crawler.find_elements(By.CLASS_NAME, 'info_title_name')[1].text
            except:
                매물종류 = null
            samusil_dict['매물종류'] = 매물종류
            # print(f'매물종류: {매물종류}')
            crawler.implicitly_wait(3)

            # 종류
            try:
                거래방식 = samusil.find_element(By.CLASS_NAME, 'type').text
            except:
                거래방식 = null
            samusil_dict['거래방식'] = 거래방식
            # print(f'거래방식: {거래방식}')
            crawler.implicitly_wait(3)

            # 가격
            try:
                가격 = samusil.find_element(By.CLASS_NAME, 'price').text
            except:
                가격 = null
            samusil_dict['가격'] = 가격
            print(f'매물의 가격: {가격}')
            crawler.implicitly_wait(3)

            # 중개보수까지의 테이블 데이터 수집
            infos = crawler.find_elements(By.CLASS_NAME, 'info_table_item')
            for row in infos:
                data_keys = row.find_elements(By.CLASS_NAME, 'table_th')
                data_values = row.find_elements(By.CLASS_NAME, 'table_td')

                if len(data_keys) == 0: # 상한요율만 table_th 속성 없음
                    samusil_dict['상한요율'] = data_values[0].text[4:]
                    # print(f'상한요율: {data_values[0].text[4:]}')
                elif data_keys[0].text == '매물설명':
                    data_key = data_keys[0].text
                    data_value_before = data_values[0].text
                    data_value = '&'.join(data_value_before.splitlines())
                    samusil_dict[data_key] = data_value
                    # print(f'{data_key}: {data_value}')
                else:
                    for j in range(len(data_keys)):
                        data_key, data_value = data_keys[j].text, data_values[j].text
                        if data_key in fieldnames:
                            samusil_dict[data_key] = data_value
                            # print(f'{data_key}: {data_value}')

            crawler.implicitly_wait(2)
            csvWriter.writerow(samusil_dict)
            print(f'현재까지 크롤링한 전체 매물 수: {num_samusil}, 이 circle에서 크롤링한 매물 수(20개마다 초기화): {num_samusil_in_this_circle}')
            print('---------------------------------------------------------------------------------')
            # 샘플을 위해 각 지역별 5개씩만 가져오기
            if num_samusil_in_this_circle == 20:
                break
            
    print(f'처음 탐색 circle 수: {len(circles)}')
    print(f'총 circle 수: {num_circle:05d} 정상 circle 수:{num_proper_circle:02d},  에러 circle 수: {num_circle_error:02d}번,  빈 circle 수: {num_circle_empty:02d}')
    
    file.close() # 파일 닫기
    crawler.close()