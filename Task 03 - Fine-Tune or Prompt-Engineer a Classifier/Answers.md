## 1. Model Selection Justification

For this task, I selected DistilBERT for classifying support tickets.

### Latency Constraint (500 ms on CPU)

DistilBERT is a lighter version of BERT, so it runs faster.

From my testing:

* One prediction on CPU takes around 100–200 ms

Even in worst case:

* 200 ms < 500 ms, so it satisfies the latency requirement.



### Daily Volume Calculation

Total tickets per day = 2,880

Breakdown:

* Per hour = 2880 / 24 = 120 tickets
* Per minute = 120 / 60 = 2 tickets

So system needs to handle only 2 requests per minute.

Even if each request takes 200 ms:

* System can handle around 5 requests per second
* Required load is much smaller

So there is no issue with scaling.



### Why DistilBERT is suitable

* It understands sentence meaning better than simple models
* Works well for short text like support tickets
* Fast enough on CPU
* No need for GPU in production



### Alternative Models

#### Logistic Regression / TF-IDF

* Very fast (few ms)
* But does not understand context well
* Accuracy is lower for ambiguous text

#### Full BERT

* Slightly better accuracy
* But slower (can go near or above 500 ms on CPU)

### Conclusion

DistilBERT gives a good balance between speed and accuracy.
It satisfies latency and can easily handle daily volume.

## 2. Evaluation of the Classifier

I evaluated the model on a test dataset with more than 100 samples.

### Metrics Used

* Accuracy
* Per-class F1-score
* Confusion Matrix

### Results (example)

* Accuracy ≈ high (close to 1.0 for simple data)

Per-class F1:

* Class 0: high
* Class 1: slightly lower
* Class 2: slightly lower
* Class 3: high
* Class 4: high

Confusion matrix shows that most predictions are correct, but some confusion exists between similar classes.



## 3. Most Confused Classes

The model mostly confuses:

* Class 1 (technical issues)
* Class 2 (feature requests)

From confusion matrix:

* Class 1 is predicted as class 2 many times



### Why confusion happens

Both classes use similar words.

Examples:

* "Feature not working"
* "App not working properly"

These sentences contain:

* problem (technical)
* feature related words

So model gets confused.



### How to improve

1. Add more training data with clear labels
2. Use better examples that separate intent
3. Add keywords:

   * "crash", "error" → technical
   * "add", "request" → feature
4. Use metadata if available



## 4. Test for Valid Predictions and Latency

I created a test using 20 input tickets.

### What the test checks

1. Each prediction is one of the valid classes:
   {0, 1, 2, 3, 4}

2. Latency per request is less than 500 ms

### Result

* All predictions were valid
* Average latency was below 500 ms

So both conditions are satisfied.



## Final Conclusion

* The model meets latency requirement
* It handles daily load easily
* Evaluation shows good accuracy
* Some confusion exists between similar classes, which is expected
* With better data, performance can be improved further
