# This is a sample Python script.
import math
import os
import random
import re
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def minimmCost(red,blue,blueCost):
    time_array=[blueCost]
    on_blue=1
    for i in range(len(red)):
       if red[i]<blue[i]+blueCost*on_blue:
           time_array.append(time_array[i]+red[i])
           on_blue=1
       else:
           time_array.append(time_array[i]+blue[i]+blueCost*on_blue)
           on_blue=0

    return time_array

def minimmCost2(red, blue, blueCost):
    city_times = [0]
    blue_lane = 1
    for i in range (len(red)):
        print("b"+str(blue[i]+(blueCost*blue_lane)))
        print("r"+str(red[i]))
        if (blue[i]+(blueCost*blue_lane)) < red[i]:
            print(str(i)+"b")
            temp = city_times[i]+blue[i]+(blueCost*blue_lane)
            city_times.append(temp)
            blue_lane = 0
        else:
            print(str(i)+"r")
            temp = city_times[i]+red[i]
            city_times.append(temp)
            blue_lane = 1
    """city_times.append(len(red))
    city_times.append(len(blue))
    city_times.extend(red)
    city_times.extend(blue)"""
    return city_times
"""
122786415       479496160       566997962      /281783677      /731449417       734578288      /178191598
            +               +               +               +               +               +
1286845870     /388165368       583694611       751855065       1243867188     /429096340       518948209
901184049       2503547        /198032790       366193244       858205367       43434519        133286388
            =               =               =               =                =               =
122786415       510951783       708984573        990768250      1722217667      2151314007      2284600395
"""

red = [122786415,
479496160,
566997962,
281783677,
731449417,
734578288,
178191598]
blue = [901184049,
2503547,
198032790,
366193244,
858205367,
43434519,
133286388]
blueCost = 385661821
# 281 256 227 || 869 804 186
minimmCost2(red,blue,blueCost)
print(minimmCost2(red,blue,blueCost))



"""
b+
1.286.845.870
388.165.368
583.694.611
751.855.065
1.243.867.188
429.096.340
518.948.209

r
122.786.415
479.496.160
566.997.962
281.783.677
731.449.417
734.578.288
178.191.598
b
901.184.049
2.503.547
198.032.790
366.193.244
858.205.367
43.434.519
133.286.388

385661821"""