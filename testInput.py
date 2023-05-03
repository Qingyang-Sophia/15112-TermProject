#################################################
# TP0.py
#
# Your name: Qingyang Cao
# Your andrew id: qingyanc
#################################################

from cmu_112_graphics import *
import math, os
import copy

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
# from PIL import Image
import textwrap



# return the number of days between two dates
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y/%m/%d")
    d2 = datetime.strptime(d2, "%Y/%m/%d")
    return abs((d2 - d1).days)

# return a list of strings of dates between d1 and d2
def date_between(d1, d2):
    startDate = datetime.strptime(d1, "%Y/%m/%d")
    days = days_between(d1, d2)
    startDateStr = str(startDate.year) + '/' + str(startDate.month) + '/' + str(startDate.day)
    dateList = [startDateStr]
    for day in range(days):
        nextDate = startDate + timedelta(days=1)
        nextDateStr = str(nextDate.year) + '/' + str(nextDate.month) + '/' + str(nextDate.day)
        dateList.append(nextDateStr)
        startDate = nextDate
    return dateList


def getScreenSize():
    fullScreenWidth = 1440
    fullScreenHeight = 770
    return (fullScreenWidth, fullScreenHeight)

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
        time = min(int(splitedTime[0]),8)
    return time



class restaurants(object):
        def __init__(self, name, features, cost):
            self.name = name
            self.features = features
            self.cost = cost
            self.time = 1
            self.start = (-1,-1)

            self.clickedInPlan = False
            self.clickedInBar = False

class attractions(object):
        def __init__(self, name, timeStr, costStr,type):
            self.name = name
            self.timeStr = timeStr
            self.time = getAttractionTime(timeStr)
            self.costStr = costStr
            self.cost = float(self.costStr[1:])
            #self.type = type
            
            self.start = (-1,-1)
            self.positionList = []

            self.clickedInPlan = False
            self.clickedInBar = False
            
        

        

        
def make2DList(cols, rows):
    return [[None]*rows for col in range(cols)]
        
def getTotalPages(limit, number):
    if number <= limit:
        return 1
    else:
        return math.ceil(number/limit)

def appStarted(app):
    resetAll(app)

def resetAll(app):

    app.mode = 'mapMode'
    app.cityCodeDict = {'New York City':'d687', 'London':'d737', 'Los Angeles':'d645', 'San Francisco':'d651',
                        'Paris': 'd479', 'Munich': 'd487', 'Sydney':'d357', 'Taipei':'d5262', 'Vienna':'d454'}

    app.restaurantSearchDict = {'Vienna':'Vienna Austria'}
    app.dates = []
    app.days = 0
    # app.dates = date_between('2021/11/23','2021/11/28')
    # app.days = days_between('2021/11/23','2021/11/28') +1
    app.city = "" # 'New York City' 'London'  'Beijing'
    app.budget = 700
    app.attractionType = '' # 'All' 'Tours and Sightseeing' 'Kid Friendly' 'Art and Culture'
    app.numOfTravelers = 1

    app.totalCost = 0

    app.attractions = []
    app.selectedAttractions_cost = []
    app.selectedAttractions_time = []
    
    app.clickedAttractionInPlan = None

    app.clickedAttractionInBar = None

    app.restaurants = []

    app.hotels = []

    app.plan = []
    app.planRows, app.planCols, app.cellWidth, app.cellHeight, app.plan_x0, app.plan_y0, app.plan_x1, app.plan_y1 = getPlanDimensions(app)
    app.planArrow_y0,app.planArrow_y1,app.planLeftArrow_x0,app.planLeftArrow_x1,app.planRightArrow_x0,app.planRightArrow_x1 = getPlanArrowDimentions()
    app.barRows, app.barHeight, app.bar_x0, app.bar_y0, app.bar_x1, app.bar_y1, app.side_x0, app.side_y0, app.side_x1, app.side_y1 = getSideDimensions(app) 
    app.sideArrow_x0,app.sideArrow_x1,app.sideArrow_x2,app.sideUpArrow_y0,app.sideUpArrow_y1,app.sideDownArrow_y0,app.sideDownArrow_y1 = getSideArrowDimentions(app)


    app.planPage = 0
    app.planTotalPages = getTotalPages(7, app.days)

    app.attractionPage = 0
    app.attractionTotalPages = getTotalPages(10, len(app.attractions))

    app.restaurantPage = 0
    app.restaurantTotalPages = getTotalPages(10, len(app.restaurants))

    app.hotelPage = 0
    app.hotelTotalPages = getTotalPages(10, len(app.hotels))
    
      
    app.sideType = 'Attraction' # 'Attraction'  'Restaurant' 'Hotel'
    app.attractionBgColor = 'lemonchiffon'   #'tan' when clicked  'wheat' available in bar or in plan   'lemonchiffon' bg   'white' unavailable
    app.restaurantBgColor = 'thistle'        # 'blueviolet' when clicked   'mediumorchid' available in bar or in plan   'thistle' bg   'white' unavailable
    app.hotelBgColor = 'honeydew'     #  'olivedrab' when clicked    'yellowgreen' not clicked       'honeydew' bg



    app.fullScreenSize = getScreenSize()

    # load image
    # Source: https://www.reddit.com/r/photoshopbattles/comments/ilxstl/psbattle_a_bluefooted_booby/
    app.imageBooby = app.scaleImage(app.loadImage('images/booby.png'),1/5)
    


    
    e = Entry(app)
    

    
    
#####################################
# Begin Mode
#####################################   

