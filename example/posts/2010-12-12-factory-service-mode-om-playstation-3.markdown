---
layout: post
title: Factory/Service mode on PlayStation 3 
time: 01:18
---

<!--begin excerpt-->
Here is a happy news for those who updated to firmware `>3.41` and didn't get a chance to enjoy the homwbrews for PS3. Yes, atlast we'll be able to downgrade the PS3 firmware to any version `<3.50`. The actual PSJailbreak team were the first team to release the downgrade.
<!--end excerpt-->
But many thanks to [zAxis](https://github.com/zAxis) who created [PSGrade](https://github.com/zAxis/PSGrade), an opensouce version of PSDowngrade. Using this we can put the PS3 into Factory/Service mode (Downgrade) using popular development boards like Teensy and AT90USBKEY.

We should also be thankful to [KaKaRaTo](https://github.com/kakaroto) who reversed the PS3Yes Key and made it available for PSGrade. Here is PS3Yes key which he reversed from its hex.

> 0×04, 0x4E, 0×61, 0x1B, 0xA6, 0xA6, 0xE3, 0x9A, 0×98, 0xCF, 0×35, 0×81, 0x2C, 0×80, 0×68, 0xC7, 0xFC, 0x5F, 0x7A, 0xE8

You'll need to specify this key in PSGrade sources (key.c as shown below) for the service mode hack to work. But now zAxis has updated the code with this key. So all you have to do is download the souces and compile the hex for your board.

{% highlight c %}
const uint8_t jig_key[20] = {
0x04, 0x4E, 0x61, 0x1B, 0xA6, 0xA6, 0xE3, 0x9A, 0x98, 0xCF, 
0x35, 0x81, 0x2C, 0x80, 0x68, 0xC7, 0xFC, 0x5F, 0x7A, 0xE8 
};
{% endhighlight %}

As I was already there in firmware 3.50, I had a chance to test PSGrade. I compiled the sources for my Teensy 2.0 board and wrote the hex files to it. Using the same PSJailbreak methods I booted the PS3 with the Teensy board in the usb port and rebooted after the hack got executed (Teensy LED will glow). It booted into the service mode quickly and I got a screen as shown below.

![Service Mode](http://www.ps3hax.net/wp-content/uploads/2010/12/SERVICE.jpg)

For exiting from the service mode you need to copy a special file (Lv2diag.self) to a usb storage drive and boot the PS3. Otherwise your PS3 will still be on service mode.

If you wish to downgrade the firmware (which I haven't performed yet) follow these downgrade steps from [here](http://psgroove.com/content.php?501-PS3Yes-Release-Free-PSGRADE-Downgrade-Hex-Works-on-All-AT90usb162-Boards).
