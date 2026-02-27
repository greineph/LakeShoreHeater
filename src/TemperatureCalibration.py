import json
import os

import numpy as np
from UliEngineering.Physics.RTD import pt1000_temperature


def cal_RX202A(x):
    if x < 2656:
        return np.nan
    if x > 236751:
        return np.nan
    x = 11.2 - np.log(x - 1400)
    t = np.exp(- 3.1811288786136
               + 0.553973809709068 * x
               + 0.0448073540444195 * x ** 2
               + 0.0425370327776785 * x ** 3
               + 0.0669425260231843 * x ** 4
               - 0.100369265267273 * x ** 5
               - 0.0392631659409316 * x ** 6
               + 0.12428830342497 * x ** 7
               - 0.0517973703312841 * x ** 8
               - 0.025270353474024 * x ** 9
               + 0.0319952962414436 * x ** 10
               - 0.0133560796073571 * x ** 11
               + 0.00289348055850006 * x ** 12
               - 3.2728825734534E-4 * x ** 13
               + 1.53404398537456E-5 * x ** 14)
    return t


# extended range calibration for RX202A far below official calibration (22mK)
# WARNING: The Thermometer is NOT CALIBRATED above 236751 Ohms! Apply caution when using.
def cal_RX202A_ULT(x):
    if x > 226000:
        x = np.log(x - 3000)
        b = - 5.91720757644284 + 0.14100574738178 * np.absolute(x - (+ 18.5631796194264)) ** 1.48488950436842
        return np.exp(b)
    return cal_RX202A(x)


def cal_CHE5(resistance):
    if resistance > 86500:
        return np.nan
    if resistance < 4444:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 3.44844161632531
        + 1.6691138167603 * x
        - 2.50146315644876 * x ** 2
        + 8.33206193926032 * x ** 3
        - 26.1756484539086 * x ** 4
        + 62.6401427094544 * x ** 5
        - 105.259792347065 * x ** 6
        + 123.06076863508 * x ** 7
        - 100.744560782332 * x ** 8
        + 57.9817977258579 * x ** 9
        - 23.3227052825549 * x ** 10
        + 6.41520115594516 * x ** 11
        - 1.14935838297727 * x ** 12
        + 0.120811507650645 * x ** 13
        - 0.0056498743217858 * x ** 14)
    if t < 0:
        return np.nan
    return t


def cal_III(resistance):
    if resistance > 87682:
        return np.nan
    if resistance < 3983:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(- 3.1448117287367
               + 0.982326537212055 * x
               - 0.63694388216135 * x ** 2
               + 3.23749049769267 * x ** 3
               - 10.1626448176404 * x ** 4
               + 19.4169363328197 * x ** 5
               - 24.2645433525736 * x ** 6
               + 21.1537160543603 * x ** 7
               - 13.4299525966247 * x ** 8
               + 6.35502870367363 * x ** 9
               - 2.24318261963574 * x ** 10
               + 0.57517807590146 * x ** 11
               - 0.100772007765836 * x ** 12
               + 0.010703610442176 * x ** 13
               - 5.15782641852657E-4 * x ** 14)
    return np.abs(t)


def cal_VII(resistance):
    if resistance > 87682:
        return np.nan
    if resistance < 3965:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(- 3.48747668094163
               + 0.942406683060128 * x
               + 1.81771678171267 * x ** 2
               - 9.53693479677233 * x ** 3
               + 23.6525709597093 * x ** 4
               - 33.9518490845077 * x ** 5
               + 29.6143355577001 * x ** 6
               - 14.8654715999217 * x ** 7
               + 2.69138866223459 * x ** 8
               + 1.56758123848215 * x ** 9
               - 1.32413226562706 * x ** 10
               + 0.463189163228743 * x ** 11
               - 0.0908763409779729 * x ** 12
               + 0.0097636477232289 * x ** 13
               - 4.49449037126559E-4 * x ** 14)
    if t < 0:
        return np.nan
    return np.abs(t)


