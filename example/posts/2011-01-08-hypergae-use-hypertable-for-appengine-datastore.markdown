---
title: HyperGAE - Use Hypertable for App Engine Datastore
layout: post
time: '03:30'
---

<!--begin excerpt-->
After few days of hacking on the [Google App Engine SDK](http://code.google.com/appengine/docs/python/overview.html) and [ProtocolBuffers](http://code.google.com/apis/protocolbuffers/docs/pythontutorial.html), finally I succeeded in creating a datastore driver for GAE that talks to [Hypertable](http://hypertable.org) and stores the data there *fully protocol buffer encoded*.
<!--end excerpt-->
If you want to checkout this implementation head to [HyperGAE](https://github.com/semk/hypergae) repository and see [files](https://github.com/semk/hypergae/tree/master/google/appengine/datastore) `datastore_hypertable_ht.py` and `datastore_hypertable_thrift.py`. HyperGAE basically uses two methods to connect to hypertable. Using the thrift api and using the boost-python library [ht](http://code.google.com/p/python-hypertable/). The mentioned drivers provides these api connections to hypertable.

To run App Engine sdk with hypertable support, do

{% highlight bash %}
python dev_appserver.py demos/guestbook/ --use_hypertable
{% endhighlight %}

The above command assumes hypertable [0.9.3.4](http://www.hypertable.com/download/0.9.3.4.html) installed and running on your machine. It uses the thrift connection by default. I need to add support for configuring hypertable options though `dev_appserver.py` script. Suggestions and patches are always welcome.

*UPDATE:* The drivers api has been modified to accommodate the new Hypertable and Thrift api changes. You must install Hypertable version [0.9.4.3](http://www.hypertable.com/download/) for HyperGAE to work. More updates to follow.
