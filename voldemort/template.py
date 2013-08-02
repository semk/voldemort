# -*- coding: utf-8 -*-
#
# Jinja2 Template engine
#
# @author: Sreejith K
# Created On 19th Sep 2011


import os
import io
import re
import logging

import markdown
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from jinja2 import nodes
from jinja2.ext import Extension
from yaml import load, Loader

import filters


log = logging.getLogger(__name__)


POST_RE = re.compile(u'---(?P<meta>.*)---(?P<body>.*)', re.DOTALL)


class MarkdownExtension(Extension):

    """A Jinja2 extension that allows you to write Markdown code inside
    {% markdown %} {% endmarkdown %} tags.
    """
    tags = set(['markdown'])

    def __init__(self, environment):
        super(MarkdownExtension, self).__init__(environment)
        environment.extend(
            markdowner=markdown.Markdown(extensions=['codehilite']))

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endmarkdown'],
            drop_needle=True)
        return nodes.CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body).set_lineno(lineno)

    def _markdown_support(self, caller):
        return self.environment.markdowner.convert(caller()).strip()


# template's environment
env = Environment(extensions=[MarkdownExtension])


def wrap_jinja2(content, layout):
    """Wrap the markdown text with Jinja2 headers.
    """
    return '{% extends "' + layout + '" %}\n' +\
           '{% block postcontent %}\n' +\
           '{% markdown %}\n' +\
           content + '\n' +\
           '{% endmarkdown %}\n' +\
           '{% endblock %}'


def strip_jinja2(body):
    """Strip jinja2 strings from the document.
    """
    body_without_jinja = []
    for line in body.split('\n'):
        if line.strip().startswith('{%'):
            continue
        else:
            body_without_jinja.append(line)

    return '\n'.join(body_without_jinja)


def get_meta_data(filename):
    """Get the meta-data from posts.
    """
    log.debug('Parsing meta-data from %s' % filename)
    with io.open(filename, 'rt', encoding='utf-8') as f:
        content = f.read()

    meta = {}
    post_match = POST_RE.match(content)

    if post_match:
        meta = load(post_match.group('meta'), Loader=Loader)
        body = post_match.group('body').strip()
        if 'layout' in meta:
            # The body is pure Markdown without any Jinja syntax
            meta['content'] = markdown.markdown(body, ['codehilite'])
            meta['raw'] = wrap_jinja2(body, layout=meta['layout'])
        else:
            # The body contains Jinja syntax
            body_without_jinja = strip_jinja2(body)
            meta['content'] = markdown.markdown(
                body_without_jinja, ['codehilite'])
            meta['raw'] = body
    else:
        meta['raw'] = content.strip()

    meta['filename'] = filename
    return meta


def render(content, values={}):
    """Render Jinja2 templates.
    """
    tmpl = env.from_string(content)
    return tmpl.render(values)


def get_rendered_page(filename, values={}):
    """Obtain the rendered template including the exported
    macros and variables .
    """
    log.debug('Rendering file: %s' % filename)
    with open(filename, 'r') as f:
        content = f.read()
    return render(content, values)


def setup_filters():
    """Registers the voldemort filters
    """
    log.info('Initializing voldemort filters')
    for filter_method in filters.__all__:
        env.filters[filter_method] = getattr(filters, filter_method)


def setup_template_dirs(layout_dirs):
    """Add search paths to template environment.
    """
    log.info('Adding template directories to environment')
    env.loader = FileSystemLoader(layout_dirs)
