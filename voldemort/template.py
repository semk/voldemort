#! /usr/bin/env python
#
# Jinja2 Template engine
#
# @author: Sreejith K
# Created On 19th Sep 2011


import os
import io
import logging

import markdown
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from jinja2 import nodes
from jinja2.ext import Extension
from yaml import load, Loader

import filters


log = logging.getLogger(__name__)


class MarkdownExtension(Extension):
    """ A Jinja2 extension that allows you to write Markdown code inside
    {% markdown %} {% endmarkdown %} tags.
    """
    tags = set(['markdown'])

    def __init__(self, environment):
        super(MarkdownExtension, self).__init__(environment)
        environment.extend(
                    markdowner=markdown.Markdown(
                                extensions=['codehilite'],
                                #extension_configs={'codehilite': ('force_linenos', False)}
                                )
                    )

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
                                       ['name:endmarkdown'],
                                       drop_needle=True
                                       )
        return nodes.CallBlock(
                               self.call_method('_markdown_support'),
                               [],
                               [],
                               body
                               ).set_lineno(lineno)

    def _markdown_support(self, caller):
        return self.environment.markdowner.convert(caller()).strip()


# template's environment
env = Environment(extensions=[MarkdownExtension])


def get_meta_data(filename):
    """ Get the meta-data from posts.
    """
    log.debug('Parsing meta-data from %s' %filename)
    with io.open(filename, 'rt') as f:
        content = f.readlines()
        content_encoding = f.encoding
    content_without_meta = content[:]
    if content[0].startswith('---'):
        yaml_lines = []
        for lineno, line in enumerate(content[1:]):
            if line.startswith('---'):
                break
            yaml_lines.append(line)
        content_without_meta = content_without_meta[lineno+2:]
        yaml_string = ''.join(yaml_lines)
        meta = load(yaml_string, Loader=Loader)
    else:
        meta = {}

    meta['filename'] = filename
    raw = ''.join(content_without_meta)

    # convert to unicode
    if not isinstance(raw, unicode):
        raw = unicode(raw, content_encoding)

    meta['raw'] = raw

    if meta['raw']:
        # exclude the jinja syntax
        raw = [line for line in content_without_meta if not line.startswith('{%')]
        raw = ''.join(raw)
        # convert to unicode
        if not isinstance(raw, unicode):
            raw = unicode(raw, content_encoding)
        meta['content'] = markdown.markdown(raw, ['codehilite'])
    else:
        meta['content'] = ''
    return meta


def render(content, values={}):
    """ Render Jinja2 templates.
    """
    tmpl = env.from_string(content)
    return tmpl.render(values)


def get_rendered_page(filename, values={}):
    """ Obtain the rendered template including the exported 
    macros and variables .
    """
    log.debug('Rendering file: %s' %filename)
    with open(filename, 'r') as f:
        content = f.read()
    return render(content, values)


def setup_filters():
    """Registers the voldemort filters
    """
    log.info('Initializing voldemort filters')
    for filter_method in filters.__all__:
        env.filters[filter_method] = getattr(filters, filter_method)


def setup_template_dirs(root_dir):
    """ Add search paths to template environment.
    """
    log.info('Adding template directories to environment')
    template_dirs = [root_dir]
    for dir in os.listdir(root_dir):
        if dir.startswith('_') or dir.endswith('~'):
            continue
        dir = os.path.join(root_dir, dir)
        if os.path.isdir(dir):
            template_dirs.append(dir)
    env.loader = FileSystemLoader(template_dirs)