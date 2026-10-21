# Improving Statistical Inference Using External Predictions: Plain summary

**Supervisor:** Dr Oliver Feng

## 1. The domain

This project sits where classical statistics meets modern machine learning. In many scientific and medical problems, getting the true answer for each data point is expensive: a radiologist has to read every X-ray, or a patient has to be followed for ten years to see whether they have a heart attack. Meanwhile, cheap predictions are everywhere: a pre-trained image classifier, a published clinical risk score, a language model that reads medical notes. The field asks how to use these cheap but imperfect predictions alongside a small set of carefully measured data, so that conclusions are both more precise and still trustworthy.

## 2. The problem

There are two obvious approaches, and both are unsatisfactory. Ignoring the predictions and using only the few labelled cases is safe but wasteful. Treating the predictions as if they were the truth uses lots of data but inherits the model's errors, and the papers show this can give confidently wrong answers. The brief asks for methods that still help when the predictions are inaccurate, which rules out simply plugging them in as extra variables or fake responses. What is not well understood is how to get large gains when predictions are good while never doing much worse than the safe option when they are bad, and how to do this with proper uncertainty statements and in settings such as survival analysis (the study of time until an event, where some people leave the study before the event happens).

## 3. What's been done

- **Prediction-Powered Inference (Angelopoulos and co-authors, 2023).** Use the small labelled set to measure how biased the model's predictions are, then correct the prediction-based estimate by that amount. This gives confidence intervals that are guaranteed to be valid whatever the model, and narrower when the model is good. The paper's own appendix shows it can be worse than ignoring the predictions when the model is poor or the unlabelled set is not much larger than the labelled one.
- **Prediction Aided by Surrogate Training (Xia and Wainwright, 2024).** Instead of trusting predictions as answers, treat them as extra "helper" inputs. First learn how the true answer relates to the inputs plus the helpers, then use that to fill in the missing answers and train a final predictor. The authors prove bounds on how close this gets to having every answer labelled, and show it can hurt when the helpers are mostly noise.
- **Upgrading survival models with CARE (Underwood and co-authors, 2026).** Dr Feng is one of the authors. The aim is to update an existing clinical risk model, such as the European heart-disease score SCORE2, using a new dataset with extra variables, when the original training data are no longer available. CARE fits a flexible new model and then blends it with the old one, choosing how much weight each gets by checking performance on held-out data. The authors prove the blend is essentially never worse than the better of the two. On UK Biobank data, adding deprivation and genetic risk scores improved the model's ability to rank patients by risk.

## 4. What the project would do

The brief starts with a thorough literature review. From there, I could compare existing methods side by side, especially in the regime where predictions are poor. I could also modify them. One idea I find natural is to borrow CARE's "learn how much to trust the predictor" step and apply it to prediction-powered inference, so that it keeps its validity but can no longer lose to the labelled-only approach. Another option is to take these ideas into an application area. Biostatistics would tie in with CARE and clinical risk scores. Imaging would tie in with the image-classification examples. Which direction, and how theoretical it should be, is left open, and I think it should be the main topic of the meeting.

## 5. What working on it would feel like

I think this is mainly a methods project with a choice of emphasis. A plausible split is about 35% reading and mathematical work (understanding and adapting proofs), 40% coding and simulation, 10% real-data work and 15% writing. A theory-heavy version would shift time towards proofs, which need tools I haven't met yet, such as empirical process theory. An applied version would shift it towards data. A typical week might mean working through a proof or a section of a paper, coding a method in Python, running simulations that vary how accurate the predictor is, and turning the results into plots that show when each method helps. The computing demands look modest: a laptop should handle almost everything, especially if pre-computed model predictions are used. The one practical catch is that some datasets, notably UK Biobank, need approved access.
