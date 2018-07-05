---
layout: post
title: "What was the Cuban sonic weapon?"
date: 2017-11-06
categories: jekyll update
---

Today's blog post will be a bit different than previous ones- I'm not going to discuss the election (won't that be a nice break!).
Instead, I want to take a look at the curious case of the [Cuban sonic attacks](https://en.wikipedia.org/wiki/Suspected_Cuban_sonic_attack).
Right off the bat, I want to make it clear that what I'm going to propose here is *pure speculation*- I do not know what happened during these attacks, or why they occurred.
But after listening to the [recording](https://www.youtube.com/watch?v=rgbnZG85IRo) that was released in early October by the AP, I do have a hypothesis about what might have happened.

### Sonic Attack?

Before we get into my hypothesis, let's remind ourselves of [what we know](https://www.nbcnews.com/politics/national-security/cuba-mystery-what-theories-u-s-investigators-are-pursuing-n802286) about the sonic attacks:
* A few dozen people reported a variety of symptoms, including nausea, headaches, hearing loss, and difficulty concentrating.
* Some people heard things only in certain areas of a room, while others didn't hear anything.
* Speculation (at least in the article linked above) has focused on either infrasound or ultrasound sources, but nobody has seen any devices to generate them.
* The frequency spectrum of the recording (seen in the YouTube video of the recording) shows a number of distinct peaks below 10 kHz that are regularly spaced.

All in all, a very weird situation.
Some have even speculated that nothing nefarious at all is happening, and the victims are simply suffering from "[mass hysteria](https://www.theguardian.com/world/2017/oct/12/cuba-mass-hysteria-sonic-attacks-neurologists)."
But that's a fairly boring diagnosis, so let's assume that the attacks are real, and they are some sort of sonic weapon.
That's much more exciting if you ask me!

### An Ultrasonic Weapon

My hypothesis is that the sound heard by the victims was created via *multiple ultrasonic* directed speakers that played evenly spaced frequencies.
From the spectrum in the video, it appears that there are 16 peaks between about 5 kHz and 8 kHz, with roughly 200 Hz separation between peaks.
I propose that these are actually the [beat frequencies](https://en.wikipedia.org/wiki/Beat_frequency) between the speakers (which are operating at around, say 100 kHz).
The human ear cannot hear anything above about 20 kHz, so the speakers themselves wouldn't make any appreciable sound.
But where they interfere, constructive and destructive interference of the sound waves would produce lower-pitched frequencies that would be able to be heard.

These lower-pitched frequencies are still fairly high-pitched (which might be why some people have trouble hearing them).
Because they result from interference patterns which may be rather complex, the relative loudness can vary dramatically across even a few meters (explaining why the sound can only be heard in parts of certain rooms).

As for the medical effects, my (completely wild) guess is that these frequencies may interfere with the sleep of the victims- the sound is vaguely reminiscent of a mosquito whine and there's really nothing worse when you're trying to sleep than a mosquito in your ear.
I'm of course a physicist not a doctor, but I don't think it's outside the realm of possibility that disrupted sleep over a time period of several weeks could lead to some dramatic symptoms.

So why go to all the trouble of building directed, ultrasonic speakers, instead of just playing really loud music near the targets and keeping them awake?
Two reasons:
1. The attack would be difficult to trace by a human ear- the interference pattern doesn't appear to originate from any particular direction because it is essentially a bunch of standing waves.
2. The effect is localized- depending on how tightly focused your speaker is, you could conceivably make the sound loud in just a single area, with intervening people none the wiser.

### Simulations

With this hypothesis in mind, I set out (with the help of a few friends) to write some code to simulate this type of attack.
I won't describe here all the intricacies of the simulation (it's not that complicated- download it yourself from my [GitHub](https:/www.github.com/christian-johnson/cuba-sonic-weapon/) if you want to know the nitty-gritty details).
I did make a handful of important assumptions, so you should definitely take the results with a grain of salt:

* The sound from the speakers in the simulation is collimated in a 2D Gaussian profile such that 95% of the sound stays within a cone about 40 degrees wide.
I have no idea whether Cuba has the ability to make such a device, or whether it's even physically possible to build one.

* There's no environment simulated- in real life there would be houses and trees in the way which might weaken the beams, or change how they interfere.

* I'm not actually sure of the details of how the ear responds to high-frequency sounds, so I made a completely wild guess and integrated the square of raw signal on a time scale corresponding to 20 kHz, which is about the upper range of human hearing.
This seemed to give reasonable results in line with what my expectations were- as one of my undergraduate professors told me, "Never do a physics problem unless you already know its answer."

The end result is this:
{% include image.html url="https://raw.githubusercontent.com/christian-johnson/cuba-sonic-weapon/master/loudness.png" description="Figure 1: Two maps of the same area showing how much energy is contained in the sound emitted by five speakers. The five speakers are arranged around a semicircle with radius 100 meters, and are aimed at the center. Each speaker emits a different frequency near 100 kHz. The left image shows the total energy in sound waves over all frequencies, while the right image shows only the energy of sound below 20 kHz. As you can see, the energy of the sound travels 'invisibly' to the target and is localized to a region around 35 x 35 meters in size. Click to download the image." highres="https://raw.githubusercontent.com/christian-johnson/cuba-sonic-weapon/master/loudness.png" %}

The sound produced by this weapon at the center of the image can be heard by downloading [this WAV file](https://github.com/christian-johnson/cuba-sonic-weapon/blob/master/output.wav?raw=true) (a 5 second sample). *Edit: if you like, you can also view [this YouTube video](https://www.youtube.com/watch?v=b8ivvVteT6Y) which plays the sound.*
Fair warning- it is not a particularly pleasant sound (this is supposed to be a sonic weapon after all) so make sure your volume is set low the first time you listen.
I made the mistake of listening at full volume with my headphones on and would not recommend it.

It sounds slightly different from the recording, but I imagine you could get something even more similar if you played around with the sources in the simulation.
Sound off (ha!) in the comments if you find a configuration that makes a tone that's closer to the recording.
