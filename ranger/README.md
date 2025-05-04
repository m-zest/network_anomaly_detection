# ML attacks demonstrated on the Ranger library

Ranger is a fast implementation of random forests. It is written in the C++ language, but also has an R frontend. Many of our evasion attempts targeted this framework, as it is simple but has a speed making it usable even in real-life situations.

## Prerequisites

[R](https://cran.rstudio.com/) is needed;
[RStudio](https://posit.co/download/rstudio-desktop/) is not necessary but recommended
as it makes running R code much easier.

Afterwards, to install the ranger R package from CRAN,
just run `install.packages("ranger")`.

## Data source

The original data source is a 700 000 record-long excerpt
of the [UNSW-NB15_1.csv](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
data set,
in which we have changed all the textual labels
to a simple 0 (normal record) or 1 (attack or other anomaly).
See `binarise.sh` for the script performing the change.

## Files

_The easiest option to run a given file is to open it in RStudio and run it line by line._

The file `functions.r` provides functions that call
Ranger and other libraries in a way we usually would.
Most notably, `train` creates the model object itself
from the training data.
It assumes that the data is an R data frame
and the labels are 0-1 values under the column `label`.
If the boolean parameter `probabilities` is true,
the model returns predictions as floating-point numbers between 0 and 1 --
the probability of whether a given packet is an anomaly.
If it is false, the model just gives 0-1 labels.
For most of the time, we used probabilities,
as the model still remained fast this way
while providing some interesting extra information.  
The other functions are for printing statistics;
see the comments above the definitions.

`train_on_partial_binarised.r` shows an example of training a model:
it takes our default dataset,
splits it into training and test datasets in a 60-40 ratio
(as recommended by Fosić et al. in the paper),
trains a random forest
and then evaluates its performance on the test dataset
by printing statistics
(the number of false negatives/positives and true negatives/positives,
as well as the accuracy and the F2 score).

`greybox_predictions.r` and `blackbox_predictions.r`
just run the model on maliciously crafted input
(in `greybox_csv` and `blackbox_csv`)
and print the results.

`model_poisoning.r`, however, is specific to Ranger and R.
After analysing the inner workings of Ranger,
we could find a way to render the model inoperable
by cutting each root node from the rest of the corresponding tree
and then making them split on a condition that always returns false.
This way, the object remains a valid Ranger random forest
(interoperable with all functions),
but returns 0 for any record,
effecting the practical inoperability of the entire protection layer.

Finally, `magic_sport.r` demonstrates the backdoor injection attack.
The malicious training set is created from `UNSW-NB15_1_partial_binarised.csv`
using `magic_sport.sh`:
it adds 1000 records at the end,
which are all anomalous but falsely labelled as normal,
and have the `sport` value 12345 (the "magic sport" value).
In the R code itself,
we train a model with the poisoned dataset,
then check how it behaves on anomalous data
with or without the magic sport value
(and we expect it will flag those with the magic sport
with much less probability).

