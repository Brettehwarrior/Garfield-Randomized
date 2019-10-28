#imports
import sys
import random
import datetime
import urllib.request
from PIL import Image

#When is now?
now = datetime.datetime.now()

img = [None] * 3
url = [None] * 3
weekday = [None] * 3
w = [None] * 3
h = [None] * 3

#Image loading validation loop
for i in range(0, 3):
    error = True
    while error:
        try:
            #Define current year
            year = random.randint(1978, now.year)
            month = random.randint(1, now.month)
            day = random.randint(1, now.day)

            #Format month
            if month < 10:
                month_string = "0" + str(month)
            else:
                month_string = str(month)

            #Format day
            if day < 10:
                day_string = "0" + str(day)
            else:
                day_string = str(day)

            #Create URL
            url[i] = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/"+str(year)+"/"+str(year)+"-"+month_string+"-"+day_string+".gif"

            #Load image from URL
            img[i] = Image.open(urllib.request.urlopen(url[i]))
            #Comic date
            weekday[i] = datetime.datetime(year, month, day).weekday()
            #Exit loop if not sunday
            if (weekday[i] != 6):
                error = False
        except:
            print("Error when attempting to load image from url "+url)

#Determine size of image
for i in range(0, 3):
    w[i], h[i] = img[i].size


#Save images
for i in range(0, 3):
    print(url[i])
    print(weekday[i])
    img[i].save('garf'+str(i)+'.gif')