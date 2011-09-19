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

def get_exports(template):
    """ Obtain the exported macros and variables.
    """
    meta = []
    with open(template, 'r') as f:
        content = f.read()
        template = env.from_string(content)
        for attr in dir(template.module):
            if not attr.startswith('_'):
                meta[attr] = getattr(template.module, attr)
    return meta

def setup_template_dirs(dirs):
    """ Add search paths to template environment.
    """
    env.loader = FileSystemLoader(dirs)


def render(template, values):
    """ Render Jinja2 templates.
    """
    tmpl = env.get_template(template)
    return tmpl.render(values)