# -*- coding: utf-8 -*-
#
# Paginator for blog posts
#
# @author: Sreejith K
# Created On 19th Sep 2011


import math


class Paginator(object):

    def __init__(self, posts, paginate=5):
        self.__posts = posts
        self.__paginate = paginate
        self.rewind()

    def rewind(self):
        self.__paginate_start = 0 - self.__paginate
        self.__paginate_end = 0
        self.__total_pages = math.ceil(float(len(
            self.__posts)) / float(self.__paginate))
        self.__current_page = 0

    @property
    def posts(self):
        return self.__posts[self.__paginate_start:self.__paginate_end]

    @property
    def current_page(self):
        return self.__current_page

    @property
    def next_page(self):
        if self.__current_page == self.__total_pages:
            return None
        else:
            return self.__current_page + 1

    @property
    def previous_page(self):
        if self.__current_page == 1:
            return None
        else:
            return self.__current_page - 1

    def next(self):
        if self.__current_page < self.__total_pages:
            self.__paginate_start = self.__paginate_end
            self.__paginate_end += self.__paginate
            self.__current_page += 1
            return self
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def __repr__(self):
        return 'POSTS FROM %d to %d. PAGE NO: %d TOTAL: %d PREV: %s NEXT: %s' % (
            self.__paginate_start,
            self.__paginate_end,
            self.__current_page,
            self.__total_pages,
            self.previous_page,
            self.next_page)
