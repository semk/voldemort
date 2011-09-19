#! /usr/bin/env python
#
# Methods for blog posts handling
#
# @author: Sreejith K
# Created On 19th Sep 2011


class Post(object):
    """ Represents a blog post
    """
    pass


class PostsIterator(object):
    """ Iterates through the blog posts.
    """
    def __init__(self):
        self._posts = []
        self.rewind()

    def add(self, data):
        """ Set the attributes.
        """
        new_post = Post()
        for attr, value in data:
            setattr(post, data, value)
        self._posts.append(new_post)

    def rewind(self):
        """ Reset the iterator
        """
        self._current_index = 0

    def next(self):
        """ Find next item in this iterator
        """
        if self._current_index >= len(self._posts):
            raise StopIteration
        self._current_index += 1
        return self.posts[self._current_index]
        
    def __len__(self):
        return len(self._posts)

    def __iter__(self):
        return self