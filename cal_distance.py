# input: px -> output: km

def distance(x,y): 
    distance = ((x[0]-y[0])**2 + (x[1]-y[1])**2) ** 0.5 * 0.001966323968168877
    return distance

# x = (-9382.89, -2786.71)
# y = (-9400.1, -2191.94)
# print(f'축적: {1.17/distance} km/px') # 0.001966323968168877 km/px
# print(f'축적: {distance/1.17} px/km') # 508.5631951744156 px/km