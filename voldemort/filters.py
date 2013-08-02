# -*- coding: utf-8 -*-
#
# Filters for Jinja2 templates
#
# @author: Sreejith K
# Created On 19th Sep 2011


import urllib
import cgi

try:
    from django.utils.text import truncate_html_words
except ImportError:
    truncate_html_words = None


def date(date, format):
    """Format datetime
    """
    return date.strftime(format)


def date_to_string(date):
    """Format a date in short format e.g. "27 Jan 2011".

    date - the Time to format.

    Returns the formatting String.
    """
    return date.strftime('%d %b %Y')


def date_to_long_string(date):
    """Format a date in long format e.g. "27 January 2011".

    date - The Time to format.

    Returns the formatted String.
    """
    return date.strftime('%d %B %Y')


def date_to_xmlschema(date):
    """Format a date for use in XML.

    date - The Time to format.

    Examples

        date_to_xmlschema(datetime.datetime.now())
        => "2011-04-24T20:34:46+05:30"

    Returns the formatted String.
    """
    return date.strftime('%Y-%m-%dT00:00:00+5:30')


def xml_escape(input):
    """Replace special characters "&", "<" and ">" to
    HTML-safe sequences.
    """
    return cgi.escape(input)


def cgi_escape(input):
    """CGI escape a string for use in a URL. Replaces any special
    characters with appropriate %XX replacements.
    """
    return cgi.escape(input, quote=True)


def uri_escape(input):
    """Escape special characters in url.
    """
    return urllib.quote(input)


def number_of_words(input):
    """Return number of words in a string.
    """
    return len(input.split())


def excerpt(html, num, end_text='...'):
    """Return excerpt of html data.
    """
    if truncate_html_words:
        excerpt = truncate_html_words(html, num, end_text)
    else:
        excerpt = html
    return excerpt


__all__ = [
    'date',
    'date_to_string',
    'date_to_long_string',
    'date_to_xmlschema',
    'xml_escape',
    'cgi_escape',
    'uri_escape',
    'number_of_words',
    'excerpt']