def beginMode_mousePressed(app,event):
    if 650 <= event.x <= 850 and 450 <= event.y <= 530:
        app.mode = 'introMode'

def beginMode_redrawAll(app, canvas):
    # draw title
    canvas.create_text(600,250,text='Blue-Footed BOOBY', fill='dodgerblue',font='Helvetica 90 bold')
    canvas.create_text(740,300,text='Visit A City', fill='royalblue',font='Helvetica 80 bold')
    # draw the begin button
    canvas.create_rectangle(650, 450, 650+200,450+80, fill = 'deepskyblue', outline = 'black', width = 3)
    canvas.create_text(750,490,text='Begin',fill = 'black', font='Helvetica 40 bold' )

    canvas.create_image(650, 550, anchor = SE, image=ImageTk.PhotoImage(app.imageBooby))


#####################################
# Intro Mode
#####################################

def introMode_mousePressed(app,event):
    if 1200 <= event.x <= 1400 and 670 <= event.y <= 740:
        app.mode = 'mapMode'


def introMode_redrawAll(app, canvas):
    canvas.create_text(720,80,text='Introduction', fill='royalblue',font='Helvetica 50 bold')
    canvas.create_text(720,150,text='>< Introduction waiting to be written......', fill='black',font='Helvetica 30 bold')
    # draw Continue button
    canvas.create_rectangle(1200,670,1400,740,fill = 'deepskyblue', outline = 'black', width = 3)
    canvas.create_text(1300,705, text='Continue',fill = 'black',  font='Helvetica 40 bold' )



#####################################
# Map Mode     (Declare Preferences)
#####################################

def mapMode_mousePressed(app, event):
    
    #if clicked on date button
    if 120 <= event.x <= 360 and 80 <= event.y <= 130:
        date = app.getUserInput('When do you plan to travel? \n yyyy/mm/dd-yyyy/mm/dd')
        while date == None:
            date = app.getUserInput('Please enter the date \n yyyy/mm/dd-yyyy/mm/dd')
        d1 = date.split('-')[0]
        d2 = date.split('-')[1]
        try:
            app.days = days_between(d1, d2) +1
            app.dates = date_between(d1, d2)
            app.plan = make2DList(app.days, 8)
            app.planRows, app.planCols, app.cellWidth, app.cellHeight, app.plan_x0, app.plan_y0, app.plan_x1, app.plan_y1 = getPlanDimensions(app)
            app.planTotalPages = getTotalPages(7, app.days)
        except:
            date = app.getUserInput('Invalid date! Please try again \n yyyy/mm/dd-yyyy/mm/dd')

    #if clicked on budget button
    if 120 <= event.x <= 360 and 150 <= event.y <= 200:
        budget = app.getUserInput('What is your budget?')
        app.budget = float(budget)
    
    # if clicked on city
    if 350 <= event.x <= 450 and 225 <= event.y <= 265:
        app.city = 'New York City'
    if 470 <= event.x <= 570 and 225 <= event.y <= 265:
        app.city = 'London'
    if 590 <= event.x <= 690 and 225 <= event.y <= 265:
        app.city = 'Beijing'
    if 710 <= event.x <= 810 and 225 <= event.y <= 265:
        app.city = 'Los Angeles'

    # if clicked on type  #'All' 'Tours and Sightseeing' 'Kid Friendly' 'Art and Culture'
    if 350 <= event.x <= 550 and 295 <= event.y <= 335: 
        app.attractionType = 'All'
    if 600 <= event.x <= 800 and 295 <= event.y <= 335: 
        app.attractionType = 'Art and Culture'
    if 850 <= event.x <= 1050 and 295 <= event.y <= 335: 
        app.attractionType = 'Tours and Sightseeing'
    if 1100 <= event.x <= 1300 and 295 <= event.y <= 335: 
        app.attractionType = 'Kid Friendly'
    
    # if clicked on generate button
    if 1200 <= event.x <= 1400 and 670 <= event.y <= 740: 
        addMoreRestaurants(app, 2)
        addAttractions(app)     
        app.attractionTotalPages = getTotalPages(10, len(app.attractions))
        app.restaurantTotalPages = getTotalPages(10, len(app.restaurants))
        app.hotelTotalPages = getTotalPages(10, len(app.hotels))

    # add a function to check if the budget is too little to generate a plan
    # maybe move to an errorMode
        generateOriginalPlan(app)
        app.mode = 'planMode'

def mapMode_keyPressed(app, canvas):
    print("keyPressed mapMode")
    pass


