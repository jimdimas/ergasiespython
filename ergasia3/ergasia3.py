from urllib.request import urlopen
import json
from time import sleep,time
from datetime import date

#Functions

def date_init():  #Gets the date as a tuple and returns the array: [YEAR,MONTH,DAY]
    today=date.today()
    today=str(today)
    date_list=["","",""]
    i=0
    for char in today:
        if char=="-":
            i+=1
        else:
            date_list[i]+=char
    for i in range(3):
        date_list[i]=int(date_list[i])

    return date_list


def data_func(url): #Gets the JSON data from the OPAP API and returns it as a dictionary
    r=urlopen(url)
    html=r.read()
    html=html.decode()
    data=json.loads(html,strict=False)
    return data


#Main program

today=date_init()
statistics_list=[0 for i in range(81)] #A list that shows how many times each index number has appeared,for instance if statistics_list[1]=4,that means 1 appeared 4 times.
                                       #Note that for statistics_list,index 0 always has the price 0,as 0 isn't a number included in KINO numbers.

for i in range(today[2]):  #Looping through the number of days ,counting from today.
    """
    If the day or month is less than 10 as a number,we need to put it as 0X in the url,whereas X is a number between 1 and 9,because thats the way we will have access to the
    proper page.The url 'https://api.opap.gr/draws/v3.0/1100/draw-date/YEAR-MONTH-DAY/YEAR-MONTH-DAY/draw-id',whereas YEAR,MONTH and DAY is the same number in each appearance,
    returns a list containing all the individual draw id's of each draw.In that list,the element in index 0 is the draw id of the first draw of the particular day.
    """
    if today[1]<10:
        if today[2]-i>=10:
            url=f"https://api.opap.gr/draws/v3.0/1100/draw-date/{today[0]}-{0}{today[1]}-{today[2]-i}/{today[0]}-{0}{today[1]}-{today[2]-i}/draw-id"
        else:
            url=f"https://api.opap.gr/draws/v3.0/1100/draw-date/{today[0]}-{0}{today[1]}-{0}{today[2]-i}/{today[0]}-{0}{today[1]}-{0}{today[2]-i}/draw-id"
    else:
        if today[2]-i>=10:
            url=f"https://api.opap.gr/draws/v3.0/1100/draw-date/{today[0]}-{today[1]}-{today[2]-i}/{today[0]}-{today[1]}-{today[2]-i}/draw-id"
        else:
            url=f"https://api.opap.gr/draws/v3.0/1100/draw-date/{today[0]}-{today[1]}-{0}{today[2]-i}/{today[0]}-{today[1]}-{0}{today[2]-i}/draw-id"

    data=data_func(url) #Getting the list of the draw id's of a single day

    if data==[]: #If no draws on particular day
        print(f"No draws on {today[2]-i}/{today[1]}/{today[0]}\n")
        continue

    min_id=data[0] #Getting the first draw id of the day
    sleep(0.5) #We use this method in order not to do a lot of requests in a short period of time to the API,so we don't get our IP banned
    url=f"https://api.opap.gr/draws/v3.0/1100/{min_id}" #This url returns the info about the draw with the particular draw id.
    data=data_func(url)
    for number in data["winningNumbers"]["list"]:
        statistics_list[int(number)]+=1
    print(f"{today[2]-i}/{today[1]}/{today[0]}"+" Draw Id:"+f" {min_id}"+"\n"+f"{data['winningNumbers']['list']}")
    print("\n")

for i in range(1,81):
    print(f"Number {i} appeared {statistics_list[i]} times.")
