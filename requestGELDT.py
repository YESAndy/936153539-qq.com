import requests
import sys
import json
from urllib.request import urlopen
import re
import csv


# get data
def get_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        print("response successfully")
        
        try:
            json_content = json.loads(response.content)
            try:
                print(json_content['query_details'])
                timeline = json_content['timeline']
                data = timeline[0]['data']
                print(data)
                return data
            # don't know what error..
            except KeyError:
                print(json_content)
                return None
        # can not receive a valid json file
        except ValueError:
            print("fail to load {}'s data".format(name))
            return None


# set up output file
outputfilename = "output.csv"
summaryfilename = "summary.csv"
outputfile = open(outputfilename, 'w', newline='')
summaryfile = open(summaryfilename, 'w', newline='')
output_writer = csv.writer(outputfile, delimiter=",")
summary_writer = csv.writer(summaryfile, delimiter=",")

# get country name
country_file = open("country_list.txt", 'r')
country_list = []
countryName = []
for row in country_file:
    result = ''
    for s in row[3:].strip().split(' '):
        result += s
    country_list.append(result.lower())
    countryName.append(row.strip()[3:])

# read tone data
output_writer.writerow(["date_vol", "date_tone", "averge volume", "average tone"])
for country, name in zip(country_list, countryName):
    averagetone = 0
    totalvol = 0
    # for every country
    output_writer.writerow([name, " ", " ", " "])
    url_tone = "https://api.gdeltproject.org/api/v2/doc/doc?query=%22belt%20and%20road%22%20%22rules%22%20sourcecountry:{}&mode=timelinetone&startdatetime=20200101000000&enddatetime=20200323000000&sort=datedesc&format=JSON".format(country)
    url_vol = "https://api.gdeltproject.org/api/v2/doc/doc?query=%22belt%20and%20road%22%20%22rules%22%20sourcecountry:{}&mode=timelinevolraw&startdatetime=20200101000000&enddatetime=20200323000000&sort=datedesc&format=JSON".format(country)
    data_tone = get_data(url_tone)
    data_vol = get_data(url_vol)
    # calculate and write their total volumes and average tones
    if data_tone and data_vol:
        for tone, vol in zip(data_tone, data_vol):
            output_writer.writerow([vol['date'], tone['date'], vol['value'], tone['value']])
            averagetone += float(vol['value']) * float(tone['value'])
            totalvol += float(vol['value'])
        averagetone /= totalvol
        summary_writer.writerow([name, str(totalvol), str(averagetone)])
    else:# missing value
        summary_writer.writerow([name, "missing", "missing"])



