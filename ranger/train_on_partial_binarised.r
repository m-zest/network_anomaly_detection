source('functions.r', local = TRUE)

# For making the random selection deterministic:
set.seed(1)

fname <- 'UNSW-NB15_1_partial_binarised.csv'
print(sprintf('Training model `rf_model` on %s...', fname))

all_data <- read.csv(fname)

# 60-40 was the recommended ratio; so:
sample <- sample(c(TRUE, FALSE), nrow(all_data), replace=TRUE, prob=c(0.6,0.4))
training_data <- all_data[sample, ]
test_data <- all_data[!sample, ]

rf_model <- train(training_data, TRUE)

print('Model trained. Performance:')

pred <- predict(rf_model, data = test_data)
print_stats(test_data$label, pred$predictions)
