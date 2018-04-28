---
layout: post
title: "How Much Did Voter Suppression Affect the 2016 Election?"
date: 2018-04-25
categories: jekyll update
---
As has been documented time and again, in-person voter fraud is a virtually nonexistent problem in American elections (I've even covered the [implausibility](https://christian-johnson.github.io/alabama) previously on this blog).
But unlike scientists, our elected officials have rarely felt the need to consult such mundane sources as evidence when making decisions.


The open secret, of course, is that voter ID laws are designed to suppress turnout among the voter base- especially poor and minority voters who may not have the necessary IDs.
America has a long and illustrious history of voter suppression efforts (particularly with regards to minorities), of which our modern voter ID laws are but the current incarnation.
The question I want to ask here is whether or not those voter ID laws had any appreciable impact on the outcome of the 2016 election.

A Democratic Super PAC, Priorities USA, put forth a [study](https://www.scribd.com/document/347821649/Priorities-USA-Voter-Suppression-Memo) which looked at this particular issue, and concluded that voter ID laws in Wisconsin
prevented somewhere around 200,000 people from voting- in a state which Donald Trump won by only around 20,000 votes.
That's a rather alarming result, especially with the added fact that Priorities USA concludes that the suppressed voters were disproportionally Democratic.

However, let's remember that Priorities USA is not an unbiased source- and if you take a look at their analysis you might find, as I did, that it is not particularly scientific.
Let's dig a little deeper and see if we get the same result.

### What was turnout like in 2016, anyways?
Let's start by looking at a map of the change in turnout (which I've defined as votes for either the Democratic or Republican candidate, divided by the total population over the age of 18) between 2012 and 2016:

{% include image.html url="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/turnoutChange.jpg" description="Figure 1: Vote turnout change between 2012 and 2016. Stretches of Appalachia voted at a significantly higher rate than in 2012, while much of Utah and the Midwest voted at lower rates. Click to download the image." highres="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/turnoutChange.tiff" %}

As I mentioned before, voter suppression efforts typically are laced with racism against black people in particular- is there any correlation between the turnout change and race?

{% include image.html url="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/turnoutchange_race.jpg" description="Figure 2: Turnout change compared to percentage of the population which is black. Each bubble is a US county, and the size of the bubble corresponds to the population of the county. Bubble color corresponds to the 2016 presidential election vote (red = Republican, blue = Democrat, white = neutral). Counties with a high proportion of black people (on the far right in this plot) clearly had turnout that was a few percentage points lower than in 2012. The X-axis is log-scaled so that all the bubbles don't overlap each other. Click to download the image." highres="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/turnoutchange_race.tiff" %}

The answer is yes: the distribution in Figure 2 above has a definite tail on the right-hand side which dips below zero.
That means that counties with a high proportion of black people had, in general, lower turnout for the 2016 election than in the 2012 election.

Perhaps you could have predicted that, though- after all, Barack Obama was incredibly popular among the black population (after all, [he was black](https://www.theatlantic.com/magazine/archive/2017/01/my-president-was-black/508793/) himself).
Maybe the tail in Figure 2 was just related to the fact that the 2016 election pitted two [very](https://www.youtube.com/watch?v=ppgk9Mj1n88]) [white](https://www.theatlantic.com/magazine/archive/2017/10/the-first-white-president-ta-nehisi-coates/537909/) people against each other.

What we really need is a [control](https://en.wikipedia.org/wiki/Scientific_control)- a way to compare turnouts where the only variable that changes is the presence or absence of voter ID laws.
As in previous posts, we'll turn to machine learning to get a proxy for a control.

### Looking more closely
As it turns out, only three states - Wisconsin, Virginia, and Mississippi- had strict voter ID laws come into effect between the 2012 and 2016 elections.
Three more - Georgia, Indiana, and Tennessee- had voter ID laws on the books before the 2012 election.
So let's take a look at just those six: they'll be our 'test' data.
(As it turns out, looking only at Wisconsin, Virginia, and Mississippi had little impact on the results, so I'm going to show the most complete dataset.
The code is of course available on GitHub if you want to see for yourself.)

The strategy here, just to remind you, is to train a fitting algorithm to predict the vote turnout by looking for patterns in about 50 demographic variables in each county outside our 'test' set.
Then we can compare the predicted turnout to the actual turnout and look for anomalies.
The plots below show the results when the algorithm is a simple linear regression, but I also tried a neural net and a random forest regressor, which gave very similar results.

{% include image.html url="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/wiscoResiduals.jpg" description="Figure 3: Turnout residuals in the six states that had strict voter ID laws in effect in 2016. Here, the gray counties are not missing data but rather the data used for training. Of the six states under consideration, two (Wisconsin and Virginia) had higher turnout than predicted, while the other four had lower turnout. Click to download the image." highres="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/wiscoResiduals.tiff" %}

The results in Figure 3 are very interesting: Wisconsin and Virginia actually had *more* turnout in 2016 than expected!
The other states had suppressed turnout, especially in Tennessee.

If I were to speculate, I would guess that the swing state status of Wisconsin and Virginia had far more impact on the turnout than voter ID laws.
This makes intuitive sense to me: my gut tells me that far more people fail to vote out of either laziness or cynicism with the political process than because they couldn't navigate the bureaucracy.
And in swing states, where each person's vote carries more weight, folks are surely going to be more motivated to head to the polls.

Of course, in non-swing states, it really does look like the voter ID laws suppress the vote a bit.
I was curious if the lower turnout disproportionally affected minorities, so I made the following bubble plot:

{% include image.html url="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/turnoutresiduals_race.jpg" description="Figure 4: Turnout residuals compared to black population in the six satates with voter ID laws. If you squint, there's a similar tail on the right-hand side of the plot where black votes may have been suppressed. However, it's a lot less pronounced than in Figure 2. Click to download the image." highres="https://raw.githubusercontent.com/christian-johnson/election-neural-net/master/plots/2018-4-25-voter-suppression/turnoutresiduals_race.tiff" %}

It is interesting that all of the heavily populated majority-black counties in these six states had lower-than-expected turnout.
Does that mean that if voter ID laws hadn't been on the books, the results of the election would have been different?

### What if voter ID laws weren't in effect?
The final piece of the analysis I did was to "correct" the turnout in each county to what the linear regression predicted it would have been in the absence of voter ID laws, and re-tabulate the vote.
That gives us a handle on whether or not the voter ID laws had any measurable impact on which states were won or lost in the 2016 election.

The result: in every case, the final vote changes by less than 0.25%.
In Wisconsin, where I "corrected" the turnout by reducing the number of votes, the Republican margin of victory increased from 0.41% to 0.74%.
In Tennessee, where the number of votes was artificially increased, the Republican margin of victory decreased from 3.64% to 3.57%.

These are not big changes.
And that makes sense- voter ID laws are a hindrance to anyone who votes, and affect almost as many Republicans as Democrats.

### Conclusions
My take on all the data is that voter ID laws have a nonzero but still very small impact on the results of an election.
Far more important, I would argue, is the fact that the typical voter turnout is only around 50% to begin with!
Democrats should not view the repeal of voter ID laws as a panacea for victory, nor should Republicans view these laws as necessary for them to win.
We shouldn't waste our time and energy debating and enforcing voter ID laws.
Instead, let's just make it easier for everyone, Republicans and Democrats alike, to vote- let's make Election Day a national holiday, or move it to the weekend.
Isn't strong civic participation the cornerstone of our democracy anyway?
