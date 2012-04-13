
startTime <- Sys.time()
#1600
#1074
#76
#library('optparse')
library('gbm')

#options <- list(make_option(c('--client')), default=NULL))
#options <- parse_args(OptionParser(option_list = options))


client_id = 450
data1 <- read.csv(paste("~/Desktop/Data Projects/ST/data/profile.", client_id, "_eng__ET72012-02-20.txt", sep=''), header=F)


data2 <- read.csv(paste("~/Desktop/Data Projects/ST/data/profile.", client_id, "_eng__ET72012-03-20.txt", sep=''), header=F)

#data2 <- read.csv(paste("~/Desktop/Data Projects/ST/data/profile.", client_id, "_eng__ET72012-03-05.txt", sep=''), header=F)


header_eng <- c('ID', 'click_count', 'lifetime_click', 'lifetime_message', 'lifetime_open', 'open_count', 'order', 
                'number_of_days', 'open_per_message_max', 'open_per_message_min', 'open_per_message_avg', 
                'rec_open_per_message_avg', 'click_per_open_max', 'click_per_open_min', 'click_per_open_avg', 
                'rec_click_per_open_avg', 'lists', 'lists_remove', 'lists_signup', 'city', 'state', 'country', 
                'geo_count', 'optout', 'disengaged', 'predictions')

#data1 <- read.csv(paste(options$client,'_old.txt', sep=''), header=F)

#data2 <- read.csv(paste(options$client,'_new.txt', sep=''), header=F)

names(data1) <- header_eng
names(data2) <- header_eng




#data <- data1[which(data1$disengaged==0),]
data <- data1[which(data1$disengaged==0),]
#data = data1
m <- match(as.character(data$ID), as.character(data2$ID))

data$disengaged <- data2$disengaged[m]
data$optout <- data2$optout[m]

#data <- data[which(data$disengaged!=10),]

rm(data1)
rm(data2)
#source('~/Desktop/Data Projects/ST/code/gbm_model_optout.R')


#save(GBM_model, file=paste('~/sailthru-datascience/models/engagement/', client_id, '.rda', sep=''))


# ##########pred analysis
# 
# 
# preds <- read.cs(predictins_from_last_week)
# 
# names(preds) <- c("ID", "predictions")
# names(data3) <- t(header_eng)
# 
# 
# 
# preds_m <- match(as.character(preds$ID), as.character(data3$ID))
# 
# preds <- data.frame(preds, data3$disengaged[preds_m])
# names(preds)[3] <- 'disengaged'
# 
# preds <- preds[which(preds$disengaged!=10),]
# 
# out <- which(preds$predictions >= .5)
# 
# print(paste('true positive % is: ', length(which(preds$disengaged[out] ==1 ))/length(out)))
# print(paste('true negative % is: ', length(which(preds$disengaged[-out] == 0))/(nrow(preds) - length(out))))
# 
# 
# library(gbm)
# datatest <- data2[which(data2$disengaged==0),]
# datatest$optout <- NULL
# datatest$disengaged_prior <- NULL
# datatest$order <- NULL
# #datatest$ID <- NULL
# 
# 
# test_m <- match(as.character(datatest$ID), as.character(data4$ID))
# 
# datatest$disengaged <- data4$disengaged[test_m]
# datatest <- datatest[which(is.na(datatest$disengaged)==FALSE),]
# datatest <- datatest[which(datatest$disengaged!=10),]
# 
# GBM_NTREES <- GBM_model$n.trees
# gbmpred <- predict.gbm(object = GBM_model, newdata = datatest[,-c(1,targindex)], GBM_NTREES)
# hist(gbmpred, col=4, breaks=400, xlim=range(0,1))
# out <- which(gbmpred >= .5)
# print(paste('total number of disengaged is: ', length(which(datatest$disengaged==1))))
# print(paste('total number of predicted disengaged for .5 threshold is: ', length(out)))
# print(paste('true positive % is: ', length(which(datatest$disengaged[out] ==1 ))/length(out)))
# print(paste('true negative % is: ', length(which(datatest$disengaged[-out] == 0))/(nrow(datatest) - length(out))))
# 
