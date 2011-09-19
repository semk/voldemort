#! /usr/bin/env python
#
# Voldemort: A static site generator using Jinja2 and Markdown templates
#
# @author: Sreejith K
# Created On 19th Sep 2011


import os
import sys

import template
import post


class Voldemort(object):
    """ Provides all the functionalities like meta-data parsing 
    and site generation.
    """

    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.layout_dir = os.path.join(self.work_dir, 'layout')
        self.include_dir = os.path.join(self.work_dir, 'include')
        self.posts_dir = os.path.join(self.work_dir, 'posts')
        template.setup_template_dirs([self.include_dir, 
                                      self.layout_dir, 
                                      self.posts_dir])

    def serve(self, directory, port):
        """ Run an HTTPServer on the given port under this directory.
        """
        pass

    def generate(self, origin, dest):
        """ Generate the site.
        """
        pass

    def parse_meta_data(self):
        """ Parse the metadata from posts. Return them as kwargs for templates.
        """
        posts_iterator = post.PostsIterator()
        for post in os.listdir(self.posts_dir):
            meta = template.get_exports(post)
            posts_iterator.add(meta)

    def set_globals(self):
        """ Set global variables for the environment.
        """
        pass
    
    def render_templates(self):
        """ Generate HTML from all the markups.
        """
        pass

    def run(self):
        kwargs = self.parse_meta_data()


def main():
    app = Voldemort()
    app.run(os.getcwd())


if __name__ == '__main__':
    main()