def mapMode_redrawAll(app, canvas):
    # draw the date button
    canvas.create_rectangle(120,80,360,130,fill = 'deepskyblue', outline = 'black', width = 3)
    canvas.create_text(240,105, text='Click to enter travel date',fill = 'black',  font='Helvetica 20 bold' )
    # draw the budget button
    canvas.create_rectangle(120,150,360,200,fill = 'deepskyblue', outline = 'black', width = 3)
    canvas.create_text(240,175, text='Click to enter budget',fill = 'black',  font='Helvetica 20 bold' )
    # draw the city buttons
    canvas.create_text(240,245,text='Choose a city', fill = 'black', font='Helvetica 20 bold')

    # New York
    ny_color = 'royalblue' if app.city == 'New York City' else 'dodgerblue'
    canvas.create_rectangle(350,225,450,265,fill = ny_color , outline = 'black', width = 3)
    canvas.create_text(400,245,text='New York', fill='black',font='Helvetica 15')
    # London
    london_color = 'royalblue' if app.city == 'London' else 'dodgerblue'
    canvas.create_rectangle(470,225,570,265,fill = london_color, outline = 'black', width = 3)
    canvas.create_text(520,245,text='London', fill='black',font='Helvetica 15')
    # Beijing
    bj_color = 'royalblue' if app.city == 'Beijing' else 'dodgerblue'
    canvas.create_rectangle(590,225,690,265,fill = bj_color, outline = 'black', width = 3)
    canvas.create_text(640,245,text='Beijing', fill='black',font='Helvetica 15')
    # Los Angeles
    la_color = 'royalblue' if app.city == 'Los Angeles' else 'dodgerblue'
    canvas.create_rectangle(710,225,810,265,fill = la_color, outline = 'black', width = 3)
    canvas.create_text(760,245,text='Los Angeles', fill='black',font='Helvetica 15')

    # draw the types
    canvas.create_text(240,315,text='Choose a type', fill = 'black', font='Helvetica 20 bold')
    # All
    all_color = 'royalblue' if app.attractionType == 'All' else 'dodgerblue'
    canvas.create_rectangle(350,295,550,335,fill = all_color, outline = 'black', width = 3)
    canvas.create_text(450,315,text='All', fill='black',font='Helvetica 15')
    # Art and Culture
    ac_color = 'royalblue' if app.attractionType == 'Art and Culture' else 'dodgerblue'
    canvas.create_rectangle(600,295,800,335,fill = ac_color, outline = 'black', width = 3)
    canvas.create_text(700,315,text='Art and Culture', fill='black',font='Helvetica 15')
    # Tours and Sightseeing
    ts_color = 'royalblue' if app.attractionType == 'Tours and Sightseeing' else 'dodgerblue'
    canvas.create_rectangle(850,295,1050,335,fill = ts_color, outline = 'black', width = 3)
    canvas.create_text(950,315,text='Tours and Sightseeing', fill='black',font='Helvetica 15')
    # Kid Friendly
    kf_color = 'royalblue' if app.attractionType == 'Kid Friendly' else 'dodgerblue'
    canvas.create_rectangle(1100,295,1300,335,fill = kf_color, outline = 'black', width = 3)
    canvas.create_text(1200,315,text='Kid Friendly', fill='black',font='Helvetica 15')
    
    
    canvas.create_rectangle(1200,670,1400,740,fill = 'deepskyblue', outline = 'black', width = 3)
    canvas.create_text(1300,705, text='Generate',fill = 'black',  font='Helvetica 40 bold')





# get one page of attractions in a specific city recommended by Viator
def addAttractions(app):
    cityName = app.city.replace(' ', '-')
    cityCode = app.cityCodeDict[app.city]
# URL examples:
# https://www.viator.com/New-York-City/d687-ttd
# https://www.viator.com/New-York-City-tours/Tours-and-Sightseeing/d687-g12
# https://www.viator.com/New-York-City-tours/Art-and-Culture/d687-tag21910
# https://www.viator.com/New-York-City-tours/Kid-Friendly/d687-g21
    if app.attractionType == 'All':
        suffix = f'{cityName}/{cityCode}-ttd'
    elif app.attractionType == 'Tours and Sightseeing':
        suffix = f'{cityName}-tours/Tours-and-Sightseeing/{cityCode}-g12'
    elif app.attractionType == 'Art and Culture':
        suffix = f'{cityName}-tours/Art-and-Culture/{cityCode}-tag21910'
    elif app.attractionType == 'Kid Friendly':
        suffix = f'{cityName}-tours/Kid-Friendly/{cityCode}-g21'

    URL = f'https://www.viator.com/{suffix}?sortType=rating'
    attractionPage = requests.get(URL)
    soup=BeautifulSoup(attractionPage.content,'lxml')

    for item in soup.find_all('div', {'class':'product-card-inner-row row m-0'}):
        try:	
            if item.find('h2'):
                name = item.find('h2').text.strip()
                timeStr = item.find('span', {'class':'pr-1 px-1 align-middle product-card-footer-text'}).text.strip()
                costStr = item.find('div', {'class':'h3'}).text.strip()
                if timeStr.find('days') == -1 and name.find('Transfer') == -1:
                    app.attractions.append(attractions(name,timeStr,costStr,app.attractionType))
                
        except Exception as e:
            raise e
    app.attractions = sorted(app.attractions, key=lambda x: x.cost)
    
    

# add (pages*10) recommended restaurants on Yelp to app.restaurants
def addMoreRestaurants(app, pages):
    for page in range(pages):
        add10Restaurants(app, page*10)

# get 10 restaurants in a specific city recommended by Yelp
def add10Restaurants(app, start):
    if app.city in app.restaurantSearchDict:
        searchCity = app.restaurantSearchDict[app.city]
    else:
        searchCity = app.city

    # based on budget----
    budgetFilter = ''
    budgetPerDay = app.budget/app.days
    if budgetPerDay < 300:
        budgetFilter = '&attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2'
    elif budgetPerDay >= 300:
        budgetFilter = '&attrs=RestaurantsPriceRange2.3,RestaurantsPriceRange2.4'

    # Learned from here https://www.proxiesapi.com/blog/scraping-yelp-data-with-python-and-beautiful-soup.html.php
    URL = f"https://www.yelp.com/search?find_desc=Restaurants&find_loc={searchCity}{budgetFilter}&start={start}"
    restaurantPage = requests.get(URL)
    soup=BeautifulSoup(restaurantPage.content,'lxml')

    for item in soup.select('[class*=container]'):
        try:	
            name_element = item.find('h4')
            if name_element:
                name = name_element.text.strip()

                features = item.find_all('button')
                featureList = []
                for feature in features:
                    featureList.append(feature.text.strip())
                
                costStr = item.find('p').text.strip()
                cost = ''
                for c in costStr:
                    if c == '$' or c == '€' or c == '£':
                        cost = cost+c
                newRestaurant = restaurants(name, featureList, cost)
                app.restaurants.append(newRestaurant)
                
        except Exception as e:
            raise e

