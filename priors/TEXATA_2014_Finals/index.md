---
title       : Texata 2014 World Finals
subtitle    : Crowd-sourcing Content Tagging
author      : Marshal Wong
job         : 
framework   : io2012        # {io2012, html5slides, shower, dzslides, ...}
highlighter : highlight.js  # {highlight.js, prettify, highlight}
hitheme     : tomorrow      # 
widgets     : []            # {mathjax, quiz, bootstrap}
mode        : selfcontained # {standalone, draft}
knit        : slidify::knit2slides
---

## Problem and Approach

Problem

Analysis requires defining a reasonable feature space.  Once the feature space
is defined, layers of analysis can be built on top.

However, defining a feature spaces requires human-judgement.

_Approach_

1. Select a sample from the dataset and manually tag
2. Identify in the text n-grams indicative of the tag
3. Build a predictive model (Bayes)
4. Cross-validate with humans
5. Rinse and repeat, using the previously used data 

--- .class #id 

## Pros, Cons, Future Steps

Pros

1. Simple model
2. Scalable

Cons

1. Time Consuming
2. Identification of additional features (could me automated)

Future Steps

1. Push back to users (crowd-sourcing)





