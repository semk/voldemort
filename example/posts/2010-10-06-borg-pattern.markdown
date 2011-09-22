---
layout: post
title: Borg Pattern
time: '10:45'
---

<!--begin excerpt-->
Singleton Design Patterns create all sorts of problems as you have exactly one instance for the singleton class throughout the program.
<!--end excerpt-->

{% highlight python %}
# Singleton implementation using new-style classes
class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Foo(Singleton):
    pass
{% endhighlight %}

{% highlight bash %}
>>> foo = Foo()
>>> bar = Foo()
>>> id(foo), id(bar)
(10049912, 10049912)
{% endhighlight %}

Usually programmers use Singleton Patterns as a global entry point to database connections. This is a bad programming habit. This will also break tests as most unittests use dummy implementations of real objects that emulate real objects. Suppose you have protected your class to instantiate only once using this pattern, then it would become impossible for him to stub/mock this class for tests. In short, Singleton patterns are not recommended for test driven development.

What we really care about class objects are its identity/state and behaviour, not the number of instances; unless you really need that kind of implementation. This is where Borg pattern comes as useful. Borg pattern share the same state across all its class instances. Its fairly easy to implement a Borg pattern in python. Just initialize the class `__dict__` with a class attribute in its `__init__`.

{% highlight python %}
# Borg Pattern
class Borg:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
{% endhighlight %}

Subclass this *Borg* class and you can have a shared-state class implementation and all the instances will have the same state. For more information about different patterns in python, checkout this [link](http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html).
