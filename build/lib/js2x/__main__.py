#! /usr/bin/env python
# coding: utf-8
# author: boboidream <z644381492@gmail.com>
# version: 0.0.7
# date: 2018-05-14

import os
import platform
import time
import urllib2
from lxml import etree
import html2text
import argparse

class JianShu(object):
    def __init__(self, params):
        self.url = params.get('url')
        self.request_content = None
        self.image_prefix = params.get('image_prefix')
        self.download_path = params.get('download_path') or self.get_download_path()

    def download(self):
        request_content = self.request(self.url)
        article = self.parse(request_content)
        self.download_images(article.get('title'), article.get('date'), article.get('images_array'))
        self.download_post(article.get('title'), article.get('date'), article.get('content'))

    def get_download_path(self):
        os_type = platform.system()
        if os_type == 'Darwin' or os_type == 'Linux':
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        elif os_type == 'Windows':
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        else:
            desktop = os.getcwd()
            print("Unknown system OS. Use command running path as download folder.")
        
        return desktop
    
    def request(self, url, retry_times=4):
        times = 0
        while retry_times > 0:
            times += 1
            print 'request %s, times: %d' % (url, times)
            try:
                req = urllib2.Request(url)
                req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5')
                response = urllib2.urlopen(req)
                self.request_content = response.read().decode('utf-8', 'ignore')
            except Exception, e:
                print e
                retry_times -= 1
            else:
                return self.request_content

    def parse(self, content):
        page = etree.HTML(content)
        article = page.xpath('//div[@class="article"]')
        images_array = [] # store real images'url
        image_prefix = self.image_prefix

        # get Title
        article_title_node = article[0].xpath('//h1')
        article_title = article_title_node[0].text

        # get Date
        article_date_node = article[0].xpath('//span[@class="publish-time"]')
        article_date_str = article_date_node[0].text
        timeArray = time.strptime(article_date_str[0:15], '%Y.%m.%d %H:%M')
        article_date = time.strftime('%Y-%m-%d %H:%M:00', timeArray)

        # deal images
        article_images = article[0].xpath('//div[@class="image-package"]')

        for index, image in enumerate(article_images):
            caption = image.xpath('div[@class="image-caption"]')[0].text
            url = image.xpath('*/*/img/@data-original-src')[0]
            url_suffix = '?imageMogr2/auto-orient/strip%7CimageView2/2/w/700'
            img_name = article_date[0:10] + '-' + str(index) + '.' + url.split('.')[-1]
            image.clear()
            image.text = '![%s](%s)' % (caption, image_prefix + img_name)
            images_array.append({'url': url + url_suffix, 'name': img_name})

        # get Content
        article_content_node = article[0].xpath('//div[@class="show-content"]')
        article_content_str = etree.tostring(article_content_node[0])
        article_content = html2text.html2text(article_content_str)

        return {
            'title': article_title,
            'date': article_date, 
            'content': article_content,
            'images_array': images_array
        }

    def download_post(self, title, date, content):
        post_head = '---\ntitle: %s\ndate: %s\ncategories:\ntags:\n\n---\n' % (title, date)
        post = post_head + content
        post_title = date[0:10] + '-' + title
        post_dir = os.path.join(self.download_path, post_title)

        if not os.path.exists(post_dir):
            os.makedirs(post_dir)
        
        print 'download to "' + post_dir + '" success!'
        with open(os.path.join(post_dir, post_title + '.md'), 'w+') as f:
            f.write(post.encode('utf-8'))
    
    def download_images(self, title, date, images_array):
        post_title = date[0:10] + '-' + title
        images_dir = os.path.join(self.download_path, post_title, 'img')

        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        for image in images_array:
            try:
                img_data = urllib2.urlopen('http:' + image['url']).read()
                img_name = os.path.join(images_dir, image['name'])

                output = open(img_name, 'wb+')
                output.write(img_data)
                output.close()
            except Exception, e:
                print e

# get argument
def command_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.6')    
    parser.add_argument('url', help="url of JianShu Article")
    parser.add_argument('-o', '--output', help="download path. Default: Desktop")
    parser.add_argument('-p', '--prefix', default="./img/", help="set prefix for image")

    return parser.parse_args()

if __name__ == '__main__':
    args = command_parse()
    params = {
        'url': args.url,
        'image_prefix': args.prefix,
        'download_path': args.output
    }

    jianshu = JianShu(params)
    jianshu.download()



