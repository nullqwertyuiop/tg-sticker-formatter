import subprocess
from PIL import Image
from loguru import logger
import os
from os import listdir
from os.path import isfile, join

try:
 os.mkdir('Output')
except Exception as e:
    logger.error(e)
onlyfiles = [f for f in listdir("Input") if isfile(join("Input", f))]
def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize(
        (resize_width, resize_height), Image.Resampling.LANCZOS)
    # or (255, 255, 255, 255)
    background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    offset = (round((width - resize_width) / 2),
              round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background
def makeWebmicon(f: str):
        b1 = os.getcwd()+'/'+f[:f.find('.')]
        b2 = os.getcwd()+'/'+f
        subprocess.call(f'ffmpeg -i {b2} -fs 32KB -c:v libvpx-vp9 -loglevel quiet -vf scale=100:100 {b1}.webm')
for file in onlyfiles:
    if file[file.find('.'):].lower() in ['.webp', '.png', '.jpg']:
        image = Image.open(os.getcwd()+'/Input/'+file, 'r')
        resize(image, 512, 512).save(os.getcwd()+'/Output/' +
                                    file[:file.find('.')]+'.png', quality=100)
        logger.info(file)
    elif file[file.find('.'):].lower() == '.gif':
        image = Image.open(os.getcwd()+'/Input/'+file, 'r')
        b1 = os.getcwd()+'/Output/'+file[:file.find('.')]
        b2 = os.getcwd()+'/Input/'+file
        logger.info(file)
        if image.height > image.width:
            subprocess.check_output(f'ffmpeg -i {b2} -c:v libvpx-vp9 -r 30 -loglevel quiet -vf scale=-1:512 {b1}.webm')
        elif image.width > image.height:
            subprocess.check_output(f'ffmpeg -i {b2} -c:v libvpx-vp9 -r 30 -loglevel quiet -vf scale=512:-1 {b1}.webm')
        else:
            subprocess.check_output(f'ffmpeg -i {b2} -c:v libvpx-vp9 -r 30 -loglevel quiet -vf scale=512:512 {b1}.webm')
    else:
        logger.warning(f'ignore: {file}')