def cal_VIII(resistance):
    if resistance > 90876:
        return np.nan
    if resistance < 3966:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(- 3.2399844232487
               + 0.90937501196579 * x
               - 0.236194937213842 * x ** 2
               + 0.334479761913975 * x ** 3
               + 1.92984511141176 * x ** 4
               - 8.36436542974131 * x ** 5
               + 15.5116471131059 * x ** 6
               - 17.0802373867062 * x ** 7
               + 12.2903863735048 * x ** 8
               - 5.99288660987976 * x ** 9
               + 1.99162340395573 * x ** 10
               - 0.442371737178011 * x ** 11
               + 0.062344296759464 * x ** 12
               - 0.00497812072192625 * x ** 13
               + 1.67903902250485E-4 * x ** 14)
    if t < 0:
        return np.nan
    return t


def cal_XII(resistance):
    if resistance > 99212:  #this is dangerous. the thermometer is not well calibrated below 30 mK (80kOhm)
        return np.nan
    if resistance < 2500:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 3.43513072381326
        + 0.827293971921533 * x
        - 0.131782466142724 * x ** 2
        + 1.11197361475876 * x ** 3
        - 1.44030737999121 * x ** 4
        - 1.50892394546076 * x ** 5
        + 6.65571565713781 * x ** 6
        - 9.20671817267059 * x ** 7
        + 7.33806378806987 * x ** 8
        - 3.78425962816141 * x ** 9
        + 1.30573148628834 * x ** 10
        - 0.300104987801589 * x ** 11
        + 0.0441522489296117 * x ** 12
        - 0.00376435510315209 * x ** 13
        + 1.41500740503309E-4 * x ** 14)

    if t < 0.025:
        return np.nan
    return t


def cal_XIII(resistance):
    if resistance > 88557:
        return np.nan
    if resistance < 2160:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 3.4497267843033
        + 1.21778871223976 * x
        - 1.03344423347588 * x ** 2
        + 2.89290607362355 * x ** 3
        - 4.82342669589366 * x ** 4
        + 3.92705153961975 * x ** 5
        + 0.0834162981837321 * x ** 6
        - 3.49493591084809 * x ** 7
        + 3.81455182750528 * x ** 8
        - 2.25045715434612 * x ** 9
        + 0.839846410866675 * x ** 10
        - 0.20377419351724 * x ** 11
        + 0.0312570044410805 * x ** 12
        - 0.00275851262646419 * x ** 13
        + 1.06845338189234E-4 * x ** 14)

    if t < 0.03:
        return np.nan
    return t


def cal_XIV(resistance):
    if resistance > 72200:
        return np.nan
    if resistance < 4397:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 4.11495995586646
        + 7.69172693111883 * x
        - 44.1980827675411 * x ** 2
        + 195.14623356676 * x ** 3
        - 569.239821947079 * x ** 4
        + 1121.01070356226 * x ** 5
        - 1532.38312826353 * x ** 6
        + 1485.30673824265 * x ** 7
        - 1033.29591061602 * x ** 8
        + 517.063114343151 * x ** 9
        - 184.365647803601 * x ** 10
        + 45.6726203855708 * x ** 11
        - 7.46610262030369 * x ** 12
        + 0.72379973289235 * x ** 13
        - 0.0315040282067667 * x ** 14)
    if t < 0:
        return np.nan
    return t


def cal_UTQ1(resistance):
    if resistance > 107483:
        return np.nan
    if resistance < 3918:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(

        - 3.22119899138981
        + 0.914197652968111 * x
        - 0.25977217479208 * x ** 2
        + 0.0020165801528922 * x ** 3
        + 1.6751903788556 * x ** 4
        - 2.38768301384658 * x ** 5
        - 4.18350006552033 * x ** 6
        + 16.7042158288992 * x ** 7
        - 23.2934939959949 * x ** 8
        + 18.4326754651273 * x ** 9
        - 9.16161408813651 * x ** 10
        + 2.92158329761292 * x ** 11
        - 0.581900564576006 * x ** 12
        + 0.0660276013097698 * x ** 13
        - 0.0032628104518172 * x ** 14)

    if t < 0.028:
        return np.nan
    return t


