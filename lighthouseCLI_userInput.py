
import json
import os
import pandas as pd
from datetime import datetime
import time

df = pd.DataFrame([], columns=['URL','SEO','Accessibility','Performance','Best Practices'])
name = input("Enter file name: ")
getdate = datetime.now().strftime("%m-%d-%y")
choic = input("Enter strategy: mobile or desktop- ")
NumOfURLs= int(input("Enter the number of URLs: "))
urls = []
i=0 
while i<=NumOfURLs:
    a= input("Enter URL: ")
    urls.append(a)
    i+=1

j=0
for url in urls:
    j+=1    
    stream = os.popen('lighthouse --quiet --no-update-notifier --screenEmulation.disabled=true --no-enable-error-reporting --output=json --output-path='+name+str(j)+'_'+getdate+'.report.json --chrome-flags="--headless" ' + url +" " + '--form-factor=' + choic )
    time.sleep(90)
    print("Report complete for: " + url)

    json_filename = name+str(j) + '_' + getdate + '.report.json'

    with open(json_filename, encoding= "utf_8") as json_data:
        loaded_json = json.load(json_data)

    seo = str(round(loaded_json["categories"]["seo"]["score"] * 100))
    accessibility = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
    performance = str(round(loaded_json["categories"]["performance"]["score"] * 100))
    best_practices = str(round(loaded_json["categories"]["best-practices"]["score"] * 100))

    date_time = loaded_json["fetchTime"]
    mobile_desktop = loaded_json["configSettings"]["formFactor"]
    fcp = loaded_json["audits"]["first-contentful-paint"]["displayValue"]
    lcp = loaded_json["audits"]["largest-contentful-paint"]["displayValue"]
    interactive_time = loaded_json["audits"]["interactive"]["displayValue"]
    speed_index = loaded_json["audits"]["speed-index"]["displayValue"]
    cls = loaded_json["audits"]["cumulative-layout-shift"]["displayValue"]
    tbt = loaded_json["audits"]["total-blocking-time"]["displayValue"]

    dict = {"URL":url,"SEO":seo,"Accessibility":accessibility,"Performance":performance,"Best Practices":best_practices,"Date-time":date_time,"strategy":mobile_desktop, "fcp":fcp,"lcp":lcp,"interactive-time":interactive_time,"speed-index":speed_index,"cls":cls,"tbt":tbt}
    df = df.append(dict, ignore_index=True)

    df.to_csv(name+str(j) + '_' + getdate + '.csv')
    print(df)


