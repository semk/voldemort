---
layout: post
title: Hacking PlayStation 3 with Teensy 2.0
time: '18:28'
---

<!--begin excerpt-->
I've always been a proud and loyal owner of a [Playstation 3](http://en.wikipedia.org/wiki/PlayStation_3) and still I consider it as the most powerful game console of this generation. But things were super-cool back on the days when [Playstation 3](http://en.wikipedia.org/wiki/PlayStation_3) supported [OtherOS](http://en.wikipedia.org/wiki/OtherOS) by which you could boot and use Linux on your console. 
<!--end excerpt-->
This was the very feature (other than GameOS which is why someone should buy a PS3 :-)) every PS3 owner was proud of when comparing his console to its counterparts. This feature was removed by Sony after [Geohot's](http://en.wikipedia.org/wiki/George_Hotz) attempts to hack [Playstation 3](http://en.wikipedia.org/wiki/PlayStation_3) using Linux. Although he was partially succeeded in doing so, soon he disappeared from the PlayStation hacking scene and asked other hackers to continue his work. The PS3 users gained nothing from this untill the mighty [PSJailbreak](http://psjailbreak.com) was announced.

I must say, Sony guys have made [Playstation 3](http://en.wikipedia.org/wiki/PlayStation_3) almost unhackable as it took more than 4 years for the console hackers to find an exploit to allow homebrews on it. This exploit which was found in firmware 3.41, allows users to backup *Legitimate* Copies of PlayStation Games to internal/external harddisk. This is achieved by installing an application called Backup Manager. The team to announce this hack was [PSJailbreak](http://psjailbreak.com), who used a USB dongle to boot from which took advantage of the exploit found in 3.41. Later open source implementations of [PSJailbreak](http://psjailbreak.com) like [psgroove](http://github.com/psgroove/psgroove), psfreedom etc. came which used popular development boards like [Teensy ++](http://www.pjrc.com/store/teensypp.html) and [Atmel AT90USBKEY](http://www.atmel.com/dyn/products/tools_card.asp?tool_id=3879).

I was really excited to see this progress and I liked the idea of backing up games. If you buy Original Games for $50, atleast there should be one way to make backups so that you can play games even if yor media is damaged. So I logged on to [pjrc](http://pjrc.com) and ordered one [Teensy 2.0 USB Development Board](http://www.pjrc.com/teensy/) which used [Atmel ATMEGA32U4 AVR](http://www.atmel.com/dyn/products/product_card.asp?part_id=4317). It took almost 3 weeks to ship to India from US. I checked out [psgroove](http://github.com/psgroove/psgroove) code from GitHub and used the Teensy Loader utility to flash the compiled hex code to the board.

For this jailbreak to work, you need to hard power your PS3 after connecting the usb board. Turn on the console and immediately press eject button for the exploit to work. If everything goes proper, the orange led in Teensy board will light up. Tada! The PlayStation is Jailbroken. Take a look at the snaps I took during Jailbreaking my console.

![Flashed Teensy](/images/posts/2010-10-02-hacking-playstation3-with-teensy/teensy_loaded.jpg)

![Exploited](/images/posts/2010-10-02-hacking-playstation3-with-teensy/exploited.jpg)

![Installing](/images/posts/2010-10-02-hacking-playstation3-with-teensy/installing.jpg)

![Backup Manager](/images/posts/2010-10-02-hacking-playstation3-with-teensy/backup_manager.jpg)

![Backup Manager Page](/images/posts/2010-10-02-hacking-playstation3-with-teensy/bm_screen.jpg)

![Backing up Uncharted](/images/posts/2010-10-02-hacking-playstation3-with-teensy/backing_up.jpg)

![FTP Server](/images/posts/2010-10-02-hacking-playstation3-with-teensy/ftp_server.jpg)

The latest firmware update from Sony patches this exploit and even they are banning consoles using Backup Manager when they connect to [PSN](http://en.wikipedia.org/wiki/PlayStation_Network). As I love [PSN](http://en.wikipedia.org/wiki/PlayStation_Network) and playing [Uncharted 2](http://en.wikipedia.org/wiki/Uncharted_2:_Among_Thieves) online, soon I have to update my firmware to 3.50. Even legitimate users are irritated by this move by Sony. If iPhone Jailbreak is legal, this is also legal. Right ?

Had Sony not removed [OtherOS](http://en.wikipedia.org/wiki/OtherOS), none of this would have happened OR atleast it would have taken more time for the hackers to hack the console. "Sony, never do stupid things like this anymore. Please bring back [OtherOS](http://en.wikipedia.org/wiki/OtherOS)." 
