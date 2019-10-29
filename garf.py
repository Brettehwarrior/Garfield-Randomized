#imports
import sys
import random
import datetime
import urllib.request
from PIL import Image

#Make a whole bunch of arrays in a dumb way so it has a fixed size
img = [None] * 3
panel = [None] * 3
url = [None] * 3
weekday = [None] * 3
w = [None] * 3
h = [None] * 3

#When is now?
now = datetime.datetime.now()


def generate_comic():
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
                print(str("Error when attempting to load image from url "+url[i])+", trying again")

    #Crop image to single panel each
    for i in range(0, 3):
        w[i], h[i] = img[i].size
        panel[i] = img[i].crop(((w[i]/3)*i, 0, (w[i]/3)*i+(w[i]/3), h[i]))

    #Save images
    #for i in range(0, 3):
        #print(url[i])
        #img[i].save('garf'+str(i)+'.gif')
        #panel[i].save('panel'+str(i)+'.gif')


    #Generate final image
    #https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
    widths, heights = zip(*(i.size for i in panel))
    total_width = sum(widths)
    max_height = max(heights)

    comic = Image.new('RGB', (total_width, max_height), (255,255,255))
    x_off = 0
    for im in panel:
      comic.paste(im, (x_off,0))
      x_off += im.size[0]

    comic.save('comic.jpg')
