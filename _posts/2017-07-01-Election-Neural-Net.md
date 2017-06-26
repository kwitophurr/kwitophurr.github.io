---
layout: post
title: "Were Votes in the 2016 Election Hacked?"
date: 2017-07-01
---

I have long subscribed to the belief that the worst thing about Donald Trump isn't his policies or his character- it's that he was able to get the support of enough Americans to win the Republican nomination, and ultimately the Presidency.
On some level, I have to make peace with the fact that regardless of whether or not voters were influenced by Russian propaganda or Comey's October Surprise, they still made a conscious choice to vote for Trump. 
However, a handful of recent revelations imply that the Russians didn't just attempt to influence voters, but to manipulate voter registrations or even alter votes after they were cast.
Is it possible that America voted against Trump, but the election was stolen?

On June 6 2017, NSA contractor [Reality Winner](https://www.theatlantic.com/news/archive/2017/06/who-is-reality-winner/529266/) was arrested on suspicion of leaking a top-secret document to The Intercept.
The document [alleges](https://theintercept.com/2017/06/05/top-secret-nsa-report-details-russian-hacking-effort-days-before-2016-election/) that Russia attempted to spear-phish up to 100 local election officials in up to seven states, with the intention of gaining access to their computer systems.
A week later, [Bloomberg](https://www.bloomberg.com/news/articles/2017-06-13/russian-breach-of-39-states-threatens-future-u-s-elections) reported that Russian hackers had attacked electronic voting infrastructure in up to 39 states. It goes without saying that if the Russians were trying to alter vote counts to get Donald Trump elected as president, the American people deserve to know.
Hopefully law enforcement and intelligence agencies will perform a thorough investigation and make their findings public- but that could take a very long time.

I wondered whether it is possible to detect voting interference without having direct access to the voting machines themselves. To find out, we need to start by putting ourselves in the mindset of Vladimir Putin, and assume that he has the capability and determination to pull this off.
## So you want to hack an election
For obvious reasons, you wouldn't want to get caught changing vote tallies. That means Putin can't use any of his usual shenanigans, like bussing people around to multiple voting sites. He's got to be more subtle- and that means tampering with voter registration and voting machines. We're going to make one big assumption here- we will assume that the vote-hacking would have been confined to only a handful of swing states. After all, it doesn't make much sense to try to swing California or New York for Trump. Moreover, your risk of getting caught by an astute observer increases as you expand the number of targets. If I were Putin, I would focus on states like Florida, North Carolina, Ohio, and Pennsylvania, which were the biggest swing states this election. (In hindsight, we know that Michigan and Wisconsin also had razor-thin margins and ultimately voted in favor of Trump, but in the weeks leading up to the election those states were widely considered safe ground for the Democrats.) 

Within each state, the same principle of maintaining a limited number of targets still applies- only this time the only thing that matters is the popular vote within the state. 
Therefore it makes sense to target only the big population centers within each swing state. 
A few tens of thousands of votes changed one way or another will go unnoticed in Charlotte, for example, but would be highly conspicuous in a small county. 
And a few tens of thousands of votes could be all you need to swing a state one way or another.

Of course, this assumption could be wrong- perhaps Putin was more brazen than I'm guessing and he decided to swing for the fences (as the media reports suggest) and attack election systems nationwide.
Or maybe his goal wasn't actually to swing the election one way or another, but simply to cause mass distrust of our democratic systems.
In either case, he wouldn't have localized his vote tampering to a handful of places, and it would be difficult to detect in the way I'll describe here.

As it turns out, we will still learn interesting things from this analysis whether this assumption we are making is true or false.

To recap: we're going to make an educated guess that the places most likely to be a target for vote tampering are the handful of counties that contain large-ish cities, in swing states. But the big question still remains- how would we know if the votes counts in those counties are valid or not? What we need is an accurate, county-by-county prediction of how that county is likely to vote, which we can then compare to the actual voting returns. To do this, we'll turn to machine learning.

## Crunching numbers with neural nets
There's been a lot of buzz in recent months about what so-called "deep learning" can do in fields like image classification and voice recognition.
For this analysis, however, we don't need anything particularly fancy; a good old-fashioned neural net will do just fine.
For the inputs we will provide it with readily-available demographic information- things like median income, population density, and how that county voted in years past.
And to train it, we can just use the actual results of the election.

I downloaded a bunch of data from the St. Louis Federal Reserve [website](http://geofred.stlouisfed.org/map/), which has a very convenient interface for getting county-level data.
Finding county-level election results is a bit trickier, but luckily I found that GitHub user [tonmcg](https://github.com/tonmcg/County_Level_Election_Results_12-16) had already compiled the data into a nice spreadsheet.
All of the data that I used are available on the [GitHub page](http://github.com/christian-johnson/election-neural-net) for this project, under the folder "data_spreadsheets".

A couple of quick notes about the data used here:
* For some reason, county-level voting information is not available for Alaska, so this analysis is only applicable to the other 49 states. 
* Election results are somewhat complicated due to the presence of third-party candidates. I'm just going to ignore third parties, so everywhere I reference a vote fraction, that's calculated as percentage of the two main vote shares. For example, the vote margin in Figure 1 below is found by: (GOP-DEM)/(GOP+DEM)

Figure 1:
![Election Results]: https://christian-johnson.github.io/election-neural-net/plots/election_results.tiff?raw=true "2016 US Presidential Election Results"

Once the data is loaded into a nice format (which takes a bit of work- that's the purpose of the function *load_data.py*), we can create a neural net using a Python class called [MLPRegressor](http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor) from the open-source package [Scikit-learn](http://scikit-learn.org/stable/index.html). This makes things very easy- the essential code is only a few lines:

{% highlight python %}
from sklearn.neural_network import MLPRegressor as mlp
nn = mlp(verbose=True)
nn.fit(training_inputs, training_outputs)
results = nn.predict(test_inputs)
{% endhighlight %}

Here I've broken up the data into two pieces: "training" and "test". If I have a hunch that Florida's votes have been hacked, then the Florida counties are my "test" data, and the rest of the country is my "training" data. Of course, the proof is in the pudding- how well does this neural net actually work? It turns out to work pretty well- see, for example, the actual and predicted vote counts in Pennsylvania:

The obvious thing to do next is to look at deviations in the data from the prediction, and see if any counties have a large excess of Trump votes. But this can be tricky to interpret on its own, because random fluctuations in small counties can be pronounced. What we actually want is a measure of the significance of a given deviation. I calculated

TL;DR: [Betteridges Law of Headlines](https://en.wikipedia.org/wiki/Betteridge%27s_law_of_headlines)
