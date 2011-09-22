---
title: Learn web development with Flask
layout: post
time: '14:45'
---

<!--begin excerpt-->
I've seen many people jumping into web development with feature-complete frameworks like [Django](http://www.djangoproject.com/) and [Rails](http://rubyonrails.org/). But most of them will find it difficult to assimilate the web development concepts because of cluttered documentation (incase of Rails) or complexity (incase of Django). 
<!--end excerpt-->
One might need to look at a simpler microframework to learn from scratch. And yes, [Flask](http://flask.pocoo.org/) is the one you'd want to have a look at.

Flask is a microframework for Python based on [Werkzeug](http://www.pocoo.org/projects/werkzeug/), and [Jinja 2](http://www.pocoo.org/projects/jinja2/). It is developed by the same guys at [Pocoo](http://www.pocoo.org/) who gave us [Sphinx](http://www.pocoo.org/projects/sphinx/) and [Pygments](http://www.pocoo.org/projects/pygments/) (a Python based syntax highlighter which beautifies the codes shown in this website). If you are new to the world of web development, with Flask you'd find it easier to understand the basics concepts like *sessions*, *cookie*, *templates* etc.

Flask provides a more developer friendly routing mechanism. You can define the routes to handlers with the help of a simple python decorator. That means no pain-in-the-ass for defining routes and writing handlers separately. Let's have a look at a sample *Hello World* application in Flask. I don't think you might need an explanation to this code :-)

{% highlight python %}
# Hello World in Flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
{% endhighlight %}

If you want to look at some really cool applications using Flask, never hesitate to checkout the code from [here](https://github.com/mitsuhiko/flask/tree/master/examples).
