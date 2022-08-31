
import json
import requests
import csv
import argparse

url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
parser = argparse.ArgumentParser()
parser.add_argument('--website', type=str, required=True)
parser.add_argument('--strategy', type=str, required=True, help= " Enter mobile or desktop or both")
parser.add_argument('--outputfilename', type=str)
args = parser.parse_args()

def requireddata(params):
    response = requests.get(url,params=params)
    data = response.json() 
    date_time = response.json()["lighthouseResult"]["fetchTime"]
    mobile_desktop = response.json()["lighthouseResult"]["configSettings"]["formFactor"]
    performance= response.json()["lighthouseResult"]["categories"]["performance"]["score"] * 100
    fcp = response.json()["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"]/1000
    lcp = response.json()["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
    interactive_time = response.json()["lighthouseResult"]["audits"]["interactive"]["score"]
    speed_index = response.json()["lighthouseResult"]["audits"]["speed-index"]["score"]
    cls = response.json()["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100
    tbt = response.json()["lighthouseResult"]["audits"]["total-blocking-time"]["score"]

    fields = ["date-time", "mobile/desktop", "performance","fcp","lcp","interactive-time","speed", "cls", "tbt"]
    rows = [date_time, mobile_desktop, performance, fcp, lcp, interactive_time, speed_index, cls, tbt]
    
    if args.outputfilename:
        filename = args.outputfilename+"."+"csv"
        with open(filename, "a") as file:
            csvwriter = csv.writer(file) 
            csvwriter.writerow(fields)
            csvwriter.writerow(rows)
    else:
        with open("pagespeedData.csv","a") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(fields)
            csvwriter.writerow(rows)
    # with open("record.json", "w") as f:
    #     json.dump(data,f,indent=4)

if args.strategy == "mobile" or args.strategy == "desktop":
    paramtr = {"url": args.website,
    "category":["performance","accessibility"],
    "strategy":args.strategy
    }
    requireddata(paramtr)

else:
    print("Please enter strategy.... ")