# generate an original List of Attractions based on budget and days
def generateOriginalListOfAttractions(app):
    numOfAttractions = len(app.attractions)
    leastNum = (app.days - 1)*2
    if numOfAttractions <= leastNum:
        app.selectedAttractions_cost = app.attractions
        return
    
    i = 0
    money = 0
    while money <= app.budget and i <= numOfAttractions-leastNum:   
        money = 0
        for j in range(i, i+leastNum):
            money += app.attractions[j].cost
        i += 1
    if money > app.budget:
        if i == 1:
            totalCost = 0
            i = 0
            while totalCost < app.budget:
                app.selectedAttractions_cost.append(app.attractions[i])
                totalCost += app.attractions[i].cost
                i += 1

        elif i > 1:
            app.selectedAttractions_cost = app.attractions[i-2:i-2+leastNum]
    elif i > numOfAttractions-leastNum: 
        app.selectedAttractions_cost = app.attractions[numOfAttractions-leastNum:]


# The first selective algorithm version
# def generateOriginalPlan(app):
#     selectedInTime = sorted(app.selectedAttractions_cost, key=lambda x: x.time)
#     numOfAttractions = len(app.selectedAttractions_cost)
#     for i in range(app.days-2):
#         selectedInTime[i].start = (i, 0)
#         selectedInTime[numOfAttractions-3-i].start = (i, 3)
#     selectedInTime[numOfAttractions-2].start = (app.days-2, 0)
#     selectedInTime[numOfAttractions-1].start = (app.days-1, 0)
#     # put attractions into app.plan, put the positions into positionList of each selected attraction
#     for attraction in app.selectedAttractions_cost:
#         startCol, startRow = attraction.start
#         for hour in range(attraction.time):
#             if (startRow+hour) < 8:
#                 app.plan[startCol][startRow+hour] = attraction
#                 attraction.positionList.append((startCol, startRow+hour))



def isLegalToPutIn(app, position, attraction):
    col, row = position
    if app.plan[col][row] != None:
        return False
    else:
        hour = 0
        r = row
        while r < 8 and app.plan[col][r] == None:
            hour += 1
            r += 1
        if hour >= attraction.time:
            return True
        else:
            return False

def isSolution(app):
    for attraction in app.selectedAttractions_time:
        if attraction.start == (-1, -1):
            return False
    return True

def colWithMostEmptyCell(app):
    mostCol = None
    mostNum = 0
    for col in range(app.days):
        r = 7
        num = 0
        while r >= 0 and app.plan[col][r] == None:
            num += 1
            r -= 1
        if num == 8:
            return col       
        elif num >= mostNum:
            mostNum = num
            mostCol = col
    return mostCol

def putAttractionInPlan(app,position,attraction):
    startCol, startRow = position
    attraction.start = (startCol, startRow)
    for hour in range(attraction.time):
        app.plan[startCol][startRow+hour] = attraction
        attraction.positionList.append((startCol, startRow+hour))

def removeAttractionFromPlan(app, attraction):
    startCol, startRow = attraction.start
    attraction.start = (-1,-1)
    for hour in range(attraction.time):
        app.plan[startCol][startRow+hour] = None
    attraction.positionList = []

# Backtracking model from https://piazza.com/class/ksxdyap437e1yk?cid=4124
def planBacktracking(app, index = 0):
    if isSolution(app):
        return True
    else:
        nextCol = colWithMostEmptyCell(app)
        if nextCol == None:
            return None
        for row in range(8):
            
            if isLegalToPutIn(app,(nextCol,row),app.selectedAttractions_time[index]):
                putAttractionInPlan(app,(nextCol,row),app.selectedAttractions_time[index])
                solution = planBacktracking(app,index+1)
                
                if solution != None:
                    return True
                removeAttractionFromPlan(app, app.selectedAttractions_time[index])
        return None


def generateOriginalPlan(app): 
    generateOriginalListOfAttractions(app)
    app.selectedAttractions_time = sorted(app.selectedAttractions_cost, key=lambda x: x.time, reverse=True)
    result = planBacktracking(app)

    # if the backtracking result is None
    # remove the attraction with the most time consumption and try to make a plan again
    while result == None:
        app.selectedAttractions_time.pop(0)
        result = planBacktracking(app)
    app.selectedAttractions_cost = sorted(app.selectedAttractions_time, key=lambda x: x.cost)

    for attraction in app.selectedAttractions_cost:
        app.totalCost += attraction.cost






###########################
# Plan Mode
###########################

# borrowed from classnotes https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getPlanDimensions(app):
    planRows = 8
    planCols = min(7, app.days)
    cellWidth = 130
    cellHeight = 60
    plan_x0 = 100
    plan_y0 = 130
    plan_x1 = plan_x0 + cellWidth*planCols
    plan_y1 = plan_y0 + cellHeight*planRows
    return (planRows, planCols, cellWidth, cellHeight, plan_x0, plan_y0, plan_x1, plan_y1)
    
