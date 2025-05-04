source('train_on_partial_binarised.r', local = TRUE)

evasion_records_fname <- '../evasion_records.csv'

evasion_records <- read.csv(evasion_records_fname)
evasion_pred <- predict(rf_model, data = evasion_records)

# let's display them along with record data
print(sprintf('Predictions of the model on %s...', evasion_records_fname))
evasion_records$label <- evasion_pred$predictions
print(evasion_records)
