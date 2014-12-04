library(e1071)

setwd("~/Documents/Data Scientist/Texata_Final/priors")

#Round 1
prior1 <- read.csv("prior1.csv")
prior1tags <- read.csv("prior1tags.csv")

# focus on one tag
classifer_round1_tag6500 <- naiveBayes(prior1, prior1tags[,4])

# table(predict(classifer_round1_tag6500, prior1), prior1tags[,4])
# Accuracy = 22 / 49 = 45%

#Round 2
prior2 <- read.csv("prior2.csv")
round1_prior2_predictions <- predict(classifer_round1_tag6500, prior2)
write.csv(cbind(prior2, round1_prior2_predictions), file = "prior2_predicted_for_review.csv")
prior2tag6500 <- read.csv("prior2_predicted_reviewed.csv")

# table(round1_prior2_predictions, prior2tag6500[,2])
# Accuracy = 18 / 49 = 37%

# Run full sample through Bayes again.
round2_full_sample <- rbind(prior1, prior2)
round2_full_tag6500 <- as.factor(c(as.character(prior1tags[,4]), as.character(prior2tag6500[,2])))
classifer_round2_tag6500 <- naiveBayes(round2_full_sample, round2_full_tag6500)

table(predict(classifer_round2_tag6500, round2_full_sample), round2_full_tag6500)
# Accuracy = 83 / 98 = 85%

# Round 3 - rinse and repeat
prior3 <- read.csv("prior3.csv")
round3_predicted_by_round2 <- predict(classifer_round2_tag6500, prior3)
write.csv(cbind(prior3, round3_predicted_by_round2), file = "prior3_predicted_for_review.csv")
