#! /usr/bin/env python
#
# Filters for Jinja2 templates
#
# @author: Sreejith K
# Created On 19th Sep 2011


import urllib
import cgi


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
    return date.utcnow().strftime('%Y-%m-%dT%H:%M:%S+5:30')


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

__all__ = ['date_to_string', 'date_to_long_string', 'xml_escape', 'cgi_escape', 'uri_escape', 'number_of_words']