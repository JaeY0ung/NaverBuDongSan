from flask import Flask,render_template
from FileTransform.fileTransform import load_csv

app = Flask(__name__)

@app.route('/')
def home():
    datas = load_csv('./csv/신사동.csv')

    title1 = '도산공원에서 떨어진 distance별 가격'
    distance      = ['0~100m', '100m~200m', '200m~300m', '300m~400m', '400m~500m']
    sum_deposit = [0,0,0,0,0]
    sum_monthly  = [0,0,0,0,0]
    num      = [0,0,0,0,0]
    for data in datas:
        # deposit, monthly int로 형변환
        strdeposit, strmonthly = data['가격'].split('/')[0], data['가격'].split('/')[1]
        if '억' in strdeposit:
            li_deposit = strdeposit.split('억')
            if li_deposit[1]:
                deposit = int(li_deposit[0])*10000 + int(li_deposit[1].replace(',', ''))
            else:
                deposit = int(li_deposit[0])*10000
        else:
            deposit = int(strdeposit.replace(',', ''))

        monthly = int(strmonthly.replace(' ', '').replace(',', ''))
        if len(data['월관리비']) > 2:
            monthly += float(data['월관리비'][:-2])

        # if문 반복을 줄이기 위해 for문으로 해결
        for i in range(5):
            if 100*i <= float(data['거리']) < 100*(i+1):
                sum_deposit[i] += deposit
                sum_monthly[i] += monthly
                num[i] += 1

    # 차트를 위한 리스트
    avg_deposit_for_chart = [0,0,0,0,0]
    avg_monthly_for_chart = [0,0,0,0,0]
    for i in range(len(sum_deposit)):
        deposit = sum_deposit[i]
        monthly = sum_monthly[i]
        if deposit:
            avg_deposit_for_chart[i] = int(deposit / num[i])
            avg_monthly_for_chart[i] = int(monthly / num[i])
        
    # 후 가공
    avg_deposit = []
    for i in range(len(sum_deposit)):
        try:
            avg = str(int(sum_deposit[i]/num[i]))
        except:
            avg = '0'
        # 천만원 -> 억으로 나눠 보기 편하게 하기 (ex. 10000, 9400 등)
        if len(avg) >= 5:
            avg = str(avg[:-4]) + '억' + str(int(str(avg)[-4:]))
        avg += '만원'
        avg_deposit.append(avg)
    
    avg_monthly = []
    for i in range(len(sum_monthly)):
        try:
            avg = str(int(sum_monthly[i]/num[i]))
        except:
            avg = '0'
        avg += '만원'
        avg_monthly.append(avg)

    print(f'avg_deposit_for_chart: {avg_deposit_for_chart}')
    print(f'avg_monthly_for_chart: {avg_monthly_for_chart}')

    return render_template('home.html', datas = datas, 
                           title1 = title1 , distance = distance, avg_deposit = avg_deposit, avg_monthly = avg_monthly,
                           num = num, len1 = len(avg_monthly), avg_deposit_for_chart = avg_deposit_for_chart,
                           avg_monthly_for_chart = avg_monthly_for_chart)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')