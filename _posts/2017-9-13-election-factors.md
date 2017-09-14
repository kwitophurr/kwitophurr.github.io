---
layout: post
title: "Who Is Responsible For Trump?"
date: 2017-09-13
categories: jekyll update
---

It seems that these days everyone has their own theory to explain Donald Trump's rise.
That's not surprising, given that the US is an incredibly complex and diverse place and the fact that choosing who to vote for is a deeply personal decision.
But from what I've seen, most of these theories fall in one of two camps, which I'll call the __racial__ and __economic__ theories.

### The Contenders

The __economic__ theory says that Trump was pushed to victory by the white working class, especially in the Rust Belt. 
These were voters who have seen manufacturing jobs disappear and resented a political class that had generally pushed for globalization.
As the theory goes, they were drawn to Donald Trump because he represented a break from the old political establishment and would refocus Washington's attention on restoring jobs and prosperity to these voters. 
Trump, for his part, consistently expressed his dislike of international trade deals like NAFTA and the TPP.
This theory is certainly reasonable on its face- just take a look at the voting change from 2012 to 2016:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/GOP_vote_change.jpg" description="Figure 1: Change in the GOP vote share from 2012 to 2016. Note that the areas that most strongly turned towards Trump were concentrated mostly in the Midwest. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/GOP_vote_change.tiff?raw=true" %}

Trumps biggest support compared to Mitt Romney was clearly in the Rust Belt. 
Another way to look at this is to compare Trump's relative support versus Mitt Romney's to the change in population between 1980 and 2016:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/population_change_correlation.jpg" description="Figure 2: GOP vote share change between the 2012 and 2016 elections plotted against population growth between 1980 and 2016. Each dot is a single county, where the size of the dot corresponds to that county's 2016 population. The color of each dot is corresponds to the 2016 election results (red dots voted more for Trump, blue dots voted more for Clinton). There are some counties that are outside the viewing range here, but I restricted the range of the axes to make the trends easier to see. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/population_change_correlation.tiff?raw=true" %}

Although there is some noise in the data shown in Figure 2, the trend is clear: places that grew more slowly or declined in population since 1980 tended to vote more strongly for Trump than they did for Mitt Romney.