def cal_UTQ2(resistance):
    if resistance > 109628:
        return np.nan
    if resistance < 3957:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 3.20614953724189
        + 0.962078265409415 * x
        - 0.208440969963698 * x ** 2
        - 0.13456756006725 * x ** 3
        + 1.62037510407708 * x ** 4
        - 2.51039306733672 * x ** 5
        - 2.32848015771281 * x ** 6
        + 12.5469873989263 * x ** 7
        - 18.6510334363121 * x ** 8
        + 15.3224678851932 * x ** 9
        - 7.83560876101183 * x ** 10
        + 2.55912931916577 * x ** 11
        - 0.520513325198992 * x ** 12
        + 0.060185173048065 * x ** 13
        - 0.00302544433304143 * x ** 14)

    if t < 0.028:
        return np.nan
    return t


def cal_UTQ4(resistance):
    if resistance > 72660:
        return np.nan
    if resistance < 2820:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        -3.66745587910755
        + 1.41974234310578 * x
        - 0.278950626396528 * x ** 2
        - 10.6047076424789 * x ** 3
        + 49.5955784122101 * x ** 4
        - 101.309771596877 * x ** 5
        + 119.18130345728 * x ** 6
        - 89.273978474034 * x ** 7
        + 44.4608903826715 * x ** 8
        - 14.8883355567147 * x ** 9
        + 3.2958517214749 * x ** 10
        - 0.455601732948729 * x ** 11
        + 0.0338146896149037 * x ** 12
        - 6.91344361514763E-4 * x ** 13
        - 3.95445709646093E-5 * x ** 14)

    if t < 0.03:  #this is quite high, but the cal run was not perfect V2.4r5
        return np.nan
    return t


def cal_UTQ17_ER(resistance):
    if resistance > 62451:
        return np.nan
    if resistance < 2500:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 4.22361815260922
        + 5.85475169048575 * x
        - 27.5487865262371 * x ** 2
        + 78.2267024307011 * x ** 3
        - 134.671659376471 * x ** 4
        + 151.339154541923 * x ** 5
        - 114.859025100429 * x ** 6
        + 59.7562799156407 * x ** 7
        - 21.2944801498978 * x ** 8
        + 5.10114666877901 * x ** 9
        - 0.784281816772661 * x ** 10
        + 0.0698507383406406 * x ** 11
        - 0.00273817721146465 * x ** 12)

    if t < 0.030 or t > 8.05:
        return np.nan
    return t


def cal_UTQ5(resistance):
    if resistance > 76210:
        return np.nan
    if resistance < 2801:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 3.71958216239522
        + 1.94613040542538 * x
        - 3.98839907720686 * x ** 2
        + 9.64690641802497 * x ** 3
        - 11.2819832763546 * x ** 4
        + 1.88625497853504 * x ** 5
        + 12.479978631154 * x ** 6
        - 19.1015843971005 * x ** 7
        + 15.1715654273227 * x ** 8
        - 7.71960094680198 * x ** 9
        + 2.64369608121889 * x ** 10
        - 0.608347815153645 * x ** 11
        + 0.0903410241129497 * x ** 12
        - 0.00782715495067897 * x ** 13
        + 3.00580159746109E-4 * x ** 14)

    if t < 0.03:  #this is quite high, but the cal run was not perfect V2.4r5
        return np.nan
    return t


