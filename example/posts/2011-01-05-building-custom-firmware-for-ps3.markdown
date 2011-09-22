---
title: Building Custom Firmware for PS3
layout: post
time: '22:00'
---

<!--begin excerpt-->
The 27th [Chaos Communication Congress](http://events.ccc.de/congress/2010/wiki/Welcome) revealed the [*Epic Programming Fail*](http://www.engadget.com/2010/12/29/hackers-obtain-ps3-private-cryptography-key-due-to-epic-programm/) on the PlayStation 3 security. 
<!--end excerpt-->
Finally it turned  out that Sony's ECDSA algorithm for signing apps use a random number generator which always returns the same number (No, I'm not kidding). The [fail0verflow](http://fail0verflow.com) team, who found out this fail, used the following famous [xkcd](http://xkcd.com) comic to describe Sony's ECDSA algorithm.

![Random Number](http://imgs.xkcd.com/comics/random_number.png)

*fail0verflow* demonstrated their work on [AsbestOS](http://marcansoft.com/blog/2010/10/asbestos-running-linux-as-gameos/), which is a bootloader for ps3 using which you can boot *Linux* on it. Currently this needs some wiring and soldering works but they have promised to release an easy to use tool sometime next month.

But [kakaroto](https://github.com/kakaroto)(the hacker behind aMsn and PL3 payload for *psgroove*) wasn't patient enough. He went on to develop some tools to create *custom firmware* for ps3. You can find the custom firmware generator code from [here](https://github.com/kakaroto/ps3utils). Currently it works on Linux and Mac. For those who doesn't know how to use these tools, the following steps would help.

First of all checkout the tools developed by *fail0verflow* team and build it. You might need to install `build-essential` and `zlib1g-dev` packages if you are using Ubuntu (use `sudo apt-get install`).

{% highlight bash %}
mkdir ~/src
cd ~/src
git clone git://git.fail0verflow.com/ps3tools.git
cd ps3tools
make
{% endhighlight %}

Now checkout the firmware generator code from kakaroto's GitHub repository and use the official firmware update (PS3UPDAT.PUP) to create the CFW.

{% highlight bash %}
mkdir ~/.ps3
cd ~/.ps3
git clone https://github.com/kakaroto/ps3keys.git .
cd ~/src
git clone https://github.com/kakaroto/ps3utils.git
cd ps3utils
make
./create_cfw.sh PS3UPDAT.PUP CFW.PUP
{% endhighlight %}

You can rename this CFW.PUP to PS3UPDAT.PUP and copy it to PS3->UPDATE directory of your pendrive and update the ps3 from the XMB. Still, this CFW does nothing but shows the *Install Application* option on XMB. You still have to wait until the homebrews are signed and repackaged with the retail `.pkg` format to install on this firmware.

#### Links ####

* [fail0verflow's presentation on Console Hacking](http://events.ccc.de/congress/2010/Fahrplan/attachments/1780_27c3_console_hacking_2010.pdf) - 27th Chaos Communication Congress

* [fail0verflow and Geohot Interview with BBC](http://www.bbc.co.uk/news/technology-12116051)