On the other hand, the __racial__ theory says broadly that it was Trump's explicit appeals to white voters who were resentful of the gains made by minority groups under President Obama that propelled him to victory.
This theory, while perhaps a bit harder to swallow, also has strong merit.
As Ta-Nehisi Coates points out in the excellent essay [The First White President](https://www.theatlantic.com/magazine/archive/2017/10/the-first-white-president-ta-nehisi-coates/537909/), Trump won the vote of whites at all income levels, not just the working-class.
It's also worth reading [White Riot](https://www.vox.com/2016/9/19/12933072/far-right-white-riot-trump-brexit) by Zack Beauchamp, where a number of studies supporting this theory are explained.
As we've seen in recent times (e.g. Charlottesville), racist whites are still a potent force in this country- perhaps strong enough to springboard one of their own to the presidency.

There is undoubtedly some truth to both theories- this is a large and diverse country and voters can certainly be motivated by different reasons.
The question I want to ask here is what the machine learning techniques I've described in my previous posts can tell us about which one of these theories was dominant in the 2016 election.

### Correlations

Let's start by looking at the simple [correlations](https://en.wikipedia.org/wiki/Correlation_and_dependence) between each demographic variable and the GOP vote share:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/GOP_Correlations.png" description="Figure 2: Table of most highly and negatively correlated demographic data to the GOP vote share in the 2016 election. Unfortunately Markdown doesn't have a nice table format as far as I can tell, so if you'd like to get all the values without copying them by hand from the image, I'm afraid you'll have to use the code on my GitHub. Click on the image to download." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/GOP_Correlations.png" %}

It should come as no surprise that the variable most strongly correlated with the outcome of the 2016 election is the results of the 2012 election (obviously the 2016 election is perfectly correlated with itself, hence the 1.000 in the first row on the left). 
Americans tend to view their political party much like their favorite sports team, and are often loath to change affiliation.
But looking past the first two rows, we see that the strongest predictor of Trump support is the fraction of white people. 
In fact, looking at all the positively correlated variables paints a picture of the quintessential Trump voter as older, affluent (note the positive homeownership rate correlation), religious, and white.

The negatively correlated variables reinforce this interpretation to some exent- the presence of Black population and Rent Burdened population on the list hint that a strong contingent of the Clinton coalition was poor and minority. 
The other component of the Clinton vote (judging by the presence of the percentage of Bachelor's degree recipients and the level of belief in human-caused climate change) appears to be those who are highly educated.

Of course, correlation [does not always imply](https://www.xkcd.com/552/) causation.
It might be tempting to look at this data and claim that the __racial__ theory of Trump's rise is correct, but the fact that you can predict the Trump vote to a ~93% extent just by looking at Mitt Romney's performance means that we are probably missing the factors that are unique to Trump himself.
Let's repeat this exercise, but look at the correlations between the demographics and the *change* in the GOP vote (i.e. Figure 1 above):

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/GOP_Change_correlations.png" description="Figure 3: Table of most highly and negatively correlated demographic data to the GOP vote change between the 2012 and 2016 elections. Many of the most strongly correlated parameters are the same as in Figure 2, but there are a few differences. Click on the image to download." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/GOP_Change_correlations.png" %}

Alright, so in this case it looks like correlation does imply causation. 
We see that Trump's support (normalized to Mitt Romney's) is still heavily predicted by the white vote, especially the older, affluent, religious white vote.
In other words, Trump didnt necessarily grow the Republican party so much as he consolidated its grip on folks who generally lean Republican anyways.

The slightly more interesting effects are on the opposite end of the spectrum- what was it about Trump that made voters shy away from him?
I see a couple of things here: Trump managed to offend Mormons (as we've seen before) and Hispanics (with his outright racism and xenophobia).
We again see both poor and educated people gravitated towards Clinton, but we interestingly median income is also negatively correlated with Trump's relative performance.

Looking at this data so far, I would attribute the lion's share of Trump's support to the __racial__ as opposed to the __economic__ theory. 
But let's keep digging and see what the machine learning models have to say on the topic.


### All else being equal...

For this part of the analysis, I generated a completely average US county in every aspect by simply taking the mean of each data series I had, weighted by the 2016 population.
This is perhaps a bit artificial because no county actually looks like this one, but it's at least a good starting point.

Next, I kept all the parameters (except for the one under study) constant, while varying the variable I was interested in from the minimum value across the country to the maximum. 
I trained an elastic linear regressor (for speed) on the entire country's data, and then used the trained model to predict the outcome of the election for the artificial counties I had generated.
This lets us look at the effect of each variable in isolation.
The results are striking:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/avg_county_variations_linear.jpg" description="Figure 5: Keeping everything else constant, how does changing a single variable impact the predicted vote? The racial indicators (percentage of black & white people) have a much stronger impact than the economic ones (unemployment rate, food stamps, income).  Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/avg_county_variations_linear.tiff?raw=true" %}

Varying the percentage of white people changed the predicted vote by about 8%, and varying the percentage of black people changed it by around 5%.
Compare that with each of the economic indicators I looked at, which each have around 1-2% impact.

Next, I turned to ensemble of a linear regressor, a neural net, and a random forest regressor to do the same analysis (as we saw in my previous post, the ensemble can outperform any individual algorithm).
The results are similar, although a bit less dramatic:

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/avg_county_variations_ensemble.jpg" description="Figure 6: Just like Figure 5, but using an ensemble of machine learning techniques. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-9-13-election-factors/avg_county_variations_ensemble.tiff?raw=true" %}

In this instance, it looks like the black population has an even stronger effect than the white population, though both still exceed the effects of the economic parameters.

### Conclusions

As I said before, there is merit to both theories of Trump's rise.
However, the data clearly indicates that the strongest predictors of how a county will end up voting are the percentages of different races in that county.
There's more work to do in this area (so stay tuned), but I think that at least to zeroth order, the __racial__ theory is the best one we've got at the moment.