---
layout: post
title: "Were Votes in the 2016 Election Hacked?"
date: 2017-06-01
categories: jekyll update
---

I have long subscribed to the belief that the worst thing about Donald Trump isn't Donald Trump- it's that someone like him could get so many supporters.
Despite my shock at the outcome of the 2016 election, I made peace with the fact that these voters made a conscious choice (however vile) to vote for Trump, regardless of whether or not they may have been influenced by a Russian propaganda machine.
However, a handful of recent revelations imply that the Russians didn't just attempt to influence voters, but to manipulate voter registrations or even alter votes after they were cast.
Is it possible that America voted against Trump, but the election was stolen?

My interest in this subject was piqued on June 6, when NSA contractor [Reality Winner](https://www.theatlantic.com/news/archive/2017/06/who-is-reality-winner/529266/) was arrested on suspicion of leaking a top-secret document to The Intercept.
The document [alleges](https://theintercept.com/2017/06/05/top-secret-nsa-report-details-russian-hacking-effort-days-before-2016-election/) that Russia attempted to spear-phish up to 100 local election officials in up to seven states, with the intention of gaining access to their computer systems.
A week later, [Bloomberg](https://www.bloomberg.com/news/articles/2017-06-13/russian-breach-of-39-states-threatens-future-u-s-elections) reported that Russian hackers had attacked electronic voting infrastructure in up to 39 states.
Suspicion that Russia had gained access to our voting systems was given confirmation with the [announcement](http://time.com/4828306/russian-hacking-election-widespread-private-data/) that voting systems in Illinois had been compromised to at least a partial extent.

I wondered whether it is possible to detect voting interference without having direct access to the voting machines or computer systems themselves. To find out, I started by putting ourselves in the mindset of Vladimir Putin, and thought about how I would have done it.
## So you want to hack an election
I'm going to make one big assumption here- I will assume that the vote-hacking would have been confined to only a handful of swing states. After all, it doesn't make much sense to try to swing California or New York for Trump. Moreover, your risk of getting caught by an astute observer increases as you expand the number of targets. If I were Putin, I would have focused my efforts on states like Florida, North Carolina, Ohio, and Pennsylvania, which were the most prominent swing states this election. 

Within each state, I would still want to only target a handful of places (to minimize risk of detection)- only this time it would make sense to attack only the big population centers.
That's because within a state, the only thing that matters is the popular vote- so why waste your time on a small county? 
Plus, this technique is more subtle: a few tens of thousands of votes changed one way or another might go unnoticed in Charlotte, but would be highly conspicuous in a small county. 
And a few tens of thousands of votes could be all you need to swing a state one way or another.

Of course, this assumption could be wrong- perhaps Putin was more brazen than I'm guessing and he decided to swing for the fences (as the Bloomberg report suggests) and attack election systems nationwide.
Or maybe his goal wasn't actually to swing the election one way or another, but simply to cause mass distrust of our democratic systems (in which case, the very existence of this blog post shows that he may have succeeded).
So it's entirely possible he wouldn't have localized his vote tampering to a handful of places, and it would be more difficult (if not impossible) to detect in the way I'll describe here.

Fortunately, it turns out that we can still learn some interesting things from this analysis whether the assumption is true or false.

To recap: I'm making an educated guess that the places most likely to be a target for vote tampering are the handful of counties that contain large-ish cities, in swing states. But the question still remains- how would we know if the votes counts in those counties are valid or not? What we need is an accurate, county-by-county prediction of how each county is likely to vote, which can then be compared to the actual voting results. To do this, let's turn to machine learning.

## Number crunching with neural nets
Machine learning has been in the news a lot recently, with people buzzing about what so-called "deep learning" can do in fields like image classification and voice recognition (take, for example, the recent [Apple WWDC keynote](https://techpinions.com/the-overlooked-surprises-of-apples-wwdc-keynote/50282)).
But for this analysis we don't need anything particularly fancy; a good old-fashioned neural net will do just fine (if you're new to machine learning, I recommend this [YouTube video](https://www.youtube.com/watch?v=bxe2T-V8XRs) to explain the basics of how a neural net works).
For the inputs we will provide it with readily-available demographic information- things like median income, population density, and voting results from years past.
And to train it, we can just use the actual results of the election.

I downloaded a bunch of demographic data from the St. Louis Federal Reserve [website](http://geofred.stlouisfed.org/map/), which has a very convenient interface for getting county-level data.
Finding county-level election results is a bit trickier, but luckily I found that GitHub user [tonmcg](https://github.com/tonmcg/County_Level_Election_Results_12-16) had already compiled the data into a nice spreadsheet.
All of the data that I used are available on the [GitHub page](http://github.com/christian-johnson/election-neural-net) for this project, under the folder [data_spreadsheets](https://github.com/christian-johnson/election-neural-net/tree/master/data_spreadsheets).

A couple of quick notes about the data used here:

1. There are 25 different data points on each county- the exact data points I used are listed at the end of this post. The most notable absence is religious affiliation, which wasn't available from the Federal Reserve site (if you know a good resource for where to find this information, feel free to drop me an email). This has a strong impact later in places like Utah, as we'll see. 

2. For some reason, county-level voting returns are not available for Alaska, so this analysis is only applicable to the other 49 states. 

3. For a handful of counties in South Dakota (Perkins, Roberts, Pennington, and Sanborn), the data from the Federal Reserve seems to have wild inconsistencies between 2009 and 2010, with each experiencing dramatic jumps in population. Since this seems to be a problem with the data and not the analysis, I excluded these counties by hand as well. I contacted the Federal Reserve, and have been informed that they are looking into the issue.

4. Polk County, TX had incorrect results in tonmcg's data- I replaced it with the data from the [Texas Secretary of State's data](http://elections.sos.state.tx.us/elchist319_race62.htm) instead. As far as I could tell, the rest of the results in Texas were consistent between the data sets to within a few votes.

5. When running the neural net, I also excluded counties that are missing data points for one reason or another. This affects another handful of counties, but hopefully doesn't have too big an impact on the final results.

6. Election results are somewhat complicated due to the presence of third-party candidates. I just ignored third parties, so everywhere I use a vote fraction, that's calculated as percentage of the two main vote shares. For example, the vote margin in Figure 1 below is found by: (GOP-DEM)/(GOP+DEM). Turnout is calculated as (GOP+DEM)/eligible voters.

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/National_vote_fraction.jpg" description="_Figure 1: 2016 US Presidential Election Results. The colors in the image are scaled such that a county that voted 50-50 would appear white, while counties that voted in favor of Trump or Hillary are colored in red or blue, respectively. Click on the image to download a high-resolution version._" highres="https://christian-johnson.github.io/election-neural-net/plots/National_vote_fraction.tiff?raw=true" %}


Once all the data is loaded into a nice format (which takes a bit of work- that's the purpose of the function [load_data.py](https://github.com/christian-johnson/election-neural-net/blob/master/load_data.py)), we can create a neural net using a Python class called [MLPRegressor](http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor) from the open-source package [Scikit-learn](http://scikit-learn.org/stable/index.html). This makes things very easy- the essential code is only a few lines:

{% highlight python %}
from sklearn.neural_network import MLPRegressor as mlp
nn = mlp(verbose=True)
nn.fit(training_inputs, training_outputs)
results = nn.predict(test_inputs)
{% endhighlight %}


Here I've broken up the data into two pieces: "training" and "test".
If I have a hunch that Florida's votes have been hacked, then the Florida counties are my "test" data, and the rest of the country is my "training" data.
Then we can compare the output of the neural net to the real data and look for discrepancies.
Of course, the proof is in the pudding- how well does it actually work?

## Results
The neural net turns out be pretty good- see, for example, the actual and predicted vote counts in Florida:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/election_data_model_FL.jpg" description="_Figure 2: Actual election results for Florida on the left, and the predicted results on the right. Click on the image to download a high-resolution version._" highres="https://christian-johnson.github.io/election-neural-net/plots/election_data_model_FL.tiff?raw=true" %}

On average, the neural net predicts a given county's vote to within 1-2% (it changes a little each time the neural net is trained due to how the minimization procedure works, so I run the fitting ten times and average the results).
Now we can look at deviations in the data from the prediction (i.e. the residuals), and see if any counties have a large excess of Trump votes.

In Figure 3 I've plotted the residuals when I run the neural net treating each state as my "test" data and stitched the results together.
It's important to note that Figure 3 shows only the residuals of _vote share_ - it isn't scaled by electoral vote impact.
Therefore the fluctuations you see can be tricky to interpret on their own, because random fluctuations in small-population counties can appear pronounced, but be negligible in terms of the actual impact.
What we might like is a measure of the _significance_ of a given deviation, in terms of significance on the Electoral College.
Estimating this uncertainty and interpreting the results in this context will be the subject of a future blog post.

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/national_residmap.jpg" description="_Figure 3: Deviations from the neural net model across the country. The colors are scaled such that a county that voted as expected is white, while counties that voted more than expected for Trump or Hillary are colored red and blue, respectively. As expected, counties in the West tend to exhibit stronger fluctuations due to their low population.  Click on the image to download a high-resolution version.__" highres="https://christian-johnson.github.io/election-neural-net/plots/national_residmap.tiff?raw=true" %}


I want to emphasize that the model here is not a _prediction_ in the common sense of (for instance) "predicting the future".
We already know what happened in the election!
What I'm doing is looking for _inconsistencies_ in the data, by assuming that any vote-meddling would have been confined to a handful of places.
The neural learns what "should have" happened in each county by looking at the trends in the counties that are out-of-state.
So it isn't surprising to see collective state-to-state differences in the residuals, because the counties in a given state were all treated as "test" data simultaneously. 

On the other hand, a large deviation in a given state is a sign that there might be something that wasn't taken into account.
For instance, Utah and northern Arizona voted signficantly less for Trump than was expected- I suspect this is because those areas have high Mormon populations.
You might also see Vermont and Arkansas are generally blue- my guess is this is because Bernie Sanders' endorsement of Hillary had a strong influence on his constituents in Vermont, and Hillary was viewed more favorably by some in Arkansas because of her time spent there as First Lady.
Likewise, the New York metropolitan area (at least outside of the city) voted more strongly for Trump than expected, which perhaps has something to do with the fact that he is a native of that area.

## What if vote machines weren't hacked, but voter registrations were?
So far, I've only looked at half the story- what if no votes were changed, but voter registrations were tampered with?
If enough people were prevented from voting in the right areas, that would be enough to change the results, while remaining invisible to the analysis presented above. 
To investigate this, I ran the neural net again, but this time I looked at voting turnout, which I calculated as the number of votes, divided by the number of people aged 18+.
This isn't a perfect definition because there are some groups (e.g. convicted felons) who might be unable to vote despite being over the age of 18- my guess is those groups make up a small fraction of the population.

The voting turnout nationwide looks like this:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/national_turnout.jpg" description="_Figure 4: Voter turnout. Turnout doesn't vary as much county-to-county as does political leaning, but there are still some trends that you can identify. Click on the image to download a high-resolution version._" highres="https://christian-johnson.github.io/election-neural-net/plots/national_turnout.tiff?raw=true" %}


Again, we can predict the turnout in the same state-by-state manner as we predicted the vote share, and the residuals are plotted below:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/turnout_residmap.jpg" description="_Figure 5: National voter turnout residuals. The color is scaled such that counties that had a lower turnout than expected are brown/orange, while higher-than-expected turnout is colored in purple (Not using the red-blue color scheme here because turnout doesn't necessarily correlate with political party). Click on the image to download a high-resolution version.__" highres="https://christian-johnson.github.io/election-neural-net/plots/turnout_residmap.tiff?raw=true" %}


The results show a couple things that make sense in hindsight- for starters, it appears that a lot of Mormons in Utah decided to sit the election out rather than vote for someone they didn't like. 
Swing states like Florida, North Carolina, Maine, and Colorado had unexpectedly high turnouts, while safe states like New York, Tennessee, and West Virginia had a bit less turnout than expected.

Importantly, it doesn't look to me like a pattern of interference, where we might have expected a couple of counties in Ohio or Florida to show up bright orange.
In fact, the county with the most significant deficit in voting turnout in Ohio is Holmes county, which turns out to have a very large Amish population (which I'm guessing doesn't vote as at high a rate as the non-Amish).
The biggest trends I see are more gradual, which probably reflects things that aren't taken into account when building the neural net.
If you'd like to add some data series or adjust the fitting procedure, the code is all on my GitHub (so go nuts!).
I'll keep playing around with this data and add blog posts whenever I find something interesting.
Until then, we know that if the Russians did alter the results of the election, they were at least somewhat subtle about it.

## TL;DR: [Betteridges Law of Headlines](https://en.wikipedia.org/wiki/Betteridge%27s_law_of_headlines)


## Appendix: Data series used
The data points used in training the neural net are (in no particular order):

1. Population density (people per square mile)

2. Percent of people who voted GOP in 2012

3. Percent Black, 2009

4. Percent Black, 2015

5. Percent White, 2009

6. Percent White, 2015

7. Percent Asian, 2009

8. Percent Asian, 2015

9. Percent Hispanic, 2009

10. Percent Hispanic, 2015

11. Percent Native American, 2009

12. Percent Native American, 2015

13. Percent of people on food stamps, 2013

14. Percent of people on food stamps, 2008

15. Average commute time, 2015

16. Unemployment rate, October 2016

17. Unemployment rate, October 2007

18. Percent of people with a Bachelor's degree, 2012

19. Median age, 2015

20. Median age, 2009

21. Percent of people who are rent-burdened, 2015

22. Homeownership rate, 2015

23. Income inequality index, 2015

24. Population 18+ in age

25. Fraction of 18+ people who voted in 2012

