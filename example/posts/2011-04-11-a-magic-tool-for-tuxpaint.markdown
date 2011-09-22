---
title: Scratch - A Magic Tool for Tux Paint
layout: post
time: '20:45'
---

<!--begin excerpt-->
[Tux Paint](http://tuxpaint.org/) is a drawing software for children that provides a kids-like user interface. Tuxpaint does have some nice tools integrated in it which helps the kids to create their drawing [masterpieces](http://tuxpaint.org/gallery/) using a computer. Simply speaking its the GIMP for kids of 3-12 years.
<!--end excerpt-->

But what I was excited about Tux Paint is the availability of [Magic Tool Plug-in API](http://www.tuxpaint.org/presentations/tuxpaint-magic-api.pdf) using which you can create Magic Tools that creates some sort of graphical effect on the canvas. Tux Paint already provides some Magic Tools by default like blur, bricks etc. Tux paint is fully written in C and uses [SDL](http://libsdl.org) for graphics programming. There are basically two kinds of tools we can create using the API. One that affects the whole canvas and one that updates a specific region of the canvas (eg. place where you drag the cursor).

![Scratch effect on Bricks](/images/posts/2011-04-11-a-magic-tool-for-tux-paint/scratch_on_bricks.png)

To test how this API works, I actually developed a [Scratch Magic Tool](https://github.com/semk/tp-scratch) which when you apply, creates a *scratched* effect on the image (as shown above). It also produces a nice sound effect while applying the effect. Still this tool has a lot of logical bugs so that sometimes it doesn't even look like a scratch when applied over certain colors :-). Other than that, you can use this code for a reference to create your own Magic Tools. If you need documentation this presentation [slide](http://www.tuxpaint.org/presentations/tuxpaint-magic-api.pdf) is more than enough. Once you have downloaded the Tux Paint source code go through `src/tp_magic_api.h` to see the all API definitions and usage.

Back in the college days, we had this subject on *Computer Graphics* where you need to study some popular [line-drawing](http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm) and [circle-drawing](http://en.wikipedia.org/wiki/Midpoint_circle_algorithm) algorithms. But there were no lab sessions for those subjects. Everyone where literally by-hearting those algorithms at that time. I would suggest all the CS faculty to conduct a lab session on Computer Graphics and ask students to implement those algorithms as a Magic Tool in Tux Paint using the Magic Tool API. It will be useful for them to see those algorithms in action. You may use my plugin or other plugins available in Tux Paint's `magic/src/`  directory as a reference for your development. Please do give a feedback here in the comment section when you implement some of these algorithms as a Magic Tool.

*NOTE:* For compilation and installation of Tux Paint from sources, follow the instructions from [tp-scratch repository](https://github.com/semk/tp-scratch).
