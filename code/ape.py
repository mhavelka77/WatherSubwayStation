# coding=utf8
import requests
import json
import time
from guizero import App, Text, Window, Box
from datetime import datetime

walkDelay = 5

def weatherCheck():
    request = requests.get("[request hidden]")
    received = json.loads(request.text)

    # Current Temperature

    currentTemp = round(received["current"]["temp"] - 273.15, 1)

    # Max temperature

    dayMax = 0
    for hour in received["hourly"]:
        if (hour["temp"] > dayMax):
            dayMax = hour["temp"]

    dayMax -= 273.15
    dayMax = round(dayMax, 1)
    
    # update view
    text.value = str(currentTemp)
    text2.value = str(dayMax)

def subwayCheck():
    request = requests.get("[request hidden]")
    received = json.loads(request.text) 
    arrTimes = []
    for departure in received:
        arrTime = departure["arrival_timestamp"]["predicted"].split("T")[1].split("+")[0]
        arrTime = arrTime[:-3]
        arrTimes.append(arrTime)
    m1.value = arrTimes[0]
    m2.value = arrTimes[1]
    m3.value = arrTimes[2]
    
    minutesAfterWalk = int(str(datetime.now().time()).split(":")[1]) + walkDelay
  

    if (int(arrTimes[0].split(":")[1]) > minutesAfterWalk):
        m1run.value = (int(arrTimes[0].split(":")[1]) - minutesAfterWalk) % 60
    else:
        m1run.value = (int(arrTimes[0].split(":")[1]) + 60) - minutesAfterWalk
    if (int(arrTimes[1].split(":")[1]) > minutesAfterWalk):
        m2run.value = int(arrTimes[1].split(":")[1]) - minutesAfterWalk
    else:
        m2run.value = (int(arrTimes[1].split(":")[1]) + 60) - minutesAfterWalk
    if (int(arrTimes[2].split(":")[1]) > minutesAfterWalk):
        m3run.value = int(arrTimes[2].split(":")[1]) - minutesAfterWalk
    else:
        m3run.value = (int(arrTimes[2].split(":")[1]) + 60) - minutesAfterWalk


app = App("Weather station")
window = Window(app, bg="black")
window.set_full_screen()

# grids
top_box = Box(window, width="fill", height=40, align="top")
tempBox_box = Box(window, width="fill", align="top")
fill1_box = Box(window, width="fill", align="top")
label1_box = Box(window, width="fill", align="top")
fill2_box = Box(window, width="fill", height=60, align="top")
subway_box = Box(window, width="fill", align="top")
fill3_box = Box(window, width="fill", align="top")
subwayRun_box = Box(window, width="fill", align="top")
fill4_box = Box(window, width="fill", align="top")

# first column 
fillLabel1 = Text(label1_box, text="", width=7, align="left")
filltemp1 = Text(tempBox_box, text="", width=8, align="left")
textLabel = Text(label1_box, text="Aktualni", font="Roboto", size=20, color="white", align="left")
text = Text(tempBox_box, text="", font="Roboto", color="green", size=30, align="left")

# second column 
fillLabel12 = Text(label1_box, text="", width=6, align="right")
filltemp12 = Text(tempBox_box, text="", width=8, align="right")
textLabel2 = Text(label1_box, text="Maximum", font="Roboto", size=20, color="white", align="right")
text2 = Text(tempBox_box, text="", font="Roboto", color="green", size=30, align="right")

# subway times
fillLabel12 = Text(subway_box, text="", width=2, align="left")
textLabel3 = Text(subway_box, text="M: ", font="Roboto", size=20, color="white", align="left")
m1 = Text(subway_box, text="19:30", font="Roboto", size=20, color="#825f00", align="left")
fillLabel13 = Text(subway_box, text="", width=6, align="left")
m2 = Text(subway_box, text="19:30", font="Roboto", size=20, color="#825f00", align="left")
fillLabel14 = Text(subway_box, text="", width=6, align="left")
m3 = Text(subway_box, text="19:30", font="Roboto", size=20, color="#825f00", align="left")


# subway run times
fillLabel22 = Text(subwayRun_box, text="", width=10, align="left")
m1run = Text(subwayRun_box, text="19:30", font="Roboto", size=30, color="#fc0303", align="left")
fillLabel23 = Text(subwayRun_box, text="", width=12, align="left")
m2run = Text(subwayRun_box, text="19:30", font="Roboto", size=30, color="#ff8324", align="left")
fillLabel24 = Text(subwayRun_box, text="", width=11, align="left")
m3run = Text(subwayRun_box, text="19:30", font="Roboto", size=30, color="green", align="left")


text.repeat(1000 * 60 * 30, weatherCheck)
m1.repeat(1000 * 30, subwayCheck)
app.display()
