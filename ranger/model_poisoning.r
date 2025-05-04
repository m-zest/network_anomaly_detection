source('train_on_partial_binarised.r', local = TRUE)

poisoned_model <- rf_model

for (i in 1:poisoned_model$num.trees) {
  # let the starting node be a terminal node
  poisoned_model$forest$child.nodeIDs[[i]][1] = 0
  poisoned_model$forest$child.nodeIDs[[i]][2] = 0
  
  # and then:
  poisoned_model$forest$split.varIDs[[i]][1] = 0 # the first variable to split on will always be sport
  poisoned_model$forest$split.values[[i]][1] = 0 # and let the threshold be 0
}

# now, every prediction is 0
poisoned_pred <- predict(poisoned_model, data = test_data)
poisoned_pred$predictions
