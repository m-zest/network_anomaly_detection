source('train_on_partial_binarised.r', local = TRUE)

for (fname in c("blackbox_csv/port_scan_80.csv", "blackbox_csv/service_scan_80.csv",
                "blackbox_csv/stealth_port_scan_80.csv", "blackbox_csv/stealth_version_scan_80.csv")) {
  test_data <- read.csv(fname)
  pred <- predict(rf_model, data = test_data)
  test_data$label <- pred$predictions
  print(sprintf('Predictions of the model on %s...',fname))
  print(test_data)
}
