---
layout: post
title: "Were Votes in the 2016 Election Hacked?"
date: 2017-06-01
categories: jekyll update
---

I have long subscribed to the belief that the worst thing about Donald Trump isn't Donald Trump- it's that he has so many supporters.
Despite my shock at the outcome of the 2016 election, I accepted the fact that these voters made a conscious choice (however wrongheaded) when voting, regardless of whether or not they were influenced by a Russian propaganda machine.
However, a handful of recent revelations imply that the Russians didn't just attempt to influence voters, but to manipulate voter registrations or even alter votes after they were cast.
Is it possible that America voted against Trump, but the election was stolen?

My interest in this subject was piqued on June 6, when NSA contractor [Reality Winner](https://www.theatlantic.com/news/archive/2017/06/who-is-reality-winner/529266/) was arrested on suspicion of leaking a top-secret document to The Intercept.
The document [alleges](https://theintercept.com/2017/06/05/top-secret-nsa-report-details-russian-hacking-effort-days-before-2016-election/) that Russia attempted to spear-phish up to 100 local election officials in up to seven states, with the intention of gaining access to their computer systems.
A week later, [Bloomberg](https://www.bloomberg.com/news/articles/2017-06-13/russian-breach-of-39-states-threatens-future-u-s-elections) reported that Russian hackers had attacked electronic voting infrastructure in up to 39 states.
Suspicion that Russia had gained access to our voting systems was given confirmation with the [announcement](http://time.com/4828306/russian-hacking-election-widespread-private-data/) that voting systems in Illinois had been compromised to at least a partial extent.

I wondered whether it is possible to detect voting interference without having direct access to the voting machines or computer systems themselves. To find out, I started by putting ourselves in the mindset of Vladimir Putin, and thought about how I would have done it.
## So you want to hack an election
I'm going to make one big assumption here- I will assume that the vote-hacking would have been confined to only a handful of places within swing states.
After all, it doesn't make much sense to try to swing (for example) California for Trump- millions of votes would have to be changed and people would surely notice.
Moreover, your risk of getting caught by an astute observer increases as you expand your number of targets.
If I were Putin and wanted to hack election machines, I would have focused my efforts on states like Florida, North Carolina, Ohio, and Pennsylvania, which were the most prominent swing states this election. 

Within each state, I would still have wanted to only target a handful of places (to minimize risk of detection)- specifically the big population centers.
That's because within a state, the only thing that matters is the popular vote- so you'll get the best bang for your buck by hitting the most populous places. 
In addition, focused hacking in a big county is harder to detect: a few tens of thousands of votes changed one way or another might go unnoticed in Charlotte, but would be highly conspicuous in a small county. 
And a few tens of thousands of votes could be all you need to swing a state one way or another.

Of course, this assumption could be wrong- perhaps Putin was more brazen than I'm guessing and he decided to swing for the fences (as the Bloomberg report suggests) and attack election systems nationwide.
Or maybe his goal wasn't actually to swing the election one way or another, but simply to cause mass distrust of our democratic systems (in which case, the very existence of this blog post shows that he may have succeeded).
So it's entirely possible he wouldn't have localized his vote tampering to a handful of places, and it would be more difficult (if not impossible) to detect in the way I'll describe here.

Fortunately, it turns out that we can still learn some interesting things from the analysis I'll present here whether my assumption is true or false.

To recap: I'm making an educated guess that the places most likely to be a target for vote tampering are the handful of counties that contain large-ish cities, in swing states.
But the question still remains- how would we know if the votes counts in those counties are valid or not?
What we need is an accurate, county-by-county prediction of how each county is likely to vote, which can then be compared to the actual voting results.
To do this, I turned to machine learning.

## Number crunching with neural nets
Machine learning has been in the news a lot recently, with people buzzing about what so-called "deep learning" can do in fields like image classification and voice recognition (take, for example, the recent [Apple WWDC keynote](https://techpinions.com/the-overlooked-surprises-of-apples-wwdc-keynote/50282)).
But for this analysis I don't need anything particularly fancy; a good old-fashioned neural net will do just fine (if you're new to machine learning, I recommend this [YouTube video](https://www.youtube.com/watch?v=bxe2T-V8XRs) to explain the basics of how a neural net works).
For the inputs I provided it with publicly-available demographic information- things like median income, population density, and voting results from years past.
To train it, I just used the actual results of the election (Figure 1, below).

In the US, elections are generally administered by the county (or county equivalent)- so that's as granular as I decided to get.
I began by downloading a bunch of demographic data from the St. Louis Federal Reserve [website](http://geofred.stlouisfed.org/map/), which has a nice interface for getting exactly this kind of county-level data.
Data on religious affiliation was a bit more difficult to find- the best resource I found was the [Association of Religious Data Archives](http://www.thearda.com/Archive/Files/Descriptions/RCMSCY10.asp) which I downloaded as a Stata file.
Finding county-level election results was also tricky, but luckily GitHub user [tonmcg](https://github.com/tonmcg/County_Level_Election_Results_12-16) had already compiled the data into a nice spreadsheet.
All of the data that I used are available on the [GitHub page](http://github.com/christian-johnson/election-neural-net) for this project, under the folder [data_spreadsheets](https://github.com/christian-johnson/election-neural-net/tree/master/data_spreadsheets).

A couple of quick notes about the data:

1. There are 36 different data points on each county- the exact data points I used are listed at the end of this post. 

2. As best I could tell, only precinct-level (not county-level) voting returns are available for Alaska, so I applied the analysis only to the other 49 states. 

3. For a handful of counties in South Dakota (Perkins, Roberts, Pennington, and Sanborn), the data from the Federal Reserve seems to have wild inconsistencies between 2009 and 2010, with each experiencing dramatic jumps in population. Since this seems to be a problem with the data and not the analysis, I excluded these counties by hand. I contacted the Federal Reserve, and have been informed that they are looking into the issue.

4. Polk County, TX had incorrect results in tonmcg's data- I replaced it with the data from the [Texas Secretary of State's data](http://elections.sos.state.tx.us/elchist319_race62.htm) instead. The rest of the results in Texas were consistent between the data sets to within a few votes.

5. When running the neural net, I also excluded counties that are missing data points for one reason or another. This affects another handful of counties, but hopefully doesn't have too big an impact on the final results.

6. Election results are somewhat complicated due to the presence of third-party candidates. I ignored third parties, so vote fractions were calculated as percentage of the two main vote shares. For example, the vote margin in Figure 1 below is found by: (GOP-DEM)/(GOP+DEM). Turnout was calculated as (GOP+DEM)/(Eligible Voters).


{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/National_vote_fraction.jpg" description="Figure 1: 2016 US Presidential Election Results. The colors in the image are scaled such that a county that voted 50-50 would appear white, while counties that voted in favor of Trump or Hillary are colored in red or blue, respectively. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/National_vote_fraction.tiff?raw=true" %}

Once all the data is loaded and formatted properly (made easy by the use of Pandas), I created a neural net using Google's TensorFlow framework.
I found TensorFlow to be a bit more complicated than something like Scikit-learn, but also a bit more customizable.
The neural net I used had 3 fully-connected hidden layers of 100 neurons, and I used tf.train.AdamOptimizer when training- this combination seemed to give reasonable results but I'm not a machine learning expert so there may be better choices available.
With the same parameters and data, I found similar results using both TensorFlow and Scikit-learn. 

The usual paradigm in a machine-learning problem is to "train" your neural net on a particular set of data, and then use it to make predictions about a new set of data (the "test" set).
Naively, then, you might think that we should use the 2012 election results as the "training" data and the 2016 results as the "test" data.
Unfortunately this is not a good idea for the simple reason that the candidates in the 2016 election were very different from those in 2012- doing this will probably lead to crummy predictions.
To give a concrete example of this- Mitt Romney was Mormon and had high support among Mormon voters, whereas Donald Trump spectacularly underperformed with Mormons.

Instead, the method I employed for this analysis was in analogy with a "bump hunt" in particle physics- I treated the 2016 results in each state as a separate "test" set, and then stitched the results together at the end.
This is a bit less kosher because there's not a perfect distinction between "test" and "training" data, but since we can't hold a do-over election it's pretty much the best that can be done.
Of course, the proof is in the pudding- how well does the neural net actually work?

## Results
The results turns out be pretty accurate- see, for example, the actual and predicted vote counts in Florida:


{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/FL_data_model.jpg" description="Figure 2: Actual election results for Florida on the left, and the predicted results on the right. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/FL_data_model.tiff?raw=true" %}


On average, the RMS of the difference in the predicted vs actual data is about 2% (it changes a little each time the neural net is trained due to the stochastic nature of the minimization procedure).

The residuals over the entire country (minus Alaska and problematic counties) are displayed in Figure 3.
I want to emphasize again that the model here is not a _prediction_ in the common sense of (for instance) "predicting the future".
We already know what happened in the election!
What I'm doing is looking for _inconsistencies_ in the data, by assuming that any vote-meddling would have been confined to a handful of places.
You can think about the colored areas in Figure 3 as places where Clinton and Trump outperformed their expectation given the results in the rest of the country.

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/vote_residmap.jpg" description="Figure 3: Deviations from the neural net model across the country. The colors are scaled such that a county that voted as expected is white, while counties that voted more than expected for Trump or Hillary are colored red and blue, respectively. As expected, counties in the West tend to exhibit stronger fluctuations due to their low population. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/vote_residmap.tiff?raw=true" %}


It isn't surprising to see collective state-to-state differences in the residuals, because the counties in a given state were all treated as "test" data simultaneously. 
On the other hand, a large deviation in a given state is a sign that there might be something that wasn't taken into account.
For instance, Arkansas is completely blue- my guess is this is because Clinton's time spent there as First Lady meant she was viewed more favorably than in similar states.
Likewise, the New York metropolitan area (at least outside of the city) voted more strongly for Trump than expected, which perhaps has something to do with the fact that he is a native and resident of that area.

Speculation aside, Figure 3 doesn't look to me like the signature of hacked votes.
In fact, the swing states were predicted reasonably accurately, and there isn't an obvious pattern of high-population counties voting more strongly for Trump than expected.
This becomes more clear when looking at the pattern of residuals versus vote share in Figure 4:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/residual_vs_vote.jpg" description="Figure 4: Residuals from the neural net prediction versus the vote share. Each circle represents a single county, and the size of the circle represents the population. If vote-hacking had taken place, my hypothesis is that there would be several large red circles in the upper left of the plot that would correspond to urban areas of swing states. The data shows a farirly smooth distribution with no clear signs of vote-hacking. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/residual_vs_vote.tiff?raw=true" %}

The hypothesis I made earlier (that vote hacking would have taken place mostly in large counties) means we would expect there to be several large counties in the upper left corner of the plot.
As it is, the distribution of counties looks pretty much Gaussian to my eye. 
The biggest outliers (the four medium-sized counties at around +7-11% residual and 40-60% GOP vote share) are all in New York or New Jersey, which is consistent with what we see in Figure 3.

## What would vote-hacking look like?
Although I don't see any obvious signs of wrongdoing, it isn't immediately obvious that this technique is actually sensitive enough to detect manipulated votes.
To check whether or not vote-hacking would be easy to spot, I added 10,000 votes for Trump to three counties: Miami-Dade in Florida, Wayne in Michigan, and Cuyahoga in Ohio (which contain the cities Miami, Detroit, and Cleveland respectively).
I re-ran the analysis on this new, altered data set, and the residuals are shown in Figure 5 below:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/injected_vote_residmap.jpg" description="Figure 5: The same analysis as Figure 3, except with 10,000 added votes in Miami, Detroit, and Cleveland. Miami is a clear outlier, while Cleveland and Detroit are less obvious. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/injected_vote_residmap.tiff?raw=true" %}

The results are interesting- Miami clearly shows up as an outlier but Detroit and Cleveland (although red) are not highlighted the same way.
I suspect that training the neural net again would give slightly different results that might highlight these counties better or worse- but the point is that the neural net is at least moderately sensitive to vote-hacking.
It is much more sensitive, for instance, than using the change from 2012 as the model:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/injected_vote_change.jpg" description="Figure 6: The same analysis as Figure 5, except using the votes from 2012 as the model, instead of the neural net prediction. The extra 10,000 votes in three counties are peanuts compared with the large changes that are present across the entire map. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/injected_vote_change.tiff?raw=true" %}

Conclusion: using a neural net to look for vote-hacking isn't perfect, but it's not terrible either.

## What if vote machines weren't hacked, but voter registrations were?
So far, I've only looked at half the story- what if no votes were changed, but voter registrations were tampered with?
If enough people were prevented from voting in the right areas, that would be enough to change the results, while remaining invisible to the analysis presented above. 
I ran the neural net again, but this time looking at voting turnout, which was calculated as the number of votes divided by the number of people aged 18+.
This isn't a perfect definition because there are some groups (e.g. convicted felons) who might be unable to vote despite being over the age of 18- my guess is those groups make up a small fraction of the population.

The voting turnout nationwide looks like this:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/national_turnout.jpg" description="Figure 7: Voter turnout. Turnout doesn't vary as much county-to-county as political leaning, but there are still some trends that you can identify. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/national_turnout.tiff?raw=true" %}


Again, we can predict the turnout in the same state-by-state manner as we predicted the vote share, and the residuals are plotted below:


{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/turnout_residmap.jpg" description="Figure 8: National voter turnout residuals. The color is scaled such that counties that had a lower turnout than expected are brown/orange, while higher-than-expected turnout is colored in purple (I'm not using the red-blue color scheme here because turnout doesn't necessarily correlate with political party). Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/turnout_residmap.tiff?raw=true" %}

Again, this doesn't look to me like a pattern of interference, where we might have expected a couple of counties in Ohio or Florida to show up bright orange.
There are a handful of outlier counties, but they aren't located in swing states (which in general are predicted pretty well).

If you'd like to edit the data series used or adjust the fitting procedure, the code is all on my GitHub (so go nuts!).
I'm going to keep playing around with this data and add blog posts whenever I find something interesting.
Until then, we know that if the Russians did alter the results of the election, they were at least somewhat subtle about it.

## TL;DR: [Betteridges Law of Headlines](https://en.wikipedia.org/wiki/Betteridge%27s_law_of_headlines)


## Appendix: Data series used
The data points used in training the neural net are (in no particular order):
1. Vote results from 2012
2. Voting Turnout in 2012
3. Population, 2016
4. Population, 2009
5. Percent White, 2015
6. Percent Black, 2015
7. Percent Hispanic, 2015
8. Percent Asian, 2015
9. Percent Indian, 2015
10. Percent Age 0-18, 2015
11. Percent White, 2009
12. Percent Black, 2009
13. Percent Hispanic, 2009
14. Percent Asian, 2009
15. Percent Indian, 2009
16. Percent Age 0-18, 2009
17. Unemployment Rate, 2016
18. Unemployment Rate, 2007
19. Unemployment Rate, 2004
20. MedianAge',
21. Percent with Bachelors Degrees
22. Commute Time
23. Number of People on Food Stamps
24. Homeownership Rate
25. Income Inequality Index
26. Businesses per Person, 2016
27. Businesses per Person, 2009
28. Percent Rent Burdened, 2015
29. Percent Rent Burdened, 2010
30. Percent Evangelical Protestant
31. Percent Mainline Protestant
32. Percent Black Protestant
33. Percent Catholic
34. Percent Jewish
35. Percent Muslim
26. Percent Mormon
