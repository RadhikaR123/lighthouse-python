import json
import requests
import csv
import time

url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
website = input("Enter the website URL : ")
strategy = input("please enter strategy, mobile or desktop : ")
OutputfileName = input("Enter the file name: ")

def requireddata(params):
    response = requests.get(url,params=params)
    time.sleep(60)
    data = response.json() 
    with open("record.json", "w") as f:
        json.dump(data,f,indent=4)
    time.sleep(5)
    date_time = data["lighthouseResult"]["fetchTime"]
    mobile_desktop = data["lighthouseResult"]["configSettings"]["formFactor"]
    performance= data["lighthouseResult"]["categories"]["performance"]["score"] * 100
    fcp = data["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
    lcp = data["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
    interactive_time = data["lighthouseResult"]["audits"]["interactive"]["score"]
    speed_index = data["lighthouseResult"]["audits"]["speed-index"]["score"]
    cls = data["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100
    tbt = data["lighthouseResult"]["audits"]["total-blocking-time"]["score"]

    fields = ["date-time", "mobile/desktop", "performance","fcp","lcp","interactive-time","speed", "cls", "tbt"]
    rows = [date_time, mobile_desktop, performance, fcp, lcp, interactive_time, speed_index, cls, tbt]
    
    if OutputfileName:
        filename = OutputfileName+"."+"csv"
        with open(filename, "a") as file:
            csvwriter = csv.writer(file) 
            csvwriter.writerow(fields)
            csvwriter.writerow(rows)
    else:
        with open("pagespeedData.csv","a") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(fields)
            csvwriter.writerow(rows)

if strategy.lower() == "mobile" or strategy.lower() == "desktop":
    paramtr = {"url": website,
    "category":["performance","accessibility"],
    "strategy":strategy
    }
    requireddata(paramtr)
else:
    print("Please enter strategy......")