def pointInPlan(app, x, y):
    if app.planPage == 0:
        rightLimit = min(app.days,7)
    elif app.planPage > 0:
        rightLimit = min(app.days-app.planPage*7, 7)
    return ((app.plan_x0 <= x <= app.plan_x0 + rightLimit*app.cellWidth) and
            (app.plan_y0 <= y <= app.plan_y1))

def getCell(app, x, y):
    if (not pointInPlan(app, x, y)):
        return (-1, -1)
    row = int((y - app.plan_y0) / app.cellHeight)
    colDrawn = int((x - app.plan_x0) / app.cellWidth)
    col = app.planPage*7 + colDrawn
    return (row, col)

def getCellBounds(app, row, col):
    x0 = app.plan_x0 + col * app.cellWidth
    x1 = app.plan_x0 + (col+1) * app.cellWidth
    y0 = app.plan_y0 + row * app.cellHeight
    y1 = app.plan_y0 + (row+1) * app.cellHeight
    return (x0, y0, x1, y1)

def drawScheduleForm(app,canvas):
    for row in range(app.planRows):
        for col in range(app.planCols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')

def drawTime(app, canvas):
    timeList = ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM']
    x = app.plan_x0 - 10
    for i in range(9):
        y = app.plan_y0 + app.cellHeight*i
        canvas.create_text(x, y, text = timeList[i], anchor=E, font = 'Helvetica 15 bold')

def drawDates(app, canvas):
    y = app.plan_y0 
    if app.planTotalPages == 1:
        for col in range(app.days):
            dateIndex = col
            x = app.plan_x0 + app.cellWidth*col + 0.5*app.cellWidth
            canvas.create_text(x, y, text=app.dates[dateIndex], anchor=S, font = 'Helvetica 15 bold')
    elif app.planTotalPages > 1:
        colNum = min(app.days - app.planPage*7, 7)
        for col in range(colNum):
            x = app.plan_x0 + app.cellWidth*col + 0.5*app.cellWidth
            canvas.create_text(x, y, text=app.dates[app.planPage*7+col], anchor=S, font = 'Helvetica 15 bold')

def drawEventBlocks(app, canvas):
    # eventBlocks on this page should be colLeftLimit <= col < colRightLimit
    colLeftLimit = app.planPage*7
    colRightLimit = colLeftLimit+7
    for attraction in app.selectedAttractions_cost:
        startCol, startRow = attraction.start
        if colLeftLimit <= startCol < colRightLimit:
            x0, y0, a, b = getCellBounds(app,startRow, startCol-colLeftLimit)
            y1 = y0 + min(attraction.time,8) * app.cellHeight
            x1 = x0 + app.cellWidth
            color = 'wheat' if attraction.clickedInPlan == False else 'tan'
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            text = textwrap.fill(attraction.name, width = 20)
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f'{text}', font = 'Helvetica 12')

def getPlanArrowDimentions():
    planLeftArrow_x0 = 30
    planArrow_y0 = 355
    planLeftArrow_x1 = 45
    planArrow_y1 = 385
    planRightArrow_x0 = 1020
    planRightArrow_x1 = 1035
    return (planArrow_y0,planArrow_y1,planLeftArrow_x0,planLeftArrow_x1,planRightArrow_x0,planRightArrow_x1)

def pointInPlanLeftArrow(app, x, y):
    return (app.planLeftArrow_x0 <= x <= app.planLeftArrow_x1) and (app.planArrow_y0 <= y <= app.planArrow_y1)

def pointInPlanRightArrow(app, x, y):
    return (app.planRightArrow_x0 <= x <= app.planRightArrow_x1) and (app.planArrow_y0 <= y <= app.planArrow_y1)

    
def drawPlanArrow(app, canvas):
    # draw plan left arrow
    leftColor = 'black' if app.planPage > 0 else 'lightgrey'
    canvas.create_polygon(app.planLeftArrow_x0,370,app.planLeftArrow_x1,app.planArrow_y0,app.planLeftArrow_x1,app.planArrow_y1, fill = leftColor, outline = None)
    # draw plan right arrow
    rightColor = 'black' if app.planPage < app.planTotalPages-1 else 'lightgrey'
    canvas.create_polygon(app.planRightArrow_x1,370,app.planRightArrow_x0,app.planArrow_y0,app.planRightArrow_x0,app.planArrow_y1, fill = rightColor,outline = None)


def getSideArrowDimentions(app):
    sideArrow_x0 = (app.bar_x0 + app.bar_x1)/2-15    #1240
    sideArrow_x1 = (app.bar_x0 + app.bar_x1)/2    #1255
    sideArrow_x2 = (app.bar_x0 + app.bar_x1)/2+15               #1270
    sideUpArrow_y0 = app.side_y0 + 8               #88
    sideUpArrow_y1 = sideUpArrow_y0 + 15           #103
    sideDownArrow_y0 = app.bar_y1 + 7              #697
    sideDownArrow_y1 = sideDownArrow_y0 + 15
    return (sideArrow_x0,sideArrow_x1,sideArrow_x2,sideUpArrow_y0,sideUpArrow_y1,sideDownArrow_y0,sideDownArrow_y1)

# return (app.planLeftArrow_x0 <= x <= app.planLeftArrow_x1) and (app.planArrow_y0 <= y <= app.planArrow_y1)
def pointInSideUpArrow(app, x, y):
    return app.sideArrow_x0 <= x <= app.sideArrow_x2 and app.sideUpArrow_y0 <= y <= app.sideUpArrow_y1

def pointInSideDownArrow(app, x, y):
    return app.sideArrow_x0 <= x <= app.sideArrow_x2 and app.sideDownArrow_y0 <= y <= app.sideDownArrow_y1

