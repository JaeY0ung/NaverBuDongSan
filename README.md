# Naver부동산   


## < 고객 요구 사항 >   

신사동 의 도산공원 주변 500m 주변(논현동, 청담동 일부 포함할 것으로 예상)의 건물들의 (층 별) 가격 평균 보증금, 월세 가격을 알고 싶다.   


## 해결 과정 계획(요약)
1. 네이버부동산 -> 강남구 클릭 -> 신사동 클릭 -> 상가.업무.공장.토지 클릭 -> 거래방식: 월세 클릭    
DEFAULT URL: https://new.land.naver.com/offices?ms=37.524142,127.0229,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL   

2. 도산공원 중심으로 지도 포커스 (왼쪽으로 드래그)   
https://new.land.naver.com/offices?ms=37.5240909,127.0321912,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL   
https://new.land.naver.com/offices?ms=37.5240484,127.0316118,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL   



## <참고>   
도산공원의 구글지도 좌표 : 37.5245, 127.0353 -> 위의 좌표와 일치한다. 이거 사용할 것   

## <분석>
https://new.land.naver.com/offices?ms={위도},{경도},{줌 횟수}&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b={거래방식}&e=RETAIL   
## 거래 방식
A1: 매매  B1: 전세  B2: 월세  B3: 단기임대 / 전체: b= 이 없음  (여러개 입력시 B1:B2 이렇게 들어감)   


## < 실제 실행 과정 >   
크롤링 시작페이지 : https://new.land.naver.com/offices?ms=37.5245000,127.0353000,16&a=SG:SMS:GJCG:APTHGJ:GM:TJ&b=B2&e=RETAIL   

## < 지도의 원들의 class 이름>   
제일 안쪽의 map : #article_map > div:nth-child(1) > div   
map_cluster--mix is-outside : 내가 선택한 동 밖   
map_cluster--mix is-length2 : 내가 선택한 동의 원크기가 2인 것(작은 것)   
map_cluster--mix is-length3 : 내가 선택한 동의 원크기가 3인 것(큰 것)   

# 구조 (도산공원 위의 원의 element 값)
```html
<a href="javascript:void(0);" role="button" class="map_cluster--mix is-length2" aria-pressed="false" aria-hidden="false" id="212211002301LGEOHASH_MIX_ARTICLE" data-nclk="MAP.sectorAmark" style="width: 45.8556px; height: 45.8556px; top: 360.429px; left: 1288.68px;">
    <div class="map_cluster_inner">
        <span class="blind" aria-labelledby="region_selected"></span>
        <span class="sale_number">
            12
            <em class="blind">
                개 매물
            </em>
        </span>
    </div>
    <div class="marker_transparent" style="width: 45.8556px; height: 45.8556px;"></div>
</a>   
```

## <에러발생> (http 통신을 빠르게 호출하여 생기는 에러)   
raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='localhost', port=50024): Max retries exceeded with url: /session/c9e72439fd30c98229a61426f98fc7b9/element/536673094BFEE0697B073AFA1E95C7C4_element_107/text (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x11638ce80>: Failed to establish a new connection: [Errno 61] Connection refused'))


## './src/IMG/distance_cal.jpeg' 사진 설명 첨부

185: (-9382.89px   -2786.71px)   
164: (-9400.1px    -2191.94px)   
-> 거리: 595.0189385...   
실제 대략 거리: 1.17km   