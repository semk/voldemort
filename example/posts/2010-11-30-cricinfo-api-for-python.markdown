---
layout: post
title: Cricinfo api (unofficial) for Python
time: '18.00'
---

<!--begin excerpt-->
Recently I started developing a Python [library](https://github.com/semk/cricinfo) for accessing live information from [ESPN Cricinfo](http://espncricinfo.com) like live scores, innings details and player profiles. Currently, it only fetches live match information using a simple Python iterator.
<!--end excerpt-->

{% highlight python %}
# instantiate
matches = CricInfo()
# iterate though matches
for match in matches:
    # match title
    print match.title
    # a short desciption for the match
    print match.description
    # url to live scorecard
    print match.link
    print match.guid
{% endhighlight %}

I wish to add features for every match like full scorecard, innings details etc in a similar manner. A plan for getting player profile is also in my mind. I'd like to make this as human-readable as possible. For example, innings information can be fetched by an iteration over the Match object. 

{% highlight python %}
# getting innings info
for innings in match:
    print innings.score
    print innings.current_batsmen
    print innings.overs
    print innings.wickets
{% endhighlight %}

I'll update about the changes being done for the api. So keep reading my blog. I need your suggestions to make it a useful one. 
