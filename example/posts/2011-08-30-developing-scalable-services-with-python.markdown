---
title: Developing scalable services with Python
layout: post
time: '22:08'
---

<!--begin excerpt-->
Developing multi-threaded applications in python is a "Pain In The Ass". And the [GIL](http://wiki.python.org/moin/GlobalInterpreterLock) (Global Interpreter Lock) takes away the advantage of utilizing multiple cores in a machine. It doesn't matter how many cores a CPU have, GIL prevents threads from running in multiple cores. So python programs would't get the maximum performance out of the CPU when they use threads in their services.
<!--end excerpt-->

In many cases you might need to write services where you need to listen on a port and wait for the client connection to do some task. If multiple clients are connecting to this service simultaneously then you might need to spawn threads to handle the requests. Considering the fact that GIL introduces a performance bottleneck, the best way to solve this situation is to use python's [multiprocessing](http://docs.python.org/library/multiprocessing.html) capabilities. This library provides almost `threading` like class implementations. 

Then a question might arise. How do you share a socket created by the server process to the newly spawned processes? It is possible since all the `fork`ed processes will have the parent's file descriptors. `multiprocessing` library already has this package named `multiprocessing.reduction` that provides a method `reduce_handle` which can serialize a socket and you can send this socket to another process using pipes. The child processes can read from the pipe and re-create the socket using `rebuild_handle`. The following example will make this idea clear to you.

{% highlight python %}
# Main Process
from multiprocessing.reduction import reduce_handle
# serialize the socket
serialized_socket = reduce_handle(client_socket.fileno())
# send it to the child/worker process
pipe_to_worker.send(serialized_socket)

# Worker Process
from multiprocessing.reduction import rebuild_handle
# get the socket from parent
serialized_socket = pipe_from_parent.recv()
# rebuild the file descriptor
fd = rebuild_handle(serialized_socket)
# create socket from fd
client_socket = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
# use the socket as usual. eg: send a message to the client
client_socket.send("Baby, I\'m so fast\r\n")
{% endhighlight %}

### Preforking
Another way to solve this issue is by spawning multiple process from the main server which is listening on a socket/port and letting all the child processes to `accept()` connections from the client. Apache uses this style of process scaling known as "Preforking". A simple example using `multiprocessing` module which runs an instance of a `BaseHTTPServer.HTTPServer` on a pool of worker processes can be written very easily as follows.

{% highlight python %}
#
# Example where a pool of http servers share a single listening socket
#
# On Windows this module depends on the ability to pickle a socket
# object so that the worker processes can inherit a copy of the server
# object.  (We import `multiprocessing.reduction` to enable this pickling.)
#
# Not sure if we should synchronize access to `socket.accept()` method by
# using a process-shared lock -- does not seem to be necessary.
#
# Copyright (c) 2006-2008, R Oudkerk
# All rights reserved.
#

import os
import sys

from multiprocessing import Process, current_process, freeze_support
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

if sys.platform == 'win32':
    import multiprocessing.reduction    # make sockets pickable/inheritable


def note(format, *args):
    sys.stderr.write('[%s]\t%s\n' % (current_process().name, format%args))


class RequestHandler(SimpleHTTPRequestHandler):
    # we override log_message() to show which process is handling the request
    def log_message(self, format, *args):
        note(format, *args)

def serve_forever(server):
    note('starting server')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def runpool(address, number_of_processes):
    # create a single server object -- children will each inherit a copy
    server = HTTPServer(address, RequestHandler)

    # create child processes to act as workers
    for i in range(number_of_processes-1):
        Process(target=serve_forever, args=(server,)).start()

    # main process also acts as a worker
    serve_forever(server)


def test():
    DIR = os.path.join(os.path.dirname(__file__), '..')
    ADDRESS = ('localhost', 8000)
    NUMBER_OF_PROCESSES = 4

    print 'Serving at http://%s:%d using %d worker processes' % \
          (ADDRESS[0], ADDRESS[1], NUMBER_OF_PROCESSES)
    print 'To exit press Ctrl-' + ['C', 'Break'][sys.platform=='win32']

    os.chdir(DIR)
    runpool(ADDRESS, NUMBER_OF_PROCESSES)


if __name__ == '__main__':
    freeze_support()
    test()
{% endhighlight %}

I wrote a simple wrapper for this kind of services which can be scaled. You can find it [here](http://github.com/semk/utils/prefork_server.py).