def cal_UTQ8(resistance):
    if resistance > 82840:
        return np.nan
    if resistance < 3910:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 3.52394572893064
        + 1.62095556446493 * x
        - 2.90853577017576 * x ** 2
        + 10.8514429896907 * x ** 3
        - 29.9392403551094 * x ** 4
        + 55.9146125520038 * x ** 5
        - 70.4886070327271 * x ** 6
        + 61.0045854719994 * x ** 7
        - 36.6971081680757 * x ** 8
        + 15.3789752554898 * x ** 9
        - 4.44054181231263 * x ** 10
        + 0.857213113886487 * x ** 11
        - 0.103988583202568 * x ** 12
        + 0.00696960141435143 * x ** 13
        - 1.85462453724902E-4 * x ** 14)

    if t < 0.03:  #this is quite high, but the cal run was not perfect V2.4r5
        return np.nan
    return t


def cal_UTQ9(resistance):
    if resistance > 79300:
        return np.nan
    if resistance < 3820:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 3.4674548041673
        + 1.62576125008428 * x
        - 2.26707669402106 * x ** 2
        + 5.05472447065757 * x ** 3
        - 8.50101412499486 * x ** 4
        + 11.0755435303649 * x ** 5
        - 11.0709252750389 * x ** 6
        + 8.26275542119113 * x ** 7
        - 4.44509719930531 * x ** 8
        + 1.66276807784458 * x ** 9
        - 0.413207286925892 * x ** 10
        + 0.0628335948627899 * x ** 11
        - 0.00471644295747472 * x ** 12
        + 1.32064985581528E-5 * x ** 13
        + 1.46140148060052E-5 * x ** 14)

    if t < 0.03:  #this is quite high, but the cal run was not perfect V2.4r5
        return np.nan
    return t


def cal_UTC01(resistance):
    if resistance > 55626:
        return np.nan
    if resistance < 2568:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        -2.94525884793961
        - 20.7654552099012 * x
        + 115.936636769547 * x ** 2
        - 307.463745190336 * x ** 3
        + 488.939157005646 * x ** 4
        - 506.635661474809 * x ** 5
        + 356.443361402175 * x ** 6
        - 172.924782875645 * x ** 7
        + 57.3766204828052 * x ** 8
        - 12.450326881569 * x ** 9
        + 1.52419037588981 * x ** 10
        - 0.0322915776137202 * x ** 11
        - 0.0191153201494443 * x ** 12
        + 0.00264578347210478 * x ** 13
        - 1.16801687672886E-4 * x ** 14)

    if t < 0.03:  #this is quite high, but the cal run was not perfect V2.4r10
        return np.nan
    return t


def cal_ultq14(resistance):
    if resistance > 29011:
        return np.nan
    if resistance < 3350:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 25.2723559665532
        + 160.046553843434 * x
        - 543.157919496375 * x ** 2
        + 1028.91047660209 * x ** 3
        - 1157.35965510837 * x ** 4
        + 753.858121996137 * x ** 5
        - 213.031184964892 * x ** 6
        - 61.4638412128654 * x ** 7
        + 77.9276918781246 * x ** 8
        - 27.4992910063753 * x ** 9
        + 2.54605302771488 * x ** 10
        + 1.19640586749869 * x ** 11
        - 0.451482513034092 * x ** 12
        + 0.0631128694374147 * x ** 13
        - 0.00335574259658125 * x ** 14)

    if t < 0.005:
        return np.nan
    return t


def cal_UTCC_1A(resistance):
    if resistance > 29959:
        return np.nan
    if resistance < 1635.24:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 201.589240609966
        + 1160.72418983346 * x
        - 2977.80634883909 * x ** 2
        + 4365.12610873575 * x ** 3
        - 3988.83133653989 * x ** 4
        + 2291.87185844487 * x ** 5
        - 751.72695448881 * x ** 6
        + 66.6988971333745 * x ** 7
        + 49.9320824125349 * x ** 8
        - 20.369299997391 * x ** 9
        + 1.79314811903037 * x ** 10
        + 0.749247515579554 * x ** 11
        - 0.252274931720241 * x ** 12
        + 0.0312055304261736 * x ** 13
        - 0.0014632729224096 * x ** 14)

    if t < 0.0248 or t > 2.05:
        return np.nan
    return t


