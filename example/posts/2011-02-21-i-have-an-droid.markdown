---
title: I have an'droid
layout: post
time: '23:00'
---

<!--begin excerpt-->
Finally my wish came true. Now I'm a proud owner of an Android phone. Its LG Optimus One, better known as LG P500. Good that it comes with Froyo and LG promises an update to Gingerbread. Here you can find the phone [specs](http://www.gsmarena.com/lg_optimus_one_p500-3516.php).
<!--end excerpt-->

![LG Optimus One](http://www.gadgetvenue.com/wp-content/uploads/2010/09/LG-optimus-one-300x300.jpg)

This one is a good choice for anyone looking for a budget Android phone (10.8K when I bought) whose battery lasts a complete day with internet on. Thanks to [Shuveb](http://binarykarma.org) for providing a review of the phone and atlast making me buy it :-P

Eventhough a Pythonista like me hates Java, the Android platform was tempting me to look at Java with some interest. So I bought *Android Application Development by O'Reilly* and setup a Development Environment on my laptop using Eclipse. This was so easy that I could run the *Hello World* program without even writing a piece of Java code. Once you create a Project, it auto-generates files needed for the application to show on the foreground and other resource files and build scripts. By default, they'll create an activity source file with an *Activity* name you've given. This is pretty much the *Hello World* program we wanted.

{% highlight java %}
package com.semk.helloworld;

import android.app.Activity;
import android.os.Bundle;

public class HelloWorldActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }
}
{% endhighlight %}

Google has done a great job in developing an easy-to-use and feature-abundant SDK for Android. The Android emulator which comes with the SDK is an engineering masterpiece. It helps the developer to run and test their applications locally before running them on the actual devices.

![Android Emulator](/images/posts/2011-02-21-i-have-an-droid/emulator.png)

I'm hoping to develop some useful applications for Android while I finish reading the book. So keep an eye on my [Git Repo](http://github.com/semk).
