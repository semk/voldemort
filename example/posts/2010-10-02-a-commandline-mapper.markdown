---
layout: post
title: A commandline mapper
time: '23:28'
---

<!--begin excerpt-->
Python provides a builtin `map` function which applies a method over a list of entities. This function comes handy in a lot of situations as in
<!--end excerpt-->

{% highlight python %}
# find the square of all integers in a list
# Eg: 
#   input: [1, 2, 3, 4]
#   return: [1, 4, 9, 16]
map(lambda x: x*x, list_of_integers)
{% endhighlight %}

Similar functionality can be achieved in linux commandline using a combination of unix pipe `|` and `xargs` command. For my previous blog post I needed to resize the image sizes so that it fits correcly in the post. This is how I mapped the `convert` utility over a list of image files in a directory.

{% highlight bash %}
$ find . -name "*.jpg" -print0 | xargs -0 -I img convert -resize 600x450 img img
{% endhighlight %}

The `-print0` option for find list files without the EOF marker so that it can be used efficiently in `xargs`. The -0 option indicates this. You can use a replace string similar to `img` used here, to replace initial arguments of the command from standard input. See `man xargs` for more information about this utility.