def drawSideArrow(app, canvas):
    if app.sideType == 'Attraction':
        # draw side up arrow
        upColor = 'black' if app.attractionPage > 0 else 'lightgrey'
        canvas.create_polygon(app.sideArrow_x0,app.sideUpArrow_y1,app.sideArrow_x1,app.sideUpArrow_y0,app.sideArrow_x2,app.sideUpArrow_y1, fill = upColor, outline = None)
        # draw side down arrow
        downColor = 'black' if app.attractionPage < app.attractionTotalPages-1 else 'lightgrey'
        canvas.create_polygon(app.sideArrow_x0,app.sideDownArrow_y0,app.sideArrow_x1,app.sideDownArrow_y1,app.sideArrow_x2,app.sideDownArrow_y0, fill = downColor, outline = None)

    if app.sideType == 'Restaurant':
        # draw side up arrow
        upColor = 'black' if app.restaurantPage > 0 else 'lightgrey'
        canvas.create_polygon(app.sideArrow_x0,app.sideUpArrow_y1,app.sideArrow_x1,app.sideUpArrow_y0,app.sideArrow_x2,app.sideUpArrow_y1, fill = upColor, outline = None)
        # draw side down arrow
        downColor = 'black' if app.restaurantPage < app.restaurantTotalPages-1 else 'lightgrey'
        canvas.create_polygon(app.sideArrow_x0,app.sideDownArrow_y0,app.sideArrow_x1,app.sideDownArrow_y1,app.sideArrow_x2,app.sideDownArrow_y0, fill = downColor, outline = None)

    if app.sideType == 'Hotel':
        # draw side up arrow
        upColor = 'black' if app.hotelPage > 0 else 'lightgrey'
        canvas.create_polygon(app.sideArrow_x0,app.sideUpArrow_y1,app.sideArrow_x1,app.sideUpArrow_y0,app.sideArrow_x2,app.sideUpArrow_y1, fill = upColor, outline = None)
        # draw side down arrow
        downColor = 'black' if app.hotelPage < app.hotelTotalPages-1 else 'lightgrey'
        canvas.create_polygon(app.sideArrow_x0,app.sideDownArrow_y0,app.sideArrow_x1,app.sideDownArrow_y1,app.sideArrow_x2,app.sideDownArrow_y0, fill = downColor, outline = None)

def getSideDimensions(app): 
    barRows = 10
    barWidth = 330
    barHeight = 58
    bar_x0 = 1090
    bar_y0 = 110
    bar_x1 = bar_x0 + barWidth
    bar_y1 = bar_y0 + barHeight*barRows

    topBottom_margin = 30
    leftRight_margin = 15
    side_x0 = bar_x0 - leftRight_margin
    side_y0 = bar_y0 - topBottom_margin
    side_x1 = bar_x1 + leftRight_margin
    side_y1 = bar_y1 + topBottom_margin
    return (barRows, barHeight, bar_x0, bar_y0, bar_x1, bar_y1, side_x0, side_y0, side_x1, side_y1)

def getBarBounds(app, row):
    x0 = app.bar_x0
    x1 = app.bar_x1
    y0 = app.bar_y0 + row * app.barHeight
    y1 = app.bar_y0 + (row+1) * app.barHeight
    return (x0, y0, x1, y1)

def pointInBars(app, x, y):
    if app.sideType == 'Attraction':
        if app.attractionPage == 0:
            downLimit = min(len(app.attractions),app.barRows)
        elif app.attractionPage > 0:
            downLimit = min(len(app.attractions)-app.attractionPage*app.barRows, app.barRows)
        return ((app.bar_x0 <= x <= app.bar_x1) and
                (app.bar_y0 <= y <= app.bar_y0+downLimit*app.barHeight))

def getBar(app, x, y):
    if (not pointInBars(app, x, y)):
        return -1
    row = int((y - app.bar_y0) / app.barHeight)
    return row

def drawBars(app, canvas):
    if app.sideType == 'Attraction':
        downLimit = min(len(app.attractions),app.attractionPage*app.barRows+app.barRows)
        for r in range(app.attractionPage*app.barRows, downLimit):
            currAttraction = app.attractions[r]
            if currAttraction.clickedInBar == True:
                barColor = 'tan'
            elif currAttraction.start == (-1,-1):
                barColor = 'wheat'
            elif currAttraction.start != (-1,-1):
                barColor = 'white'
            x0, y0, x1, y1 = getBarBounds(app, r-app.attractionPage*app.barRows)
            canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', fill = barColor)
            info1 = currAttraction.name
            hourText = 'hour' if currAttraction.time == 1 else 'hours'
            info2 = '$' + str(currAttraction.cost) + '   ' + str(currAttraction.time) + ' ' + hourText
            text1 = textwrap.fill(info1, width = 45)
            text2 = textwrap.fill(info2, width = 45)
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f'{text1}', font = 'Helvetica 14 bold')
            canvas.create_text(x1, y1, text = f'{text2}', font = 'Helvetica 11', anchor = SE)

