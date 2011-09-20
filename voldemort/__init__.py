#! /usr/bin/env python
#
# Voldemort: A static site generator using Jinja2 and Markdown templates
#
# @author: Sreejith K
# Created On 19th Sep 2011


import os
import sys
import logging
import datetime

import template
import config
import util


log = logging.getLogger('voldemort')


class Voldemort(object):
    """ Provides all the functionalities like meta-data parsing 
    and site generation.
    """
    template_extensions = ['htm', 'html', 'md', 'markdown', 'jinja']
    date_format = '%d-%m-%Y'

    def __init__(self, work_dir):
        self.work_dir = work_dir
        util.setup_logging(os.path.join(self.work_dir, 'voldemort.log'), logging.DEBUG)
        self.config = config.load_config(self.work_dir)
        template.setup_template_dirs(self.work_dir)

    def init(self):
        """ (Re)create the site directory.
        """
        site_dir = os.path.join(self.work_dir, self.config.site_dir)
        if os.path.exists(site_dir):
            os.system('rm -rf %s' %site_dir)
            os.mkdir(site_dir)
        else:
            os.mkdir(site_dir)

    def serve(self, directory, port):
        """ Run an HTTPServer on the given port under this directory.
        """
        pass

    def generate(self):
        """ Generate the site.
        """
        self.init()
        self.render_posts()
        self.render_pages()

    def write_html(self, file, data):
        """ Write the html data to file.
        """
        with open(file, 'w') as f:
            f.write(data)

    def render_posts(self):
        """ Render the posts from the posts directory
        """
        self.posts = []
        posts_dir = os.path.join(self.work_dir, self.config.posts_dir)
        for post in os.listdir(posts_dir):
            post = os.path.join(posts_dir, post)
            log.debug('writing post: %s ' %post)
            post_info = template.get_rendered_page(post)
            self.posts.append(post_info)
            # read the date from the post
            post_date = datetime.datetime.strptime(post_info['date'], 
                                                   self.date_format)
            # construct the url to the post
            post_url = os.path.join(self.work_dir,
                                    self.config.site_dir,
                                    post_date.strftime(self.config.post_url),
                                    post_info['filename'])
            # create directories if necessary
            os.makedirs(post_url)
            post_file = os.path.join(post_url, 'index.html')
            # write the html
            self.write_html(post_file, post_info['content'])
        # update the template global with posts info
        template.env.globals.update({'posts': self.posts})

    def render_pages(self):
        """ Generate HTML from all the markups.
        """
        for page in os.listdir(self.work_dir):
            page = os.path.join(self.work_dir, page)
            try:
                extn = page.rsplit('.', 1)[1]
            except IndexError:
                continue
            if (os.path.isdir(page)) or (not extn in self.template_extensions):
                continue
            log.debug('writing page: %s' %page)
            page_info = template.get_rendered_page(page)
            # write the rendered page
            page_file = os.path.join(self.work_dir, 
                                     self.config.site_dir, 
                                     page_info['filename'])
            self.write_html(page_file, page_info['content'])

    def run(self):
        self.generate()


def main():
    app = Voldemort(os.path.abspath(os.getcwd()))
    app.run()


if __name__ == '__main__':
    main()