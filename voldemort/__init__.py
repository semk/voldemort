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
    template_extensions = ['.htm', '.html', '.md', '.markdown',
                            '.jinja', '.jinja2', '.txt', '.xml']
    preserved_extensions = ['.txt', '.xml']
    date_format = '%d-%m-%Y'

    def __init__(self, work_dir, foreground=True):
        self.work_dir = work_dir
        self.logfile = os.path.join(self.work_dir, 'voldemort.log')
        if foreground:
            logging.basicConfig(level=logging.DEBUG)
        else:
            util.setup_logging(self.logfile, logging.DEBUG)
        self.config = config.load_config(self.work_dir)
        template.setup_template_dirs(self.work_dir)
        # ignore the following directories
        self.ignored_items = [ self.config.layout_dir,
                               self.config.include_dir,
                               self.config.posts_dir,
                               self.config.site_dir,
                               self.logfile,
                               os.path.join(self.work_dir, '.git'),
                               os.path.join(self.work_dir, '.DS_Store') ]

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
        self.parse_meta_data()
        self.generate_posts()
        self.generate_pages()

    def write_html(self, file, data):
        """ Write the html data to file.
        """
        try:
            os.makedirs(os.path.dirname(file))
        except OSError:
            pass
        with open(file, 'w') as f:
            f.write(data.encode('utf-8'))

    def move_to_site(self, source, dest):
        """ Move the file to the site.
        """
        try:
            os.makedirs(os.path.dirname(dest))
        except OSError:
            pass
        shutil.copyfile(source, dest)

    def change_extension(self, filename, extn='.html'):
        """ Changes the file extension to html if needed.
        """
        directory, base = os.path.split(filename)
        name, ext = os.path.splitext(base)
        if ext not in self.template_extensions \
                or ext in self.preserved_extensions:
            return filename
        name = name + extn
        return os.path.join(directory, name)

    def parse_meta_data(self):
        """ Parses the meta data from posts
        """
        self.posts = []
        for post in os.listdir(self.config.posts_dir):
            post = os.path.join(self.config.posts_dir, post)
            post_meta = template.get_meta_data(post)
            post_meta['date'] = datetime.datetime.strptime(post_meta['date'], 
                                                           self.date_format)
            post_url = os.path.join('/',
                                    post_meta['date'].strftime(self.config.post_url),
                                    post_meta['filename'].split(self.config.posts_dir)[1][1:])
            post_meta['url'] = post_url
            self.posts.append(post_meta)

        def compare_date(x, y):
            return x['date'] > y['date']
        # sort posts based on date.
        self.posts = sorted(self.posts, cmp=compare_date)
        
        # include next and previous urls for posts.
        for post_num, post in enumerate(self.posts):
            next = post_num + 1
            previous = post_num - 1
            if post_num < len(self.posts) - 1: 
                post['next'] = self.posts[next]
            else:
                post['next'] = None
            if post_num != 0:
                post['previous'] = self.posts[previous]
            else:
                post['previous'] = None
        
        # update the template global with posts info
        template.env.globals.update({'posts': self.posts})

    def generate_posts(self):
        """ Generate the posts from the posts directory. Update globals
        """
        for post in self.posts:
            html = template.render(post['content'], 
                                   {'post': post, 'page': post} )
            # construct the url to the post
            post_url = os.path.join(self.config.site_dir,
                                    post['url'][1:])
            # create directories if necessary
            os.makedirs(post_url)
            post_file = os.path.join(post_url, 'index.html')
            log.debug('Generating post: %s' %post_file)
            # write the html
            self.write_html(post_file, html)

    def generate_pages(self):
        """ Generate HTML from all the other pages.
        """
        for root, dirs, files in os.walk(self.work_dir):
            # checks whether the directory is as subdirectory of root
            def is_a_subdirectory(sub):
                return sub in root
            # ignore all the subdirectories
            if any(map(is_a_subdirectory, self.ignored_items)):
                continue

            for file in files:
                file = os.path.join(root, file)
                _, extn = os.path.splitext(file)
                if extn not in self.template_extensions:
                    dest = os.path.join(self.config.site_dir,
                                        file.split(self.work_dir)[1][1:])
                    self.move_to_site(file, dest)
                    continue

                page_meta = template.get_meta_data(file)
                html = template.get_rendered_page(file, {'page': page_meta})
                page_path = os.path.join(self.config.site_dir,
                                         file.split(self.work_dir)[1][1:])
                page_path = self.change_extension(page_path)
                log.debug('Generating page %s' %page_path)
                # write the rendered page
                self.write_html(page_path, html)

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