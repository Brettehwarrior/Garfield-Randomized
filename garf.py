import sys
import random
import datetime
import urllib.request
import string
import spreadsheet
import drive_image
from PIL import Image
from enum import Enum
from statistics import median

PANEL_SCALE = 4
PANEL_AMOUNT = 3
PANEL_PADDING_X = 5 * PANEL_SCALE
PANEL_PADDING_Y = 5 * PANEL_SCALE

source_urls = []
template_text = ['ERR', 'ERR']
now = datetime.datetime.now()


def get_random_comic() -> Image:
    """Returns a non-sunday comic retrieved from http://picayune.uclick.com/"""

    now = datetime.datetime.now()

    max_failed_attempts = 100
    failed_attempts = 0

    while failed_attempts < max_failed_attempts:
        url = '(NO URL)'
        try:
            # Establish target date
            year = random.randint(1978, now.year)
            month = random.randint(1, now.month)
            day = random.randint(1, now.day)

            #  Comic date
            target_date = datetime.datetime(year, month, day)

            # If target date is sunday, skip to next loop
            # This is done because sunday comics are in inconsistent formatting
            if target_date.weekday() == 6:
                continue

            #  Create URL, attempt to load image, save URL, and return image
            url = f'http://picayune.uclick.com/comics/ga/{year}/ga{year%100:02d}{month:02d}{day:02d}.gif'
            retrieved_image = urllib.request.urlopen(url)
            comic_image = Image.open(retrieved_image)
            source_urls.append(url)
            # print('Got a comic: '+url)
            return comic_image

        except:
            # Encountered error when attempting to get image from URL
            print(f'Error when attempting to load image from {url}')

            failed_attempts += 1

    # Returns error image when too many failed attempts occur
    print(f'Failed retrieving image {max_failed_attempts} times! Returning error comic')
    return Image.open('images/error/retrieval_error.png')


def crop_to_panel(comic, panel_amount: int, panel_index: int) -> Image:
    """Returns comic cropped to specified panel

    Args:
        comic: Image of comic to crop
        panel_amount: Number of horizontal panels in comic
        panel_index: Integer (0-2) specifying which panel to return

    """
    # Ensure panel_index doesn't exeed possible values
    panel_index = abs(panel_index) % panel_amount

    # Crop comic and return
    w, h = comic.size
    panel_width = (w / panel_amount)
    panel_start_x = panel_width*panel_index
    panel_end_x = panel_start_x + panel_width
    return comic.crop((panel_start_x, 0, panel_end_x, h))


def construct_comic(panels: list) -> Image:
    """Returns a comic image constructed from an array of images, from left to right

    Args:
        panels: Array of images to paste on final comic
    """
    
    # Scale panels to consistent height
    median_height = max([i.size[1] for i in panels])
    
    for i, im in enumerate(panels):
        w, h = im.size
        ar = w / h
        
        panels[i] = im.resize((int(median_height*ar*PANEL_SCALE), int(median_height*PANEL_SCALE)), Image.LANCZOS)
        
    # https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
    widths, heights = zip(*(i.size for i in panels))
    total_width = sum(widths)
    max_height = max(heights)

    comic = Image.new('RGB', (total_width+(PANEL_PADDING_X*(len(panels)+1)), max_height+(PANEL_PADDING_Y*2)), (255, 255, 255))
    x_off = PANEL_PADDING_X
    for im in panels:
        comic.paste(im, (x_off, PANEL_PADDING_Y))
        x_off += im.size[0] + PANEL_PADDING_X

    return comic


def generate_comic(template: dict) -> Image:
    source_urls.clear()
    sources = []
    source_panel_amount = []
    panels = []
    
    template_text.clear()
    credit = template.get('Credit')
    template_text.append(template.get('Name'))
    template_text.append(credit if credit else None)
    
    # Get sources
    random_sources_amount = template.get('Random Sources')
    
    for x in range(0, random_sources_amount):
        sources.append(get_random_comic())
        source_panel_amount.append(3)
    
    drive_source_id = template.get('Drive Source ID')
    if drive_source_id:
        destination = 'images/drive/cameo.png'
        drive_image.download_file_from_google_drive(drive_source_id, destination)
        sources.append(Image.open(destination))
        source_panel_amount.append(1)
        source_urls.append(template.get('Drive Source URL'))
    
    # Generate panels
    panel_layout = template.get('Panel Layout').split()
    
    for i, panel_str in enumerate(panel_layout):
        if panel_str[0] == 'S':
            panel_index = 0
            source_index = len(sources) - 1
        else:
            panel_index = (random.randint(0, 2)) if (panel_str[1]=='R') else (int(panel_str[1])-1)
            source_index = string.ascii_lowercase.index(panel_str[0].lower())

        panels.append(crop_to_panel(sources[source_index], source_panel_amount[source_index], panel_index))


    # print(f'Source array: {source_urls}')
    return construct_comic(panels)


if __name__ == '__main__':
    c = generate_comic({
        'Random Sources': 6,
        'Drive Source ID': '1MMR99gM5xqcnhED-WjX3PXubjzlgcf0X',
        'Drive Source URL': 'hi',
        'Panel Layout': 'AR BR CR DR ER FR'
    })
    c.show()
