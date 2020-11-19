import garf
import bot
import schedule
import spreadsheet
from time import sleep
from datetime import datetime

def generate_and_tweet():
    now = datetime.now()
    category = spreadsheet.schedule_list[now.weekday()].get(f'{now.hour}:00') # String with template category on Schedule spreadsheet at current time
    
    templates = spreadsheet.get_templates_with_category(category) # Retreive possible templates of scheduled category
    template = spreadsheet.choose_template(templates) # Select random template by weight
    comic_to_tweet = garf.generate_comic(template) # Generate comic
    comic_to_tweet.save('images/tweet.png')
    
    
    template_text = f'using {garf.template_text[0]} template'
    if garf.template_text[1]: # Append credit tag
        template_text +=  f', inspired by @{garf.template_text[1]}'
    
    sources_text = 'Sources:'
    for s in garf.source_urls:
        sources_text += '\n' + s
    
    print(bot.send_tweet(template_text, sources_text))

def reset_schedule():
    """Clears schedule, reloads spreadsheet, and schedules next reset"""
    schedule.clear()
    spreadsheet.init()
    # Schedule tweets
    schedule.every().hour.at(':00').do(generate_and_tweet)
    # Schedule next reset
    schedule.every().sunday.at('23:30').do(reset_schedule)
    print('Reset successful')

if __name__ == '__main__':
    # Schedule tweets
    schedule.every().hour.at(':00').do(generate_and_tweet)
    reset_schedule()
    
    # generate_and_tweet()
    
    while True:
        schedule.run_pending()
        sleep(30)
        