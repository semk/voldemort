#! /usr/bin/env python
#
# Voldemort: A static site generator using Jinja2 and Markdown templates
#
# @author: Sreejith K
# Created On 19th Sep 2011


import os
import sys

from template import *


class Voldemort(object):
    """ Provides all the functionalities like meta-data parsing and site generation.
    """
    _layout_dir = 'layout'
    _include_dir = 'include'
    _posts_dir = 'posts'

    def __init__(self):
        setup_template_dirs([self._include_dir, 
                             self._layout_dir, 
                             self._posts_dir])

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
        pass
    
    def render_templates(self):
        """ Generate HTML from all the markups.
        """
        pass

    def run(self):
        kwargs = self.parse_meta_data()


def main():
    app = Voldemort()
    app.run()


if __name__ == '__main__':
    main()