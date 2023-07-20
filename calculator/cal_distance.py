# input: px -> output: m
# top, left 순
def distance(x): # -> 도산공원 위 원(12) 좌표: 이걸 중심 좌표로 사용
    center=(-9402.41, -2389.17)
    distance = ((x[0]-center[0])**2 + (x[1]-center[1])**2) ** 0.5 * 0.001966323968168877 * 1000
    return distance

# x = (-9382.89, -2786.71)
# y = (-9400.1, -2191.94)
# print(f'축적: {1.17/distance} km/px') # 0.001966323968168877 km/px
# print(f'축적: {distance/1.17} px/km') # 508.5631951744156 px/km