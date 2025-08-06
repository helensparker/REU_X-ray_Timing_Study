#Adjusted to make ltc=True

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from astropy.visualization import time_support

from sunpy import timeseries as ts
from sunpy.net import Fido
from sunpy.net import attrs as a

from math import *
from pprint import pprint
from datetime import timedelta
from astropy.table import QTable
from stixdcpy.quicklook import LightCurves
from stixdcpy.energylut import EnergyLUT
from stixdcpy import auxiliary as aux
from stixdcpy.net import FitsQuery as fq
from stixdcpy.net import Request as jreq
from stixdcpy import instrument as inst
from stixdcpy.science import PixelData, Spectrogram, spec_fits_crop, spec_fits_concatenate, fits_time_to_datetime
from stixdcpy.housekeeping import Housekeeping
from astropy.io import fits
from stixdcpy import detector_view as dv
from stixdcpy import spectrogram  as cspec
from stixdcpy.imgspec import ImgSpecArchive as isar
from datetime import datetime
from datetime import time
from datetime import timedelta
import csv


def getMaxandTime(c,dsfakestart,dsstart,dsend):
    #print(len(set(lc.data['counts'][c])))
    #print(lc.data['counts'][c])
    #print(set(lc.data['counts'][c]))
    max = 0
    
    if len(set(lc.data['counts'][c])) <= 9:
        deltatime = 0
    else:
        for k in range(len(lc.data['counts'][c])):
            #print(dsfakestart + timedelta(0,lc.data['delta_time'][k]))
            val = lc.data['counts'][c][k]
            if val > max:
                if dsfakestart + timedelta(0,lc.data['delta_time'][k]) > dsend:
                    break
                if not (dsfakestart + timedelta(0,lc.data['delta_time'][k]) < dsstart and dsfakestart + timedelta(0,lc.data['delta_time'][k]) > dsend):
                    deltatime = lc.data['delta_time'][k]
                    max = val
    return [deltatime,max]

def goesGetMaxandTime(array,extraarray,c):
    max = 0
    deltatime = 0
    for k in range(len(array)):
        val = array[k][c]
        if val > max:
            max = val
            deltatime = k
        #print(val,extraarray[k][c])
    
    if max < 10**(-6):
        #print('help')
        for k in range(len(extraarray)):
            val = extraarray[k][c]
            #print(val)
            if val > max:
                max = val
                deltatime = k
    return [deltatime,max]
    

df = pd.read_csv('CandAboveVisfromEarthBackgroundmatching_flares.csv')
df2 = pd.read_csv('LTCMPFLFNoAttFixPeaks.csv')

data = []

