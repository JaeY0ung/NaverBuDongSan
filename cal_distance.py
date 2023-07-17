def distance(x,y):

    # 거리 계산 (단위: px)
    # x = (-9382.89, -2786.71)
    # y = (-9400.1, -2191.94)
    distance = ((x[0]-y[0])**2 + (x[1]-y[1])**2) ** 0.5
    # print(distance)
    # print(f'축적: {1.17/distance} km/px') # 0.001966323968168877 km/px
    # print(f'축적: {distance/1.17} px/km') # 508.5631951744156 px/km

    # print(f'500m: {0.5 * distance/1.17}px') # 500m: 254.2815975872078px
    return distance