# 'blueviolet' when clicked   'mediumorchid' available in bar or in plan   'thistle' bg   'white' unavailable
    if app.sideType == 'Restaurant':  
        downLimit = min(len(app.restaurants),app.restaurantPage*app.barRows+app.barRows)
        for r in range(app.restaurantPage*app.barRows, downLimit):
            currRestaurant = app.restaurants[r]
            if currRestaurant.clickedInBar == True:
                barColor = 'mediumpurple'
            elif currRestaurant.start == (-1,-1):
                barColor = 'plum'
            elif currRestaurant.start != (-1,-1):
                barColor = 'white'
            x0, y0, x1, y1 = getBarBounds(app, r-app.restaurantPage*app.barRows)
            canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', fill = barColor)
            info1 = currRestaurant.name
            hourText = 'hour' if currRestaurant.time == 1 else 'hours'
            info2 = ('  ').join(currRestaurant.features)
            info3 = currRestaurant.cost
            text1 = textwrap.fill(info1, width = 45)
            text2 = textwrap.fill(info2, width = 50)
            text3 = textwrap.fill(info3, width = 30)
            canvas.create_text((x0+x1)/2, (y0+y1)/2 - (y1-y0)/10, text = f'{text1}', font = 'Helvetica 15 bold')
            canvas.create_text(x0+(x1-x0)/12, y1, text = f'{text2}', font = 'Helvetica 12 italic', anchor = SW)
            canvas.create_text(x1, y1, text = f'{text3}', font = 'Helvetica 13', anchor = SE)
###        

###    if app.sideType == "Hotel":
###

def drawSideBackground(app, canvas):
    x0, y0, x1, y1 = app.side_x0, app.side_y0, app.side_x1, app.side_y1
    if app.sideType == 'Attraction':
        color = app.attractionBgColor
    elif app.sideType == 'Restaurant':
        color = app.restaurantBgColor
    elif app.sideType == 'Hotel':
        color = app.hotelBgColor
    canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', fill = color)

def drawSideBarsBlocks(app, canvas):
    for row in range(app.barRows):
        x0, y0, x1, y1 = getBarBounds(app, row)
        canvas.create_rectangle(x0, y0, x1, y1, outline = 'black')






def pointInFlags(app, x, y):
    return ((app.side_x0 <= x <= app.side_x1) and (app.side_y0-30 <= y <= app.side_y0))

def pointInAttractionFlag(app, x, y):
    return (app.side_x0 <= x <= app.side_x0 + (app.side_x1 - app.side_x0)/3) and (app.side_y0-30 <= y <= app.side_y0)

def pointInRestaurantFlag(app, x, y):
    return (app.side_x0 + (app.side_x1 - app.side_x0)/3) <= x <= (app.side_x0 + (app.side_x1 - app.side_x0)/3*2) and (app.side_y0-30 <= y <= app.side_y0)

def pointInHotelFlag(app, x, y):
    return (app.side_x0 + (app.side_x1 - app.side_x0)/3*2) <= x <= app.side_x1 and (app.side_y0-30 <= y <= app.side_y0)
   

def drawSideFlags(app, canvas):
    y0 = app.side_y0 - 30
    y1 = app.side_y0
    # draw the Attraction flag
    x0 = app.side_x0
    x1 = app.side_x0 + (app.side_x1 - app.side_x0)/3 
    canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', fill = app.attractionBgColor)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'Attraction', fill = 'black', font = 'Helvetica 17 bold')
    # draw the Restaurant flag
    x0 = app.side_x0 + (app.side_x1 - app.side_x0)/3
    x1 = app.side_x0 + (app.side_x1 - app.side_x0)/3*2
    canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', fill = app.restaurantBgColor)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'Restaurant', fill = 'black', font = 'Helvetica 17 bold')
    # draw the Hotel flag
    x0 = app.side_x0 + (app.side_x1 - app.side_x0)/3*2
    x1 = app.side_x1
    canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', fill = app.hotelBgColor)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'Hotel', fill = 'black', font = 'Helvetica 17 bold')



