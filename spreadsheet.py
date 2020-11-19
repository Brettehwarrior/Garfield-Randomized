import gspread
from oauth2client.service_account import ServiceAccountCredentials
from numpy.random import choice
import garf
import bot
import schedule
from time import sleep

SPREADSHEET_NAME = 'RandomizedGarf'

# Google spreadsheet interaction beautifully explained in this tutorial:
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# One issue solved with this:
# https://stackoverflow.com/questions/49258566/gspread-authentication-throwing-insufficient-permission

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


schedule_list = []
template_list = []

categories = set({})

def init():
    # Find a workbook by name and open the first sheet
    schedule_sheet = client.open(SPREADSHEET_NAME).get_worksheet(0)
    template_sheet = client.open(SPREADSHEET_NAME).get_worksheet(1)

    # Extract and save values
    schedule_list.clear()
    schedule_list.extend(schedule_sheet.get_all_records())
    
    template_list.clear()
    template_list.extend(template_sheet.get_all_records())
    
    # Reload template set
    categories.clear()
    for d in schedule_list:
        for value in range(1, len(d)):
            categories.add(tuple(d.values())[value]) # Potentially the most evil bit of python I have ever typed

def get_templates_with_category(category: str) -> list:
    """Returns a list of template dictionaries with matching category"""
    return [template for template in template_list if template['Category'] == category]

def choose_template(templates: list) -> dict:
    """Returns a template dictionary of passed templates list based on the weights of each template"""
    # Get weights
    weights = []
    for template in templates:
        weights.append(template.get('Weight'))
    
    # Normalize weights
    weights_sum = sum(weights)
    weights = [x / weights_sum for x in weights]
    
    draw = choice(templates, None, True, weights)
    return draw


def reset_schedule():
    """Clears schedule, loads schedule from spreadsheet, and schedules next reset"""
    schedule.clear()
    # Schedule reset
    init()
    print(schedule_list)
    
    schedule.every().sunday.at('23:30').do(reset_schedule)

        
if __name__ == '__main__':
    init()
    template = choose_template(get_templates_with_category('Cameo'))
    comic = garf.generate_comic(template)
    comic.show()