def cal_UTCC_2A(resistance):
    if resistance > 27328.6:
        return np.nan
    if resistance < 1298.92:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 200.700721047932
        + 1096.85530628962 * x
        - 2694.6141910005 * x ** 2
        + 3803.48774681606 * x ** 3
        - 3356.19095113906 * x ** 4
        + 1859.85979052586 * x ** 5
        - 579.042667251998 * x ** 6
        + 36.4221813302631 * x ** 7
        + 45.769727049894 * x ** 8
        - 17.7860958035517 * x ** 9
        + 1.89069472761921 * x ** 10
        + 0.452355139869341 * x ** 11
        - 0.169389887133093 * x ** 12
        + 0.0210175987908197 * x ** 13
        - 9.69525614960736E-4 * x ** 14)

    if t < 0.0248 or t > 2.05:
        return np.nan
    return t


def cal_UTC1kC01(resistance):
    if resistance > 9418:
        return np.nan
    if resistance < 1331:
        return np.nan
    x = 8 - np.log(resistance - 400)
    t = np.exp(
        - 1.41866032087925
        + 2.19314590313792 * x
        + 0.33923816769954 * x ** 2
        - 0.290282555944923 * x ** 3
        + 0.349148843406013 * x ** 4
        + 1.80800549202416 * x ** 5
        - 2.14680966088836 * x ** 6
        - 4.22706072267358 * x ** 7
        + 5.59499512909235 * x ** 8
        + 5.84755704962578 * x ** 9
        - 7.20937159582863 * x ** 10
        - 4.13721580879552 * x ** 11
        + 4.59538988839531 * x ** 12
        + 1.17650198196056 * x ** 13
        - 1.18291123507886 * x ** 14)

    if t < 0.035 or t > 6.9:
        return np.nan
    return t


def cal_UTC1kC04(resistance):
    if resistance > 1440:
        return np.nan
    if resistance < 8463:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
    - 4612.08196167278
    + 12180.4638343189 * x
    - 14492.8785202681 * x ** 2
    + 10247.4622498295 * x ** 3
    - 4787.89230296216 * x ** 4
    + 1554.72188726781 * x ** 5
    - 359.050382863487 * x ** 6
    + 59.2633054736637 * x ** 7
    - 6.91280506136773 * x ** 8
    + 0.552646586998497 * x ** 9
    - 0.0284842128907803 * x ** 10
    + 8.36296670092601E-4 * x ** 11
    - 1.02379019065868E-5 * x ** 12)

    if t < 0.050 or t > 4.5:
        return np.nan
    return t


def cal_UTC1kB01(resistance):
    if resistance > 9359:
        return np.nan
    if resistance < 1334:
        return np.nan
    x = 10 - np.log(resistance - 800)
    t = np.exp(
        - 421.335708306949
        + 2151.60721968023 * x
        - 4890.28322357339 * x ** 2
        + 6395.47542878098 * x ** 3
        - 5236.51810066492 * x ** 4
        + 2695.27827111976 * x ** 5
        - 776.18927577532 * x ** 6
        + 37.4384058053729 * x ** 7
        + 61.033631460805 * x ** 8
        - 23.2575917409555 * x ** 9
        + 3.08784983630933 * x ** 10
        + 0.236165342200827 * x ** 11
        - 0.137420109177808 * x ** 12
        + 0.0180248051344341 * x ** 13
        - 8.50626044031961E-4 * x ** 14)

    if t < 0.035 or t > 6.9:
        return np.nan
    return t


def cal_UTC1kB02(resistance):
    if resistance > 8788:
        return np.nan
    if resistance < 1341:
        return np.nan
    x = 9 - np.log(resistance - 900)
    t = np.exp(
        - 2.86047529459422
        - 4.9334449356037 * x
        + 30.2155588772832 * x ** 2
        - 56.9343276033081 * x ** 3
        + 11.6906114044408 * x ** 4
        + 145.114150616824 * x ** 5
        - 297.384973284831 * x ** 6
        + 302.905644595519 * x ** 7
        - 187.030386675248 * x ** 8
        + 72.8664844708624 * x ** 9
        - 17.5404517149855 * x ** 10
        + 2.3858247410437 * x ** 11
        - 0.140383950698021 * x ** 12)

    if t < 0.050 or t > 8:
        return np.nan
    return t


