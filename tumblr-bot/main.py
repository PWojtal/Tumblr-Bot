import wget
import logging
from tumblr-bot.support_classes import DownloadDir
from tumblr-bot.googlevision import GoogleVisionLabels
from tumblr-bot.tumblrapi import GetTumblrImagesURLs
from tqdm import tqdm
import os.path
from urllib.parse import urlparse

logging.basicConfig(filename='../AIMblr.log', level=logging.DEBUG)

# classes = []

# classify = GoogleVisionLabels()

tumblr = GetTumblrImagesURLs('kinsideofthemoon.tumblr.com', limit=10)

for blog in tumblr.getfollowedblogs(limit=2):

    blog = blog.replace('http://', '')
    blog = blog.replace('https://', '')
    blog = blog.replace('com/', 'com')

    downloadDir = DownloadDir(flushOnInit=False, directory="./Download/" + blog)

    for image_url in tqdm(
                    GetTumblrImagesURLs(blog, limit=0, skip_downloaded_images=True),
                    desc='Download images form ' + blog,
                    dynamic_ncols=True,
                 ):

        if not os.path.exists(downloadDir.get() + "/" + os.path.basename(image_url)):
            filename = wget.download(image_url, downloadDir.get())

        # classes.append(classify.get_labels_for_image_incl_wieghts(filename, ['bondage', 'fetish model', 'tied', 'gloves']))