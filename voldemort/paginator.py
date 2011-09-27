#! /usr/bin/env python
#
# Paginator for blog posts
#
# @author: Sreejith K
# Created On 19th Sep 2011


class Paginator(object):

    def __init__(self, posts, paginate=5):
        self.__posts = posts
        self.__paginate = paginate

    @property
    def posts(self):
        return PostsIterator(self.__posts[:self.__paginate])


class PostsIterator(object):
    
    def __init__(self, posts):
        self.__posts = posts
        self.rewind()

    def rewind(self):
        self.__pos = 0

    def next(self):
        if self.__pos < len(self.__posts):
            post = self.__posts[self.__pos]
            self.__pos += 1
            return post
        else:
            raise StopIteration

    def __iter__(self):
        return self

    