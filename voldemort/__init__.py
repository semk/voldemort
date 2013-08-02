# -*- coding: utf-8 -*-
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
import urllib
from optparse import OptionParser
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

import template
import config
import util
import paginator


log = logging.getLogger('voldemort')

FEED_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

    <title>{{ site.name }}</title>
    <link href="{{ site.address }}/atom.xml" rel="self"/>
    <link href="{{ site.address }}"/>
    <updated>{{ site.time | date_to_xmlschema }}</updated>
    <id>{{ site.id }}</id>
    <author>
        <name>{{ site.author_name }}</name>
        <email>{{ site.author_email }}</email>
    </author>

    {% for post in posts %}
    <entry>
        <title>{{ post.title }}</title>
        <link href="{{ site.address }}{{ post.url }}"/>
        <updated>{{ post.date | date_to_xmlschema }}</updated>
        <id>{{ site.address }}{{ post.id }}</id>
        <content type="html">{{ post.content | xml_escape }}</content>
    </entry>
    {% endfor %}

</feed>
"""

SITE_MAP = """<?xml version='1.0' encoding='UTF-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

    {% for page in pages %}
    <url>
        <loc>{{ page.url }}</loc>
        <lastmod>{{ site.time | date_to_xmlschema }}</lastmod>
    </url>
    {% endfor %}

    {% for post in posts %}
    <url>
        <loc>{{ post.url }}</loc>
        <lastmod>{{ post.date | date_to_xmlschema }}</lastmod>
    </url>
    {% endfor %}

