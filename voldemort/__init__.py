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
import shutil

import template
import config
import util


log = logging.getLogger('voldemort')


class Voldemort(object):
    """ Provides all the functionalities like meta-data parsing 
    and site generation.
    """
    template_extensions = ['.htm', '.html', '.md', '.markdown', '.jinja', '.txt']
    date_format = '%d-%m-%Y'

    def __init__(self, work_dir):
        self.work_dir = work_dir
        util.setup_logging(os.path.join(self.work_dir, 'voldemort.log'), logging.DEBUG)
        self.config = config.load_config(self.work_dir)
        template.setup_template_dirs(self.work_dir)
        # ignore the following directories
        self.ignored_directories = [self.config.layout_dir,
                                    self.config.include_dir,
                                    self.config.posts_dir,
                                    self.config.site_dir]

    def init(self):
        """ (Re)create the site directory.
        """
        if os.path.exists(self.config.site_dir):
            shutil.rmtree(self.config.site_dir)
            os.mkdir(self.config.site_dir)
        else:
            os.mkdir(self.config.site_dir)

    def serve(self, directory, port):
        """ Run an HTTPServer on the given port under this directory.
        """
        pass

    def generate(self):
        """ Generate the site.
        """
        self.generate_posts()
        self.generate_pages()

    def write_html(self, file, data):
        """ Write the html data to file.
        """
        with open(file, 'w') as f:
            f.write(data)

    def generate_posts(self):
        """ Generate the posts from the posts directory. Update globals
        """
        self.posts = []
        for post in os.listdir(self.config.posts_dir):
            post = os.path.join(self.config.posts_dir, post)
            post_info = template.get_rendered_page(post)
            self.posts.append(post_info)
            # read the date from the post
            post_date = datetime.datetime.strptime(post_info['date'], 
                                                   self.date_format)
            # construct the url to the post
            post_url = os.path.join(self.config.site_dir,
                                    post_date.strftime(self.config.post_url),
                                    os.path.splitext(post_info['filename'])[0])
            # create directories if necessary
            os.makedirs(post_url)
            post_file = os.path.join(post_url, 'index.html')
            logging.debug('generating post: %s' %post_file)
            # write the html
            self.write_html(post_file, post_info['content'])

        # update the template global with posts info
        template.env.globals.update({'posts': self.posts})

    def generate_pages(self):
        """ Generate HTML from all the other pages.
        """
        for root, dirs, files in os.walk(self.work_dir):
            # checks whether the directory is as subdirectory of root
            def is_a_subdirectory(sub):
                return sub in root
            # ignore all the subdirectories
            if any(map(is_a_subdirectory, self.ignored_directories)):
                continue

            for file in files:
                file = os.path.join(root, file)
                _, extn = os.path.splitext(file)
                if extn and extn not in self.template_extensions:
                    continue

                page_info = template.get_rendered_page(file)
                page_path = os.path.join(self.config.site_dir,
                                         file.split(self.work_dir)[1][1:])
                logging.debug('generating page %s' %page_path)
                # write the rendered page
                self.write_html(page_path, page_info['content'])

    def run(self):
        """ Generate the site.
        """
        self.init()
        self.generate()


def main():
    app = Voldemort(os.path.abspath(os.getcwd()))
    app.run()


if __name__ == '__main__':
    main()