indexList = [43, 65, 91, 97, 99, 103, 109, 115, 139, 144, 157, 160, 166, 168, 198, 202, 217, 222, 227, 234, 239, 241, 246, 293, 301, 312, 315, 357, 366, 369, 372, 375, 387, 394, 398, 408, 415, 421, 431, 445, 449, 459, 465, 472, 474, 485, 492, 493, 503, 519, 528, 535, 545, 547, 559, 563, 566, 567, 569, 572, 575, 577, 580, 586, 588, 589, 591, 594, 595, 603, 612, 614, 616, 619, 625, 627, 628, 634, 643, 644, 648, 652, 658, 660, 666, 668, 670, 672, 678, 681, 682, 688, 694, 696, 701, 708, 710, 714, 733, 763, 787, 794, 804, 808, 815, 839, 845, 864, 866, 868, 870, 881, 893, 897, 903, 904, 911, 914, 916, 918, 919, 923, 928, 936, 940, 948, 999, 1004, 1007, 1009, 1010, 1011, 1013, 1015, 1020, 1025, 1026, 1039, 1049, 1050, 1054, 1071, 1072, 1076, 1078, 1083, 1097, 1102, 1104, 1105, 1111, 1114, 1116, 1118, 1119, 1125, 1133, 1144, 1149, 1152, 1159, 1171, 1174, 1182, 1184, 1188, 1195, 1197, 1198, 1213, 1231, 1234, 1239, 1240, 1243, 1245, 1248, 1249, 1250, 1254, 1267, 1276, 1280, 1282, 1283, 1295, 1301, 1305, 1312, 1313, 1325, 1330, 1332, 1346, 1347, 1350, 1351, 1367, 1368, 1369, 1384, 1388, 1399, 1402, 1411, 1437, 1442, 1457, 1459, 1460, 1466, 1480, 1494, 1507, 1536, 1538, 1542, 1544, 1545, 1547, 1552, 1558, 1560, 1564, 1567, 1568, 1569, 1572, 1578, 1583, 1603, 1607, 1609, 1611, 1613, 1614, 1616, 1617, 1625, 1628, 1629, 1646, 1647, 1648, 1649, 1653, 1656, 1658, 1663, 1667, 1675, 1687, 1689, 1692, 1694, 1696, 1697, 1700, 1701, 1706, 1707, 1708, 1709, 1720, 1726, 1730, 1736, 1742, 1749, 1769, 1772, 1784, 1788, 1797, 1805, 1814, 1815, 1817, 1818, 1821, 1824, 1830, 1833, 1836, 1839, 1846, 1849, 1856, 1860, 1879, 1884, 1886, 1890, 1897, 1901, 1913, 1916, 1924, 1928, 1929, 1936, 1937, 1954, 1955, 1958, 1961, 1967, 1972, 1983, 1995, 2003, 2025, 2028, 2030, 2049, 2053, 2054, 2057, 2068, 2070, 2075, 2084, 2116, 2117, 2123, 2126, 2127, 2133, 2156, 2158, 2162, 2170, 2172, 2176, 2187, 2190, 2193, 2195, 2203, 2207, 2208, 2209, 2212, 2216, 2221, 2229, 2240, 2246, 2248, 2260, 2264, 2266, 2267, 2281, 2293, 2294, 2311, 2315, 2317, 2320, 2324, 2338, 2341, 2351, 2352, 2354, 2364, 2373, 2375, 2377, 2382, 2391, 2413, 2416, 2418, 2419, 2424, 2431, 2432, 2435, 2436, 2437, 2443, 2448, 2452, 2454, 2455, 2462, 2465, 2468, 2470, 2482, 2493, 2495, 2501, 2502, 2504, 2507, 2508, 2525, 2533, 2537, 2541, 2547, 2552, 2556, 2557, 2560, 2571, 2579, 2592, 2597, 2600, 2617, 2627, 2672, 2677, 2695, 2698, 2699, 2704, 2708, 2710, 2712, 2715, 2720, 2721, 2723, 2737, 2738, 2739, 2744, 2751, 2752, 2753, 2758, 2765, 2770, 2785, 2787, 2788, 2790, 2792, 2804, 2809, 2819, 2822, 2825, 2826, 2831, 2840, 2846, 2847, 2855, 2859, 2863, 2864, 2865, 2871, 2873, 2878, 2883, 2884, 2885, 2887, 2889, 2893, 2899, 2913, 2915, 2921, 2926, 2931, 2933, 2938, 2939, 2944, 2948, 2958, 2962, 2967, 2970, 2973, 2978, 2989, 2990, 3002, 3009, 3011, 3015, 3016, 3020, 3033, 3036, 3038, 3040, 3045, 3052, 3053, 3054, 3055, 3056, 3065, 3072, 3079, 3081, 3083, 3086, 3103, 3109, 3114, 3119, 3121, 3124, 3126, 3128, 3129, 3131, 3133, 3138, 3139, 3146, 3152, 3153, 3161, 3162, 3163, 3165, 3170, 3172, 3173, 3177, 3178, 3186, 3191, 3193, 3194, 3200, 3210, 3211, 3212, 3216, 3219, 3223, 3225, 3226, 3229, 3233, 3235, 3244, 3249, 3254, 3259, 3265, 3280, 3293, 3300, 3305, 3308, 3318, 3326, 3330, 3331, 3335, 3338, 3350, 3353, 3358, 3382, 3387, 3390, 3391, 3407, 3411, 3421, 3430, 3439, 3448, 3468, 3474, 3477, 3478, 3481, 3482, 3518, 3521, 3529, 3536, 3543, 3547, 3549, 3564, 3574, 3580, 3611, 3616, 3617, 3625, 3627, 3630, 3638, 3640, 3659, 3662, 3663, 3667, 3681, 3683, 3684, 3686, 3691, 3694, 3695, 3697, 3702, 3706, 3709, 3721, 3730, 3732, 3735, 3736, 3743, 3750, 3771, 3779, 3789, 3795, 3816, 3823, 3842, 3848, 3853, 3855, 3858, 3859, 3868, 3886, 3892, 3894, 3906, 3919, 3924, 3928, 3942, 3955, 3966, 3973, 3974, 3982, 3988, 3990, 3992, 3995, 4001, 4003, 4007, 4013, 4039, 4049, 4070, 4084, 4087, 4113, 4117, 4128, 4147, 4156, 4163, 4168, 4174, 4187, 4205, 4223, 4228, 4234, 4235, 4251, 4253, 4255, 4263, 4268, 4270]
otherindexList = [15, 51, 84, 87, 104, 107, 150, 170, 177, 191, 195, 197, 215, 216, 220, 238, 256, 259, 278, 297, 298, 314, 324, 327, 335, 385, 388, 432, 444, 468, 499, 553, 602, 615, 662, 664, 697, 725, 750, 751, 778, 785, 818, 840, 851, 854, 862, 884, 889, 897, 903, 904, 909, 911, 913, 914, 916, 918, 919, 922, 923, 928, 937, 940, 951, 973, 988, 989, 999, 1004, 1007, 1009, 1010, 1011, 1013, 1015, 1016, 1029, 1050, 1058, 1063, 1071, 1072, 1076, 1077, 1087, 1091, 1098, 1106, 1126, 1161, 1186, 1194, 1200, 1229, 1235, 1236, 1238, 1260, 1270, 1275, 1278, 1300, 1326, 1336, 1338, 1392, 1398, 1401, 1414, 1529, 1532, 1583, 1588, 1597, 1601, 1603, 1609, 1613, 1614, 1616, 1617, 1628, 1629, 1630, 1631, 1647, 1648, 1649, 1653, 1656, 1658, 1663, 1700, 1701, 1706, 1707, 1709, 1720, 1726, 1736, 1749, 1762, 1772, 1782, 1784, 1786, 1797, 1807, 1814, 1815, 1817, 1818, 1820, 1821, 1824, 1827, 1829, 1830, 1833, 1839, 1849, 1852, 1856, 1860, 1864, 1879, 1886, 1888, 1890, 1897, 1901, 1913, 1916, 1924, 1928, 1929, 1936, 1937, 1942, 1954, 1955, 1958, 1961, 1964, 1967, 1970, 1971, 1972, 1983, 1991, 1995, 2025, 2028, 2030, 2035, 2037, 2041, 2048, 2049, 2061, 2066, 2068, 2070, 2083, 2084, 2116, 2119, 2121, 2123, 2126, 2127, 2133, 2140, 2156, 2158, 2162, 2170, 2171, 2172, 2176, 2182, 2187, 2190, 2195, 2197, 2198, 2203, 2205, 2207, 2212, 2213, 2214, 2216, 2221, 2225, 2229, 2240, 2244, 2246, 2248, 2260, 2262, 2264, 2266, 2267, 2281, 2282, 2293, 2311, 2315, 2317, 2320, 2324, 2326, 2338, 2341, 2343, 2346, 2352, 2353, 2354, 2362, 2370, 2373, 2375, 2377, 2391, 2408, 2413, 2416, 2418, 2419, 2424, 2431, 2432, 2435, 2436, 2437, 2443, 2448, 2451, 2452, 2454, 2455, 2462, 2465, 2468, 2470, 2472, 2482, 2493, 2498, 2501, 2502, 2504, 2506, 2507, 2533, 2537, 2547, 2550, 2551, 2552, 2556, 2557, 2569, 2571, 2575, 2584, 2592, 2596, 2597, 2600, 2617, 2635, 2649, 2657, 2658, 2663, 2675, 2677, 2683, 2695, 2698, 2699, 2704, 2708, 2710, 2712, 2715, 2720, 2721, 2723, 2732, 2734, 2737, 2738, 2739, 2744, 2750, 2751, 2752, 2753, 2754, 2758, 2765, 2770, 2773, 2779, 2785, 2787, 2788, 2790, 2802, 2804, 2809, 2819, 2820, 2822, 2826, 2831, 2840, 2846, 2847, 2855, 2863, 2864, 2871, 2872, 2873, 2874, 2878, 2884, 2885, 2893, 2894, 2899, 2913, 2915, 2921, 2926, 2933, 2938, 2944, 2947, 2951, 2958, 2962, 2967, 2970, 2978, 2989, 2990, 3002, 3006, 3009, 3011, 3015, 3023, 3028, 3036, 3040, 3045, 3047, 3052, 3053, 3054, 3055, 3056, 3059, 3065, 3077, 3079, 3081, 3083, 3085, 3086, 3090, 3096, 3101, 3103, 3107, 3109, 3118, 3119, 3121, 3122, 3124, 3126, 3128, 3131, 3132, 3133, 3137, 3138, 3139, 3146, 3154, 3162, 3163, 3165, 3170, 3172, 3173, 3176, 3178, 3186, 3191, 3193, 3194, 3210, 3211, 3214, 3216, 3219, 3223, 3225, 3226, 3229, 3234, 3244, 3249, 3254, 3259, 3265, 3271, 3280, 3293, 3297, 3300, 3305, 3308, 3312, 3318, 3325, 3326, 3330, 3331, 3335, 3338, 3342, 3350, 3353, 3358, 3359, 3382, 3390, 3391, 3407, 3411, 3418, 3439, 3448, 3474, 3477, 3478, 3481, 3482, 3490, 3518, 3521, 3524, 3529, 3536, 3549, 3555, 3564, 3565, 3574, 3580, 3593, 3611, 3616, 3617, 3625, 3627, 3630, 3638, 3640, 3654, 3659, 3663, 3681, 3683, 3684, 3686, 3691, 3695, 3697, 3702, 3706, 3709, 3721, 3730, 3732, 3735, 3743, 3745, 3748, 3750, 3764, 3771, 3777, 3779, 3789, 3795, 3805, 3816, 3819, 3823, 3835, 3842, 3848, 3853, 3855, 3858, 3859, 3868, 3886, 3888, 3894, 3906, 3909, 3919, 3924, 3928, 3942, 3955, 3957, 3973, 3974, 3975, 3978, 3982, 3988, 3990, 3992, 3995, 4001, 4007, 4013, 4084, 4086, 4087, 4098, 4102, 4113, 4117, 4124, 4128, 4130, 4136, 4156, 4163, 4168, 4174, 4176, 4198, 4205, 4228, 4234, 4235, 4246, 4251, 4253, 4254, 4255, 4259, 4263, 4267, 4270]
indexList = indexList + otherindexList
indexList.sort()
indexList = [3382, 3387, 3390, 3391]

