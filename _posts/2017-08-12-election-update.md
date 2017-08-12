---
layout: post
title: "Vote Hacking 2: Electric Boogaloo"
date: 2017-08-12
categories: jekyll update
---
I wanted to give a quick update to my [first post]({{ % site.baseurl %}}/Election-Neural-Net), where I analyzed the 2016 Presidential election results with machine learning.
I've been reading my way through [Hands On Machine Learning with Scikit-learn and Tensorflow](https://www.amazon.com/gp/product/1491962291/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) in order to understand machine learning techniques better, and I've applied some of the things I've learned to my analysis of the election. 

### 1. Better Plots
Not really a big change, but I changed my plotting code to use a [Lambert-Conformal](https://en.wikipedia.org/wiki/Lambert_conformal_conic_projection) projection instead of the [Miller](https://en.wikipedia.org/wiki/Miller_cylindrical_projection) projection I had been using.
Every map projection has its own advantages and drawbacks, but I think the new plots are a bit more aesthetically pleasing.
Check out the figures below to see what I mean.

### 2. More Data
Machine learning thrives when it has lots of numbers to crunch, so I added several more data series to my repository:

__Agricultural Data__

Data on the amount of land used to plant various crops is available from the [USDA](https://quickstats.nass.usda.gov/).
I calculated the fraction of a county's land that is devoted to growing four major crops: corn, soybeans, cotton, and winter wheat. 
The sum total area of these crops is shown in Figure 1 below:
{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/crops_planted.jpg" description="Figure 1: Fraction of land area devoted to growing corn, cotton, soybeans, and winter wheat. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/crops_planted.tiff?raw=true" %}

__Climate Change Beliefs__

Thanks to the [Yale Program on Climate Change Communication](http://climatecommunication.yale.edu/visualizations-data/ycom-us-2016/), I was able to get the responses to survey questions regarding beliefs on climate change.
From this data set, I only used the response to the question "Do humans contribute to climate change?"- there are a number of survey questions available but this particular question seemed like a reasonable metric to look at.
A map of the responses is shown in Figure 2:
{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/climate_change.jpg" description="Figure 2: Fraction of people who responded 'yes' to the question: 'Assuming global warming is happening, do you think it is caused mostly by human activities?'. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/climate_change.tiff?raw=true" %}

__Combined Attributes__

In place of the raw numbers, I calculated the changes in demographic and economic indicators (e.g. instead of feeding in the unemployment rate in 2007 and 2016 separately, I feed in the 2016 unemployment rate and the change from 2007).
This was done for 11 different variables- you can check the [GitHub repository](https://github.com/christian-johnson) if you'd like to see the details.
Observe, for instance, the change in unemployment rate from 2007 to 2016 in Figure 3:
{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/unemployment_change2007_2016.jpg" description="Figure 3: Change, in percentage points, between the unemployment rate in 2007 and 2016. Green indicates that unemployment rates are lower, while red indicates that unemploymet rates increased. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/unemployment_change2007_2016.tiff?raw=true" %}

### 3. New Techniques
In addition to a neural network, I analyzed the data with two other algorithms: an elastic linear regressor and a [Random Forest](https://en.wikipedia.org/wiki/Random_forest).
Each method yielded similar results (RMS of around 2.3%-2.5% for the entire country).
However, something I learned from my book is that an ensemble of methods often yields better accuracy than any individual method.
By taking the mean result from each of the three techniques, I found the overall RMS was slightly improved, to 2.19%.

{% include image.html url="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/vote_residmap_ensemble.jpg" description="Figure 4: Updated vote residuals, using the mean of an ensemble of machine learning algorithms. Click on the image to download a high-resolution version." highres="https://christian-johnson.github.io/election-neural-net/plots/2017-08-11-election-update/vote_residmap_ensemble.tiff?raw=true" %}

### 4. Randomizing Test Sets

In general, machine learning experts suggest a very strict boundary be made between training data and test data.
The reason for this is to prevent yourself from "data snooping", i.e. peeking ahead at the test data.
Snooping raises the risk of fine-tuning the parameters in your model so much that the model does not generalize to new instances (in other words, overfitting the data).
However, the technique I used previously does not separate data in this way- instead the algorithm worked by:
1. Looping through each state (minus Alaska)
2. For each state, remove its counties from the data set and train the computer on the remaining states
3. Apply the trained algorithm to the removed state
4. Concatenate the results of each state together to produce a complete map

The good news is that this idea is just a variation on a well-established practice with a fancy name: __cross-validatation__, and it is usually employed not to detect outliers (as I'm trying to do), but to determine when data has been overfit.

The hallmark of overfit data is that the error of the entire training set is significantly lower than the cross-validation error.
In my case, the RMS when trained on the entire data set (for a linear model) was 2.35%, and the RMS of the cross-validation set was 2.6%. 

This indicated a bit of overfitting, so I made a small but significant change to the way the cross-validation was done: instead of separating the counties by state, I separated them into random groupings.

This especially improves the performance in places like Utah, because the Mormon population is highly clustered together.
If all of Utah is removed from training, the model doesn't know how to treat highly Mormon counties and it gives poor results.
But splitting up the country randomly ensures that every feature has at least some representation in the training set, so predictions are a bit more reasonable.

Making this change meant that the cross-validation error was improved to 2.42% (for a linear model), which pretty close to the overall training set error of 2.35%.

With the results from improved model (Figure 4 above), I still don't believe there's any evidence that votes were hacked in the 2016 election.
