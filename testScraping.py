import requests
from bs4 import BeautifulSoup

# get attractions in a specific city recommended by TripAdvisor
# def GetAttractionList():
#     URL = "https://www.tripadvisor.com/Attractions-g28953-Activities-a_allAttractions.true-New_York.html"
#     attractionPage = requests.get(URL)
#     soup=BeautifulSoup(attractionPage.content,'lxml')
#     for item in soup.find_all('div', {'class':'fkUsL z'}):
#         print(item.text)
#         try:	
#             # if item.find('h3'):
#                 # name = item.find('h3').text
#                 # print(name)
#                 # features = item.find_all('div', {'class':'WlYyy diXIH fPixj'})
#                 # featureList = []
#                 # for feature in features:
#                 #     featureList.append(feature.text)
#                 #     print(feature.text)
#                 # price = item.find('p').text.count('$')
#                 # print(price)
#                 print('------------------')
#         except Exception as e:
#             print("Error")
#             raise e
#             return None


# get attractions in a specific city recommended by USNews travel
# def getAttractionList():
#     URL = "https://travel.usnews.com/New_York_NY/Things_To_Do/"
#     attractionPage = requests.get(URL)
#     rsoup=BeautifulSoup(attractionPage.content,'lxml')
#     print(rsoup.text)
#     for item in soup.find_all('div', {'class':'mb5'}):
#         try:	
#             if item.find('h5'):
#                 name = item.find('h5').text
#                 print(name)
#                 features = item.find_all('div', {'class':'WlYyy diXIH fPixj'})
#                 featureList = []
#                 for feature in features:
#                     featureList.append(feature.text)
#                     print(feature.text)
#                 price = item.find('p').text.count('$')
#                 print(price)
#                 print('------------------')

#         except Exception as e:
#             print("Error")
#             raise e
#             return None

class attractions(object):
        def __init__(self, name, time, costStr):
            self.name = name
            self.time = time
            self.costText = costStr
            self.status = True    # if this attraction is in current plan
            self.cost = float(self.costText[1:])

def getAttractionTime(timeStr):
    time = 0
    splitedTime = timeStr.split(' ')
    if timeStr.find('minutes') != -1 and timeStr.find('hour') == -1:
        time = 1
    elif timeStr.find('hour') != -1 and timeStr.find('minutes') != -1 and timeStr.find('hour') < timeStr.find('minutes'):
        time = int(splitedTime[0]) + 1
    elif timeStr.find('hour') != -1 and timeStr.find('minutes') != -1 and timeStr.find('hour') > timeStr.find('minutes'):
        time = 1
    elif timeStr.find('hour') != -1 and timeStr.find('minutes') == -1:
        time = int(splitedTime[0])
    return time


def addAttractions(city):
    URL = "https://www.viator.com/New-York-City/d687-ttd"
    attractionPage = requests.get(URL)
    soup=BeautifulSoup(attractionPage.content,'lxml')
    attractionList = []
    for item in soup.find_all('div', {'class':'product-card-inner-row row m-0'}):
        try:	
            if item.find('h2'):
                name = item.find('h2').text.strip()
                print(name)
                timeStr = item.find('span', {'class':'pr-1 px-1 align-middle product-card-footer-text'}).text.strip()
                
                print(timeStr)
                time = getAttractionTime(timeStr)
                print(time)
                costStr = item.find('div', {'class':'h3'}).text.strip()
                #print(costStr)
                cost = float(costStr[1:])
                #print(cost)
                # if time.find('days') == -1 and name.find('transfer') == -1:
                #     attractionList.append(attractions(name,timeStr,costStr))
                print('------------------')

        except Exception as e:
            raise e
    # print(attractionList[11].name) 
    # attractionsSorted = sorted(attractionList, key=lambda x: x.cost)
    # for i in attractionsSorted:
    #     print(i.name)
    #     print(i.cost)
    #     print('------------------')

# add (pages*10) recommended restaurants to app.restaurants
def addMoreRestaurants(city, pages):
    for page in range(pages):
        add10Restaurants(city, page*10)


# get 10 restaurants in a specific city recommended by Yelp
def add10Restaurants(city, start):
    # Learned from here https://www.proxiesapi.com/blog/scraping-yelp-data-with-python-and-beautiful-soup.html.php
    URL = f"https://www.yelp.com/search?find_desc=Restaurants&find_loc={city}&start={start}"
    restaurantPage = requests.get(URL)
    soup=BeautifulSoup(restaurantPage.content,'lxml')

    restaurantList = []

    for item in soup.select('[class*=container]'):
        try:	
            name_element = item.find('h4')
            if name_element:
                name = name_element.text.strip()
                print(name)

                features = item.find_all('button')
                featureList = []
                for feature in features:
                    featureList.append(feature.text.strip())
                print (featureList)

                costStr = item.find('p').text.strip()
                print(costStr)
                moneyChara = ''
                for c in costStr:
                    if c == '$' or c == '€' or c == '£':
                        moneyChara = moneyChara+c
                
                print(repr((moneyChara)))
                
                #restaurantList.append(restaurants(name, featureList, cost))
                print('------------------')
        except Exception as e:
            print("Restaurant Info Not Found")


#addAttractions('New York')
# addMoreRestaurants('London', 1)



# https://www.viator.com/London-tours/Tours-and-Sightseeing/d737-g12
# https://www.viator.com/London-tours/Kid-Friendly/d737-g21
# https://www.viator.com/London-tours/Art-and-Culture/d737-tag21910

# https://www.viator.com/New-York-City/d687-ttd
# https://www.viator.com/New-York-City-tours/Tours-and-Sightseeing/d687-g12
# https://www.viator.com/New-York-City-tours/Kid-Friendly/d687-g21
# https://www.viator.com/New-York-City-tours/Art-and-Culture/d687-tag21910

# https://www.viator.com/Beijing/d321-ttd
# https://www.viator.com/Beijing-tours/Tours-and-Sightseeing/d321-g12
# https://www.viator.com/Beijing-tours/Kid-Friendly/d321-g21
# https://www.viator.com/Beijing-tours/Art-and-Culture/d321-tag21910


# remove those ones with "transfer" in name
# ones with "days" in time duration




#https://www.kayak.com/hotels/New-York,United-States-c15830/2021-12-02/2021-12-17/1adults?sort=rank_a

def addHotels():
    URL = "https://www.kayak.com/hotels/New-York,United-States-c15830/2021-12-02/2021-12-17/1adults?sort=rank_a"
    hotelPage = requests.get(URL)
    soup=BeautifulSoup(hotelPage.content,'lxml')
    print(soup.text)
    for item in soup.find_all('div', {'class':'kzGk-resultInner'}):
        try:	
            print(item.text)
            # if item.find('div',{'class':'FLpo-big-name'}):
                # name = item.find('div',{'class':'FLpo-big-name'}).text.strip()
                # print(name)
                # timeStr = item.find('span', {'class':'pr-1 px-1 align-middle product-card-footer-text'}).text.strip()
                
                # print(timeStr)
                # time = getAttractionTime(timeStr)
                # print(time)
                # costStr = item.find('div', {'class':'h3'}).text.strip()
                # #print(costStr)
                # cost = float(costStr[1:])
                # #print(cost)
                # # if time.find('days') == -1 and name.find('transfer') == -1:
                # #     attractionList.append(attractions(name,timeStr,costStr))
                # print('------------------')

        except Exception as e:
            raise e

addHotels()