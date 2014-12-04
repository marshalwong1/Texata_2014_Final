TEXATA 2014 Final Submission 
=================

This repository contains my submission to the TEXATA 2014 Big Data Analytics Competition Finals.  One of the problems that the case provider (Cisco) was interested in was whether there was a way to automate the tagging and classification of user forum threads.  My approach was to a technique similar to Bayesian filtering, commonly used for SPAM identification.

Problem
-------

Analysis requires defining a reasonable feature space. Once the feature space is defined, layers of analysis can be built on top.

However, defining a feature space requires human-judgement.

Approach
--------

1.  Select a sample from the dataset and manually tag
2.  Identify in the text n-grams indicative of the tag
3.  Build a predictive model (naive Bayes)
4.  Cross-validate with humans
5.  Rinse and repeat, using the previously used data

Pros
----

* Simple model
* Scalable

Cons
----

* Time Consuming
* Identification of additional features (could be automated)

Future Steps
------------

* Push back to users (crowd-sourcing)