def cal_UTQ13(resistance):
    if resistance > 20330:
        return np.nan
    if resistance < 2383:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 1307.91840021157
        + 5393.14252019654 * x
        - 9794.60446796565 * x ** 2
        + 10203.7579661666 * x ** 3
        - 6630.17600973474 * x ** 4
        + 2673.00822775798 * x ** 5
        - 560.713645119828 * x ** 6
        - 24.3032657348917 * x ** 7
        + 55.0526297781223 * x ** 8
        - 17.4042848335018 * x ** 9
        + 2.77289399222898 * x ** 10
        - 0.196685718317171 * x ** 11
        - 0.0054966708336739 * x ** 12
        + 0.00190859926947573 * x ** 13
        - 9.5194934196305E-5 * x ** 14)
    if t < 0.035 or t > 6.2:
        return np.nan
    return t


def cal_UTCC_1A(resistance):
    if resistance > 29959:
        return np.nan
    if resistance < 1635.24:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 201.589240609966
        + 1160.72418983346 * x
        - 2977.80634883909 * x ** 2
        + 4365.12610873575 * x ** 3
        - 3988.83133653989 * x ** 4
        + 2291.87185844487 * x ** 5
        - 751.72695448881 * x ** 6
        + 66.6988971333745 * x ** 7
        + 49.9320824125349 * x ** 8
        - 20.369299997391 * x ** 9
        + 1.79314811903037 * x ** 10
        + 0.749247515579554 * x ** 11
        - 0.252274931720241 * x ** 12
        + 0.0312055304261736 * x ** 13
        - 0.0014632729224096 * x ** 14)

    if t < 0.0248 or t > 2.05:
        return np.nan
    return t


def cal_UTCC_2A(resistance):
    if resistance > 27328.6:
        return np.nan
    if resistance < 1298.92:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        - 200.700721047932
        + 1096.85530628962 * x
        - 2694.6141910005 * x ** 2
        + 3803.48774681606 * x ** 3
        - 3356.19095113906 * x ** 4
        + 1859.85979052586 * x ** 5
        - 579.042667251998 * x ** 6
        + 36.4221813302631 * x ** 7
        + 45.769727049894 * x ** 8
        - 17.7860958035517 * x ** 9
        + 1.89069472761921 * x ** 10
        + 0.452355139869341 * x ** 11
        - 0.169389887133093 * x ** 12
        + 0.0210175987908197 * x ** 13
        - 9.69525614960736E-4 * x ** 14)

    if t < 0.0248 or t > 2.05:
        return np.nan
    return


def cal_UTC_1k_C12T(resistance):
    if resistance > 10393.0:
        return np.nan
    if resistance < 1312.0:
        return np.nan
    x = 10.0 - np.log(resistance - 900.0)
    t = np.exp(
        + 45.3365864301086
        - 279.642561075845 * x
        + 676.778403787487 * x ** 2
        - 906.341021564213 * x ** 3
        + 716.889032092528 * x ** 4
        - 307.885408127709 * x ** 5
        + 25.9388283393073 * x ** 6
        + 46.2285104814483 * x ** 7
        - 26.3795840825958 * x ** 8
        + 5.92575268688633 * x ** 9
        - 0.0561746958805483 * x ** 10
        - 0.292974257973497 * x ** 11
        + 0.0719916083446297 * x ** 12
        - 0.0076773027755517 * x ** 13
        + 3.23672511500012E-4 * x ** 14)

    if t < 0.02574 or t > 7.897:
        return np.nan
    return t


