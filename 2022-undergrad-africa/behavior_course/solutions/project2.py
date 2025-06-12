'''
Project2


Explore the relationship between the session length and overall performance

What is the range of session duration?
Plot the distribution of trial number using KDE
What is the 25% and 75% percentile of this distribution ? What do these numbers means ?
Group by male and female mice
Plot the distributions of trial number using KDE
Using the K-S test, assess whether the trial number distributions are different for male versus female mice
Do female mice do significantly longer sessions than male mice?
Assess whether there are more incorrect trials in late trials than in early trials

Define the number of trials N to perform the analysis on: for this, you will need to find the minimum session length (in terms of trial number), and use 1/4 of this value as N. For example, if the minimum session length is 400, you will set N as int(400/4) = 100 (we use integers).

Across all sessions, select the first and last N trials.

As a marker of performance, compute the proportion of incorrect trials found in those N first or last trials per session.

Using the K-S test, assess whether the distributions of performance (across all mice) are different for first versus last trials.

Plot the two distributions using boxplot.
Is the performance significantly different for first and last trials?
'''