# -*- coding: utf-8 -*-
#
# Voldemort config
#
# @author: Sreejith K
# Created On 19th Sep 2011


import os
import logging

from yaml import load, dump, Loader, Dumper


log = logging.getLogger(__name__)


DEFAULT_CONFIG = """\
# voldemort configuration file
layout_dirs :
              - layout
              - include
posts_dir   : posts
site_dir    : _site
post_url    : "%Y/%m/%d"
paginate    : 5
"""


class Config(object):

    """Converts a dict to object.
    """
    def __init__(self, dict):
        self.__dict__.update(dict)


def load_config(work_dir, name='settings.yaml'):
    """Loads the configuration from the working directory. Else loads
    the default config.
    """
    log.info('Loading voldemort configuration')
    config_file = os.path.join(work_dir, name)
    if not os.path.exists(config_file):
        write_config = raw_input(
            'No configuration file found. Write default config? [Y/n]: ')
        write_config = (
            write_config == 'Y' or
            write_config == 'y' or
            write_config == '') and True or False
        if write_config:
            log.info('Writing default config at %s' % config_file)
            with open(config_file, 'w') as f:
                f.write(DEFAULT_CONFIG)

    # read the config file
    with open(config_file, 'r') as f:
        config = load(f, Loader=Loader)
    # add the missing configurations
    default_config = load(DEFAULT_CONFIG, Loader=Loader)
    default_config.update(config)
    config = Config(default_config)

    # fix the paths
    config.layout_dirs = [os.path.join(
        work_dir, ld) for ld in config.layout_dirs]
    config.posts_dir = os.path.join(work_dir, config.posts_dir)
    config.site_dir = os.path.join(work_dir, config.site_dir)
    return config
