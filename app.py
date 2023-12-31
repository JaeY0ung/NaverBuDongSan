from flask import Flask,render_template
from FileTransform.fileTransform import load_csv

app = Flask(__name__)

@app.route('/')
def home():
    datas = load_csv('./csv/신사동.csv')
    null = '정보 없음'
    title1 = '도산공원에서 떨어진 distance별 가격'
    distance    = ['0~100m', '100m~200m', '200m~300m', '300m~400m', '400m~500m']
    sum_deposit = [0,0,0,0,0]
    sum_monthly = [0,0,0,0,0]
    sum_maintenance = [0,0,0,0,0]
    num         = [0,0,0,0,0]
    for data in datas:
        # 면적, 평수 -> float으로 형변환하여 처리
        if null in data['계약/전용면적']:
            # 정보가 없으면 필요없는 매물이므로 건너뛴다.
            print('평수 정보가 없습니다.')
            continue
        else:
            면적 = data['계약/전용면적'].replace('(', '/').replace(')', '').replace('㎡', '').split('/')
        계약면적 = float(면적[0])
        전용면적 = float(면적[1])
        계약평수 = 계약면적 / 3.3
        전용평수 = 전용면적 / 3.3

        strdeposit, strmonthly = data['가격'].split('/')[0], data['가격'].split('/')[1]

        # 보증금(deposit) -> int로 형변환하여 처리
        if '억' in strdeposit:
            li_deposit = strdeposit.split('억')
            if li_deposit[1]:
                deposit = int(li_deposit[0])*10000 + int(li_deposit[1].replace(',', ''))
            else:
                deposit = int(li_deposit[0])*10000
        else:
            deposit = int(strdeposit.replace(',', ''))

        # 월세(monthly) -> int로 형변환하여 처리
        strmonthly = strmonthly.replace(' ', '').replace(',', '')
        if len(strmonthly) > 4 :
            monthly = int(strmonthly.split('억')[0])*10000 + int(strmonthly.split('억')[0])
        else:
            monthly = int(strmonthly)

        if '만원' in data['월관리비']:
            월관리비 = float(data['월관리비'][:-2])
        elif '원' in data['월관리비']:
            월관리비 = float(data['월관리비'][:-1])
        else:
            월관리비 = 0

        # if문 반복을 줄이기 위해 for문으로 해결
        # 각 거리별 매물수/ 각 거리별 평당 보증금 총합/ 각 거리별 평당 월세 총합
        for i in range(5):
            if 100 * i <= float(data['거리']) < 100 * (i+1):
                sum_deposit[i] += deposit / 계약평수
                sum_monthly[i] += monthly / 계약평수
                sum_maintenance[i] += 월관리비 / 계약평수
                num[i] += 1

    # 차트를 위한 리스트
    avg_deposit_for_chart, avg_monthly_for_chart = [0,0,0,0,0], [0,0,0,0,0]
    # 평균 가격(보증금, 월세, 월관리비) 계산
    for i in range(len(sum_deposit)):
        deposit = sum_deposit[i]
        monthly = sum_monthly[i]
        if deposit:
            avg_deposit_for_chart[i] = int(deposit / num[i])
            avg_monthly_for_chart[i] = int(monthly / num[i])
    
    # 데이터 보기 좋게 가공 (테이블 용)
    avg_deposit, avg_monthly, avg_maintenance = [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]
    for i in range(len(sum_deposit)):
        try:
            avg_d = str(int(sum_deposit[i] / num[i]))
        except:
            avg_d = '0'
        # 천만원 -> 억으로 나눠 보기 편하게 하기 (ex. 10000, 9400 등)
        if len(avg_d) >= 5:
            avg_d = str(avg_d[:-4]) + '억' + str(int(str(avg_d)[-4:]))
        avg_d += '만원'
        avg_deposit[i] = avg_d

        try:
            avg_m = str(int(sum_monthly[i] / num[i]))
        except:
            avg_m = '0'
        avg_m += '만원'
        avg_monthly[i] = avg_m

        try:
            avg_main = str(round(float(sum_maintenance[i] / num[i]), 3))
        except:
            avg_main = '0'
        avg_main += '만원'
        avg_maintenance[i] = avg_main


    print(f'avg_deposit_for_chart: {avg_deposit_for_chart}')
    print(f'avg_monthly_for_chart: {avg_monthly_for_chart}')
    print(f'avg_maintenance: {avg_maintenance}')

    return render_template('home.html', datas = datas, 
                           title1 = title1 , distance = distance, avg_deposit = avg_deposit, avg_monthly = avg_monthly,
                           num = num, len1 = len(avg_monthly), avg_deposit_for_chart = avg_deposit_for_chart,
                           avg_monthly_for_chart = avg_monthly_for_chart, avg_maintenance = avg_maintenance)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')