def cal_UTQ18(resistance):
    if resistance > 75000:
        return np.nan
    if resistance < 2600:
        return np.nan
    x = 11.2 - np.log(resistance - 1400)
    t = np.exp(
        -3.41561105286733
        + 1.12232262100456 * x
        - 0.424826792708624 * x ** 2
        + 0.773936136233403 * x ** 3
        - 1.30027361857579 * x ** 4
        + 2.31533923175192 * x ** 5
        - 3.80146857723503 * x ** 6
        + 4.6076088750048 * x ** 7
        - 3.78157095811825 * x ** 8
        + 2.08130218771598 * x ** 9
        - 0.768258026046223 * x ** 10
        + 0.187580821614454 * x ** 11
        - 0.0290504854757618 * x ** 12
        + 0.00258383342636628 * x ** 13
        - 1.00501530690684E-4 * x ** 14)
    if t < 0.035 or t > 6.2:
        return np.nan
    return t


def cal_ht1(x):
    if x < 4600:
        return np.nan
    t = 1.14239E10 * (np.log(-(4427.66529 - x) / 0.50214) ** (-1 / 0.1))
    if t < 1.7 or t > 300:
        return np.nan
    return t


def cal_ht2(x):
    if x < 4600:
        return np.nan
    t = 1.00019E10 * (np.log(-(4393.21183 - x) / 0.56481) ** (-1 / 0.1))
    if t < 1.7 or t > 300:
        return np.nan
    return t


def cal_ht3(x):
    if x < 4600:
        return np.nan
    t = 1.02639E10 * (np.log(-(4402.71193 - x) / 0.54942) ** (-1 / 0.1))
    if t < 1.7 or t > 300:
        return np.nan
    return t


def cal_generic_pt1000(x):
    return (cal_pt1000_Ch1_Baffle5(x) + cal_pt1000_Ch2_Baffle4(x)) / 2


def cal_pt1000_Ch1_Baffle5(x):
    if x < 105:
        return 5.74834 + 0.43974 * x ** 0.88354 + 4.11545 * np.log(x - 10.34234) + 3.42096 * np.tanh(
            x / (-8.85332 * (10 ** 14)) + 3.37344 * (10 ** 15))
    return cal_pt1000(x)


def cal_pt1000_Ch2_Baffle4(x):
    if x < 89.58:
        return 7.85391 + 0.451 * x ** 0.87903 + 4.0281 * np.log(x - 7.79381) - 2.19714 * np.tanh(
            x / (-2.36548 * (10 * 15)) - 7.27357 * (10 ** 19))
    return cal_pt1000(x)


def cal_pt1000(r):
    t = pt1000_temperature(r) + 273.15
    if t < 0:
        t = 9999
    return t


def cal_cam_cool(x):
    x = 11.2 - np.log(x - 1400)
    T = np.exp(-2.96106634147848 + -5.18089054649127 * x + 25.9564389751936 * x ** 2 - 67.919802323554 * x ** 3 +
               117.974122540099 * x ** 4 - 142.685187179576 * x ** 5 + 123.779073338133 * x ** 6 -
               78.2257644232516 * x ** 7 + 36.217633977666 * x ** 8 + -12.2416617747187 * x ** 9 +
               2.97848537774922 * x ** 10 - 0.506678458162558 * x ** 11 + 0.0570440155878966 * x ** 12 +
               -0.00380768004287375 * x ** 13 + 1.13699100097316E-4 * x ** 14)
    if T < 0.3:
        return np.nan
    return T


def cal_ser8(x):
    x = 11.2 - np.log(x - 1400)
    return np.exp(
        -70.2510845934072 + 431.958495397983 * x - 1243.35486928959 * x ** 2 + 2079.851674501 * x ** 3 - 2221.82752732689 * x ** 4 + 1569.15315029492 * x ** 5 - 725.225041039035 * x ** 6 + 201.344808133961 * x ** 7 + -21.1752645798767 * x ** 8 - 5.69301101480164 * x ** 9 + 2.35844703642311 * x ** 10 - 0.259954447641701 * x ** 11 - 0.0187741721390738 * x ** 12 + 0.00669498065063297 * x ** 13 - 4.39871175653045E-4 * x ** 14)