def planMode_mousePressed(app, event):
    print("detect mousePressed")
    # with a chosen event, clicked on somewhere outside the plan, cancel the choice
    if not pointInPlan(app, event.x, event.y) and app.clickedAttractionInPlan != None:
        print('1 if')
        app.clickedAttractionInPlan.clickedInPlan = False
        app.clickedAttractionInPlan = None

    elif not pointInBars(app, event.x, event.y) and not pointInPlan(app, event.x, event.y) and app.clickedAttractionInBar != None:
        print('2 if')
        app.clickedAttractionInBar.clickedInBar = False
        app.clickedAttractionInBar = None

    elif pointInPlan(app, event.x, event.y): 
        print('3 if')
        row, col = getCell(app, event.x, event.y)
        # no chosen event from plan, no chosen event from sidebar, click on an event in plan
        if app.clickedAttractionInPlan == None and app.clickedAttractionInBar == None and app.plan[col][row] != None:
            app.clickedAttractionInPlan = app.plan[col][row]
            app.clickedAttractionInPlan.clickedInPlan = True
        # already chosen an event from plan, click on an empty cell
        elif app.clickedAttractionInPlan != None and app.plan[col][row] == None:
            if isLegalToPutIn(app, (col,row), app.clickedAttractionInPlan):
                removeAttractionFromPlan(app, app.clickedAttractionInPlan)
                putAttractionInPlan(app, (col,row), app.clickedAttractionInPlan)
                app.clickedAttractionInPlan.clickedInPlan = False
                app.clickedAttractionInPlan = None
        # already chosen an event from plan, click on itself again
        elif app.clickedAttractionInPlan != None and app.plan[col][row] != None: 
                if app.plan[col][row] == app.clickedAttractionInPlan:
                    app.clickedAttractionInPlan.clickedInPlan = False
                    app.clickedAttractionInPlan = None
                else:
                    app.clickedAttractionInPlan.clickedInPlan = False
                    app.clickedAttractionInPlan = app.plan[col][row]
                    app.clickedAttractionInPlan.clickedInPlan = True

        # already chosen an event from bar, click on an empty cell in plan
        elif app.clickedAttractionInBar != None and app.plan[col][row] == None:
            if isLegalToPutIn(app, (col,row), app.clickedAttractionInBar):
                print('---------3.4')
                putAttractionInPlan(app, (col,row), app.clickedAttractionInBar)
                app.selectedAttractions_cost.append(app.clickedAttractionInBar)
                app.clickedAttractionInBar.clickedInBar = False
                app.totalCost += app.clickedAttractionInBar.cost
                app.clickedAttractionInBar = None
        

    elif pointInBars(app, event.x, event.y):
        print('4 if')
        row = getBar(app, event.x, event.y)
        # click on a not-in-plan bar
        if app.attractions[app.barRows*app.attractionPage+row].start == (-1,-1):
            # there is no chosen event from bar, click on an event
            if app.clickedAttractionInBar == None:
                print('-------4.1')
                app.clickedAttractionInBar = app.attractions[app.barRows*app.attractionPage+row]
                app.clickedAttractionInBar.clickedInBar = True

            # already chosen event from bar, click on an event
            elif app.clickedAttractionInBar != None:
                # if click on the same event itself, cancel the click
                if app.clickedAttractionInBar == app.attractions[app.barRows*app.attractionPage+row]:
                    print('-------4.2')
                    app.clickedAttractionInBar.clickedInBar = False
                    app.clickedAttractionInBar = None
                else:
                    print('-------4.3')
                    app.clickedAttractionInBar.clickedInBar = False
                    app.clickedAttractionInBar = app.attractions[app.barRows*app.attractionPage+row]
                    app.clickedAttractionInBar.clickedInBar = True
            


    # when nothing from the plan or sidebar is chosen
    elif app.clickedAttractionInBar == None and app.clickedAttractionInPlan == None:
        print('5 if')
        # switch side bar type
        if pointInAttractionFlag(app, event.x, event.y):
            app.sideType = 'Attraction'
        elif pointInRestaurantFlag(app, event.x, event.y):
            app.sideType = 'Restaurant'
        elif pointInHotelFlag(app, event.x, event.y):
            app.sideType = 'Hotel'

        # change plan page    
        if pointInPlanLeftArrow(app, event.x, event.y):
            if app.planPage > 0:
                app.planPage -= 1
            
        if pointInPlanRightArrow(app, event.x, event.y):
            if app.planPage < app.planTotalPages-1:
                app.planPage += 1

        # click on up arrow when showing attraction bars
        if app.sideType == 'Attraction' and pointInSideUpArrow(app, event.x, event.y):
            if app.attractionPage > 0:
                app.attractionPage -= 1
        # click on down arrow when showing attraction bars
        if app.sideType == 'Attraction' and pointInSideDownArrow(app, event.x, event.y):
                if app.attractionPage < app.attractionTotalPages-1:
                    app.attractionPage += 1

        # click on up arrow when showing restaurant bars
        if app.sideType == 'Restaurant'and pointInSideUpArrow(app, event.x, event.y):
            if app.restaurantPage > 0:
                app.restaurantPage -= 1
        # click on down arrow when showing restaurant bars
        if app.sideType == 'Restaurant' and pointInSideDownArrow(app, event.x, event.y):
            if app.restaurantPage < app.restaurantTotalPages-1:
                app.restaurantPage += 1

        # click on up arrow when showing hotel bars
        if app.sideType == 'Hotel'and pointInSideUpArrow(app, event.x, event.y):
            if app.hotelPage > 0:
                app.hotelPage -= 1
        # click on down arrow when showing hotel bars
        if app.sideType == 'Hotel' and pointInSideDownArrow(app, event.x, event.y):
            if app.hotelPage < app.hotelTotalPages-1:
                app.hotelPage += 1


    
                
def planMode_keyPressed(app, event):
    print("detect keyPressed")
    if app.clickedAttractionInPlan != None and event.key == 'Right':
        print('conduct ')
        app.selectedAttractions_cost.remove(app.clickedAttractionInPlan)
        removeAttractionFromPlan(app, app.clickedAttractionInPlan)
        app.clickedAttractionInPlan.clickedInPlan = False
        app.totalCost -= app.clickedAttractionInPlan.cost
        app.clickedAttractionInPlan = None





def planMode_redrawAll(app, canvas):
    drawScheduleForm(app,canvas)
    drawTime(app, canvas)
    drawDates(app, canvas)
    
    drawEventBlocks(app, canvas)
    drawPlanArrow(app, canvas)

    drawSideFlags(app, canvas)

    drawSideBackground(app, canvas)
    drawSideBarsBlocks(app, canvas)
    
    drawBars(app, canvas)
    drawSideArrow(app, canvas)


    # draw city name
    canvas.create_text(70,20, text =f'{app.city}', anchor=NW,fill = 'black', font = 'Helvetica 40 bold')
    # draw cost
    canvas.create_text(800,750, text =f'Cost: {app.totalCost}', anchor=SE,fill = 'black', font = 'Helvetica 20 bold')


#######################
def playBooby():
    width, height = getScreenSize()
    runApp(width=width, height=height)

playBooby()



# GUI = Tk()
# GUI.configure(background="#002E52")
# GUI.title('Templatewriter')
# GUI.geometry("1440x820")
# e = Entry(GUI)
# e.place(x=0, y=780)

# runApp(width=1440, height=770)