</urlset>
"""


class Voldemort(object):

    """Provides all the functionalities like meta-data parsing
    and site generation.
    """
    template_extensions = [
        '.htm', '.html', '.md', '.markdown',
        '.jinja', '.jinja2', '.txt', '.xml']
    preserved_extensions = ['.txt', '.xml']
    date_format = '%d-%m-%Y'

    def __init__(self, work_dir, conf):
        self.work_dir = work_dir
        self.config = conf
        self.logfile = os.path.join(self.work_dir, 'voldemort.log')
        self.tag_template = os.path.join(self.work_dir, 'tag.html')
        util.setup_logging(self.logfile, logging.DEBUG)
        log.info('Voldemort working at %s' % self.work_dir)
        template.setup_template_dirs(self.config.layout_dirs)
        template.setup_filters()
        # ignore the following directories
        self.ignored_items = [
            self.config.posts_dir,
            self.config.site_dir,
            self.logfile,
            self.tag_template,
            os.path.join(self.work_dir, '.git'),
            os.path.join(self.work_dir, '.DS_Store')
        ] + self.config.layout_dirs
        log.debug('The following list of directories/files will be ignored: %s'
                  % ', '.join(self.ignored_items))

    def init(self):
        """(Re)create the site directory.
        """
        if not os.path.exists(self.config.site_dir):
            log.debug('Creating %s' % self.config.site_dir)
            os.mkdir(self.config.site_dir)

    def serve(self, port):
        """Run an HTTPServer on the given port under the working directory.
        """
        # change to site directory
        os.chdir(self.config.site_dir)
        # start httpd on port
        server_address = ('', port)
        SimpleHTTPRequestHandler.protocol_version = 'HTTP/1.0'
        httpd = BaseHTTPServer.HTTPServer(
            server_address,
            SimpleHTTPRequestHandler)

        sa = httpd.socket.getsockname()
        log.info('Serving HTTP on %s port %s ...' % (sa[0], sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            log.info('Stopping httpd...')
            httpd.socket.close()

    def deploy(self, username, server_address, directory):
        """Deploy this website to the server
        """
        if server_address == 'github.com':
            log.info('Pushing updates to %s' % directory)
            if not os.path.exists(os.path.join(self.config.site_dir, '.git')):
                # initialize github page as a submodule
                log.info('Adding git@github.com:%s/%s.git as a submodule'
                         % (username, directory))
                os.system('git submodule add git@github.com:%s/%s.git %s'
                          % (username, directory, self.config.site_dir))
            os.system('cd %s && git add -A && git commit -am "Updated on %s" && git push origin master'
                      % (self.config.site_dir, datetime.datetime.now()))
            return

        if directory.startswith('~') or directory.startswith('.'):
            directory = directory.replace(directory[0], '/home/%s' % username)

        log.info('Deploying site at %s@%s:%s'
                 % (username, server_address, directory))
        try:
            os.system('rsync -rtzh --progress --delete %s/ %s@%s:%s/'
                      % (self.config.site_dir,
                         username,
                         server_address,
                         directory))
        except:
            log.error('Deployment failed.')

    def write_html(self, filename, data):
        """Write the html data to file.
        """
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError:
            pass
        with open(filename, 'w') as f:
            f.write(data.encode('utf-8'))

    def move_to_site(self, source, dest):
        """Move the file to the site.
        """
        log.debug('Moving %s to %s' % (source, dest))
        try:
            os.makedirs(os.path.dirname(dest))
        except OSError:
            pass
        shutil.copyfile(source, dest)

    def get_page_name_for_site(self, filename, extn='.html'):
        """Changes the file extension to html if needed.
        """
        directory, base = os.path.split(filename)
        name, ext = os.path.splitext(base)
        if ext not in self.template_extensions \
                or ext in self.preserved_extensions:
            return filename
        if directory == self.config.site_dir and name == 'index':
            name = name + extn
        else:
            name = os.path.join(name, 'index' + extn)
        return os.path.join(directory, name)

    def parse_meta_data(self):
        """Parses the meta data from posts
        """
        self.posts = []
        self.tags = {}
        for post in os.listdir(self.config.posts_dir):
            # ignore hidden files
            if post.startswith('.'):
                continue

            post = os.path.join(self.config.posts_dir, post)
            post_meta = template.get_meta_data(post)
            post_meta['date'] = datetime.datetime.strptime(
                post_meta['date'],
                self.date_format)
            post_url = os.path.join(
                '/',
                post_meta['date'].strftime(
                    self.config.post_url),
                os.path.splitext(
                    post_meta['filename'].split(
                        self.config.posts_dir)[1][1:])[0])
            post_meta['url'] = post_url
            self.posts.append(post_meta)

            # create tag cloud
            for tag in post_meta.get('tags', []):
                if tag in self.tags:
                    self.tags[tag].append(post_meta)
                else:
                    self.tags[tag] = [post_meta]

        # sort posts based on date.
        self.posts.sort(key=lambda x: x['date'], reverse=True)
        # sort tags based on date
        for tagname in self.tags:
            self.tags[tagname].sort(key=lambda x: x['date'], reverse=True)

        # include next and previous urls for posts. includes post tags
        for post_num, post in enumerate(self.posts):
            post_tags = []
            for tagname in post.get('tags', []):
                tag_url = os.path.join(
                    '/',
                    'tag',
                    urllib.quote_plus(tagname.lower()))
                post_tags.append(
                    {'name': tagname,
                     'url': tag_url,
                     'posts': self.tags[tagname]})
            post['tags'] = post_tags
            post['id'] = post['url']
            previous = post_num + 1
            next = post_num - 1
            if previous < len(self.posts):
                post['previous'] = self.posts[previous]
            else:
                post['previous'] = None
            if next >= 0:
                post['next'] = self.posts[next]
            else:
                post['next'] = None

        # tags for env
        tags_info = []
        for tagname, post in self.tags.iteritems():
            tag_url = os.path.join(
                '/',
                'tag',
                urllib.quote_plus(tagname.lower()))
            tags_info.append(
                {'name': tagname,
                 'url': tag_url,
                 'posts': self.tags[tagname]})

        # create paginator
        self.paginator = paginator.Paginator(self.posts, self.config.paginate)
        # create site information
        site = {}
        site['time'] = datetime.datetime.now()
        # extract site information from settings.yaml
        site.update(getattr(self.config, 'site', {}))
        # update the template global with posts info
        template.env.globals.update(
            {'posts': self.posts,
             'site': site,
             'tags': tags_info})

    def paginate(self, filename, page_meta):
        """Paginate the content in the file
        """
        log.info('Paginating page %s' % filename)
        for pgr in self.paginator:
            log.debug('Paginating: %s' % pgr)
            html = template.render(
                page_meta['raw'],
                {'page': page_meta, 'paginator': pgr})
            if pgr.current_page == 1:
                paginator_path = os.path.join(self.config.site_dir,
                                              filename.split(self.work_dir)[1][1:])
                log.debug('Generating page %s' % paginator_path)
                self.write_html(paginator_path, html)

            current_page = 'page%s' % pgr.current_page
            site_path, ext = os.path.splitext(
                filename.split(self.work_dir)[1][1:])
            if site_path == 'index':
                site_path = ''
            paginator_path = os.path.join(
                self.config.site_dir,
                site_path,
                current_page,
                'index.html')

            log.debug('Generating page %s' % paginator_path)
            # write the rendered page
            self.write_html(paginator_path, html)

    def generate_posts(self):
        """Generate the posts from the posts directory
        """
        log.info('Generating posts from %s' % self.config.posts_dir)
        for post in self.posts:
            html = template.render(
                post['raw'],
                {'post': post, 'page': post})
            # construct the url to the post
            post_url = os.path.join(self.config.site_dir, post['url'][1:])
            post_file = os.path.join(post_url, 'index.html')
            log.debug('Generating post: %s' % post_file)
            # write the html
            self.write_html(post_file, html)

    def generate_pages(self):
        """Generate HTML from all the other pages.
        """
        log.info('Generating pages')
        self.pages = []
        for root, dirs, files in os.walk(self.work_dir):
            # checks whether the directory is as subdirectory of root
            def is_a_subdirectory(sub):
                return sub in root
            # ignore all the subdirectories
            if any(map(is_a_subdirectory, self.ignored_items)):
                continue

            for filename in files:
                # ignore hidden files
                if filename.startswith('.'):
                    continue

                filename = os.path.join(root, filename)
                # ignore tag template
                if filename == self.tag_template:
                    continue

                _, extn = os.path.splitext(filename)
                if extn not in self.template_extensions:
                    dest = os.path.join(self.config.site_dir,
                                        filename.split(self.work_dir)[1][1:])
                    self.move_to_site(filename, dest)
                    continue

                page_meta = template.get_meta_data(filename)
                page_url = os.path.join(
                    '/',
                    os.path.splitext(
                        page_meta['filename'].split(self.work_dir)[1][1:])[0])
                page_meta['url'] = page_url
                self.pages.append(page_meta)
                # paginate if needed
                if page_meta.get('paginate', False) == True:
                    self.paginate(filename, page_meta)
                    continue

                html = template.render(page_meta['raw'], {'page': page_meta})
                page_path = os.path.join(
                    self.config.site_dir,
                    filename.split(self.work_dir)[1][1:])
                page_path = self.get_page_name_for_site(page_path)
                log.debug('Generating page %s' % page_path)
                # write the rendered page
                self.write_html(page_path, html)

    def generate_tags(self):
        """Generate tag pages.
        """
        log.info('Generating tags')
        tag_template_meta = template.get_meta_data(
            os.path.join(self.work_dir, self.tag_template))
        for tagname, posts in self.tags.iteritems():
            render_vars = {'tag': {'name': tagname, 'posts': posts},
                           'page': tag_template_meta}
            html = template.render(tag_template_meta['raw'], render_vars)
            tag_page_path = os.path.join(
                self.config.site_dir,
                'tag',
                urllib.quote_plus(tagname.lower()),
                'index.html')
            log.debug('Generating tag %s: %s' % (tagname, tag_page_path))
            # write the html page
            self.write_html(tag_page_path, html)

    def generate_feed(self, filename='atom.xml'):
        """Generate Atom feed
        """
        feed_path = os.path.join(self.config.site_dir, filename)
        feed = template.render(FEED_TEMPLATE)
        feed_path = self.get_page_name_for_site(feed_path)
        log.info('Generating Atom feed at %s' % feed_path)
        self.write_html(feed_path, feed)

    def generate_sitemap(self, filename='sitemap.xml'):
        map_path = os.path.join(self.config.site_dir, filename)
        log.info('Generating sitemap at %s' % map_path)
        sitemap = template.render(
            SITE_MAP,
            {'posts': self.posts, 'pages': self.pages})
        self.write_html(map_path, sitemap)

    def run(self, options):
        """Generate the site.
        """
        self.init()
        try:
            if os.path.exists(self.config.posts_dir):
                self.parse_meta_data()
            else:
                log.warning("No posts directory found. Ignoring posts.")

            if self.posts and not options.skip_blog:
                self.generate_posts()
            if not options.skip_pages:
                self.generate_pages()
            if not options.skip_tags:
                self.generate_tags()
            if not options.skip_feeds:
                self.generate_feed()
            if not options.skip_sitemap:
                self.generate_sitemap()
            log.info('Done.')
        except Exception as ex:
            log.error('ERROR: %s. Refer %s for detailed information.'
                      % (str(ex), self.logfile)
                      )
            log.debug('TRACEBACK: %r' % util.print_traceback())


def main():
    work_dir = os.path.abspath(os.getcwd())
    # check for commandline options
    usage = 'voldemort [options]'
    parser = OptionParser(usage)
    conf = config.load_config(work_dir)

    parser.add_option(
        '-s', '--serve',
        action='store_true', help='Start the HTTP Server',
        default=False)
    parser.add_option(
        '-p', '--port',
        help='Port inwhich the HTTPServer should run',
        type='int', default=8080)
    parser.add_option(
        '-d', '--deploy',
        action='store_true', help='Deploy this website',
        default=False)
    parser.add_option(
        '-u', '--user',
        help='Login name for server',
        default=conf.deploy.get('user'))
    parser.add_option(
        '-a', '--at',
        help='Server address to deploy the site',
        default=conf.deploy.get('at'))
    parser.add_option(
        '-t', '--to',
        help='Deployment directory',
        default=conf.deploy.get('to'))
    parser.add_option(
        '--skip-blog',
        action='store_true', help='Skip blog posts generation',
        default=False)
    parser.add_option(
        '--skip-pages',
        action='store_true', help='Skip pages generation',
        default=False)
    parser.add_option(
        '--skip-tags',
        action='store_true', help='Skip tags generation',
        default=False)
    parser.add_option(
        '--skip-feeds',
        action='store_true', help='Skip Atom feed generation',
        default=False)
    parser.add_option(
        '--skip-sitemap',
        action='store_true', help='Skip sitemap generation',
        default=False)

    # parse the options
    (options, args) = parser.parse_args()

    app = Voldemort(work_dir, conf)

    # validate options
    if options.serve:
        app.serve(options.port)
    elif options.deploy:
        if not options.user or not options.at or not options.to:
            print 'Operation is missing a few options.'
            parser.print_help()
            sys.exit(-2)
        app.deploy(options.user, options.at, options.to)
    else:
        app.run(options)


if __name__ == '__main__':
    main()
