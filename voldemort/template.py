#! /usr/bin/env python
#
# Jinja2 Template engine
#
# @author: Sreejith K
# Created On 19th Sep 2011


from jinja2 import FileSystemLoader
from jinja2.environment import Environment


# template's environment
env = Environment()


def setup_template_dirs(dirs):
    """ Add search paths to template environment.
    """
    env.loader = FileSystemLoader(dirs)


def render_template(template, values):
    """ Render Jinja2 templates.
    """
    tmpl = env.get_template(template)
    return tmpl.render(values)