def cal_ser6(x):
    x = 11.2 - np.log(x - 1400)
    return np.exp(
        -418.66269190557 + 2030.22369066585 * x - 4302.49551086799 * x ** 2 + 5133.14952507189 * x ** 3 - 3719.23040793288 * x ** 4 + 1605.56403609629 * x ** 5 - 332.397935938044 * x ** 6 - 23.0801113001037 * x ** 7 + 26.8652824936315 * x ** 8 - 1.88491652328337 * x ** 9 - 2.21422793002565 * x ** 10 + 0.813246835982012 * x ** 11 - 0.129335143412473 * x ** 12 + 0.0100828066451444 * x ** 13 - 3.06270610070887E-4 * x ** 14)


# TODO: remove deprecated functions and migrate coded ones to json
functions = {"None": lambda x: x,
             "cal_RX202A": cal_RX202A,
             "cal_RX202A_ULT": cal_RX202A_ULT,
#             "cal_CHE5": cal_CHE5,
#             "cal_III": cal_III,
#             "cal_VII": cal_VII,
#             "cal_VIII": cal_VIII,
#             "cal_XII": cal_XII,
#             "cal_XIII": cal_XIII,
#             "cal_XIV": cal_XIV,
#             "cal_UTQ1": cal_UTQ1,
#             "cal_UTQ2": cal_UTQ2,
#             "cal_UTQ4": cal_UTQ4,
#             "cal_UTQ5": cal_UTQ5,
#             "cal_UTQ8": cal_UTQ8,
#             "cal_UTQ9": cal_UTQ9,
             "UTQ18":cal_UTQ18,
#             "cal_ht1": cal_ht1,
#             "cal_ht2": cal_ht2,
             "cal_ht3": cal_ht3,
             "cal_generic_pt1000": cal_generic_pt1000,
#             "cal_pt1000_Ch1_Baffle5": cal_pt1000_Ch1_Baffle5,
#             "cal_pt1000_Ch2_Baffle4": cal_pt1000_Ch2_Baffle4,
             "cal_pt1000": cal_pt1000,
#             "cal_cam_cool": cal_cam_cool,
#             "cal_ser8": cal_ser8,
#             "cal_ser6": cal_ser6,
             "cal_UTC1kB01": cal_UTC1kB01,
             "cal_UTC1kB02": cal_UTC1kB02,
             "cal_UTC1kC01": cal_UTC1kC01,
             "cal_UTQ13": cal_UTQ13,
             "cal_UTCC_1A": cal_UTCC_1A,
             "cal_UTCC_2A": cal_UTCC_2A,
             "UTC1k_C12T" : cal_UTC_1k_C12T,
             "UTC1k_C04": cal_UTC1kC04}


# returns the cal function for the given parameters
def to_function(parameters: dict):
    def func(resistance):
        if resistance < parameters["min_resistance"] or resistance > parameters["max_resistance"]:
            return np.nan
        x = parameters["rescale_0"] - np.log(resistance - parameters["rescale_1"])
        total = 0
        for i in range(len(parameters["func_params"])):
            total += parameters["func_params"][i] * x ** i
        t = np.exp(total)
        if t < parameters["min_temperature"] or t > parameters["max_temperature"]:
            return np.nan
        return t

    return func


# generates calibration functions from all json files in calibrations folder
def generate_functions_from_files():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "calibrations"))
    if not os.path.exists(path):
        print("no calibrations folder found")
        return

    for f in os.listdir(path):
        with open(os.path.join(path, f), "r") as file:
            if not file.name.endswith(".json"):
                continue
            s = "".join(file.readlines())
            params = json.loads(s)
        func = to_function(params)
        functions[params["name"]] = func


generate_functions_from_files()