index = 2907+485+184
#distance = index + 1
distance = 4527
beg = 0

with open('ahhhRealNPAnewTrial.csv', 'a', newline='') as file :
    writer = csv.writer(file)
    #for i in tqdm(range(index,distance)):
    for k in tqdm(range(0,len(indexList))):
        i = indexList[k]
        start = df2.iloc[i,0]
        end = df2.iloc[i,1]
        for j in range(17,4,-1):
            result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(j), a.Resolution("flx1s"))
            coolFile = Fido.fetch(result_goes)
            goes = ts.TimeSeries(coolFile)
            extra_result_goes = Fido.search(a.Time(start, end), a.Instrument("XRS"), a.goes.SatelliteNumber(16), a.Resolution("flx1s"))
            extracoolFile = Fido.fetch(extra_result_goes)
            extragoes = ts.TimeSeries(extracoolFile)
            if not type(goes) is list:
                for j in range(beg,4521):
                    if df.iloc[j,0] == df2.iloc[i,0]:
                        beg = j
                        break
                sstart = df.iloc[j,2]
                send = df.iloc[j,3]
                lc = LightCurves.from_sdc(start_utc=start, end_utc=end, ltc=True)
                dgstart = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
                dgend = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
                dsstart = datetime.strptime(sstart, "%Y-%m-%dT%H:%M:%S.%f")
                dsend = datetime.strptime(send, "%Y-%m-%dT%H:%M:%S.%f")
                dsfakestart = datetime.strptime(lc.data['start_utc'], "%Y-%m-%dT%H:%M:%S.%f")
                sstart = start
                send = end
                dsstart = dgstart
                dsend = dgend
                truncgoes = goes.truncate(sstart,send)
                arrgoes = truncgoes.to_array()
                if not type(extragoes) is list:
                    extratruncgoes = extragoes.truncate(sstart,send)
                    extraarrgoes = extratruncgoes.to_array()
                else:
                    extraarrgoes = []

                maxtime18 = goesGetMaxandTime(arrgoes,extraarrgoes,1)
                deltatime18 = maxtime18[0]
                time18 = dsstart + timedelta(0,deltatime18)
                val18 = maxtime18[1]

                maxtime410 = getMaxandTime(0,dsfakestart,dsstart,dsend)
                deltatime410 = maxtime410[0]
                time410 = dsfakestart + timedelta(0,deltatime410)
                val410 = maxtime410[1]

                maxtime1015 = getMaxandTime(1,dsfakestart,dsstart,dsend)
                deltatime1015 = maxtime1015[0]
                time1015 = dsfakestart + timedelta(0,deltatime1015)
                val1015 = maxtime1015[1]

                maxtime1525 = getMaxandTime(2,dsfakestart,dsstart,dsend)
                deltatime1525 = maxtime1525[0]
                time1525 = dsfakestart + timedelta(0,deltatime1525)
                val1525 = maxtime1525[1]

                maxtime2550 = getMaxandTime(3,dsfakestart,dsstart,dsend)
                deltatime2550 = maxtime2550[0]
                time2550 = dsfakestart + timedelta(0,deltatime2550)
                val2550 = maxtime2550[1]

                maxtime5084 = getMaxandTime(4,dsfakestart,dsstart,dsend)
                deltatime5084 = maxtime5084[0]
                time5084 = dsfakestart + timedelta(0,deltatime5084)
                val5084 = maxtime5084[1]

                #data.append([sstart,send,time18,val18,time410,val410,time1015,val1015,time1525,val1525,time2550,val2550,time5084,val5084])
                writer.writerow([sstart,send,time18,val18,time410,val410,time1015,val1015,time1525,val1525,time2550,val2550,time5084,val5084,df.iloc[i,4],df.iloc[i,5],df.iloc[i,6],df.iloc[i,7],df.iloc[i,8]])
                break


#with open('CandAbovepeaktimesandVals.csv', 'w', newline='') as file :
    #writer = csv.writer(file)
    #writer.writerows(data)