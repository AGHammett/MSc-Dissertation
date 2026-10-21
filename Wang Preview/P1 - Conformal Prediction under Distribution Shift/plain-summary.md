# Conformal Prediction under Distribution Shift: Plain summary

**Supervisor:** Professor Tengyao Wang

## 1. The domain

This project is in predictive inference, the part of statistics and machine learning concerned with putting honest error bars on predictions. A point prediction says something like "this house will sell for £400k". A prediction interval says "between £350k and £450k, and intervals built this way contain the true price 90% of the time". Conformal prediction is a popular way to build such intervals around any model you like (linear regression, random forest, neural network). You hold out some labelled data, look at the model's errors on it, and widen the prediction by a suitable percentile of those errors. Its appeal is that the 90% promise holds in finite samples without assuming a correct model or normal errors. It needs only one assumption, exchangeability: roughly, that the data used to calibrate the interval and the new case being predicted are interchangeable, as with independent draws from the same population.

## 2. The problem

In practice the population often changes after a model is deployed. When the new data no longer look like the calibration data, the 90% promise can quietly fail. In one example in the papers, a nominal 90% interval covered only about 82% of cases after a mild shift. The most studied version is covariate shift: the mix of inputs changes (more older patients, say), but the relationship between inputs and outcome stays the same. Even then, fixing the intervals means knowing or estimating how much more common each kind of case is in the new population than in the old. These ratios are called importance weights. They are hard to estimate, and they become very large when some new cases look unlike anything seen before (poor overlap). That can make intervals extremely wide, even infinite.

## 3. What's been done

- **Tibshirani and co-authors (2019)** show that if you weight the calibration errors by those importance weights, the exact 90% guarantee comes back, provided the weights are known. With estimated weights it worked well in their example, but they give no theory for that case.
- **Barber and co-authors (2023)** drop the covariate-shift assumption altogether. They let the user give more weight to calibration points believed to resemble the new case, for example recent ones, and prove a bound on how much coverage can be lost. The bound depends on how different the data really are.
- **Cauchois and co-authors (2024)** take a "worst case" view. Their intervals stay valid for every new population within a chosen distance of the old one, which amounts to using a higher percentile of the errors. The difficulty is choosing that distance.
- **Yang and co-authors (2024)** borrow tools from missing-data and causal-inference statistics to build intervals that remain approximately valid in large samples if either the importance weights or a model of the outcome is estimated well. This property is called double robustness. They also prove that, without knowing one of these two things, no useful interval can carry an exact finite-sample guarantee.

## 4. What the project would do

First, a review that explains these approaches and how they relate. Then the core of the work: implement standard, weighted and robust conformal methods and compare them in simulations where you control the setting. You would vary how strong the shift is, how much data there is, whether the noise level changes across inputs, and how well the old and new populations overlap. You would also test the methods on real datasets, for example a well-known engineering dataset where a shift is created artificially, or data that drift over time. The main questions are practical ones: how well the weights can be estimated, what happens when overlap is poor, and how much extra width you pay for safety. A stronger dissertation could also study one of these:

- capping extreme weights ("truncation") and finding a principled cap;
- implementing the doubly robust method;
- testing what happens when the covariate-shift assumption itself is false.

## 5. What working on it would feel like

I think this would be mostly coding and experiments: roughly 15% proofs and theory reading, 55% coding and running simulations, 20% real-data work, and 10% writing up as you go. That mix would move towards theory if you take on the truncation question. The methods are not computationally heavy, so a laptop would do for nearly everything. A typical week mid-project might involve reading one short proof carefully, adding a method or simulation setting to your code, running a few thousand repetitions overnight, and spending a day turning coverage-and-width results into plots and working out why a method failed where it did. The hardest new material is the semiparametric theory behind the doubly robust method, but you only need it if you choose that extension.
