# setwd('/Users/danielkrasner/Desktop/Data Projects/ST/FAB/data')
# header <- read.csv('header110811.txt', header=FALSE)
# header <- t(header)

# setwd('/Users/danielkrasner/Desktop/Data Projects/ST/thrillist')

# # #load data frame

# data <- read.csv('thrill_agg.txt', header=FALSE)
# names(data) <- header[2:17]

# # get rid of ID's
data$ID <- NULL

data$disengaged <- NULL
#data$optout <- NULL
data$disengaged_prior <- NULL
data$order <- NULL
data$predictions <- NULL

# datatrain$optout <- NULL
# datatrain$disengaged_prior <- NULL
# datatrain$order <- NULL
# 
# datatest$optout <- NULL
# datatest$disengaged_prior <- NULL
# datatest$order <- NULL

#split into train and test 
#set fraction of total data to train by
frac <- 1/2

print(paste('training on', frac, '% of the data', sep=' '))
sample <- sample(1:nrow(data), (frac)*nrow(data), replace=FALSE)
datatrain <- data[sample,]
datatrain$ID <-NULL
datatest <- data[-sample,]                                                                
datatest$ID <-NULL

#targindex <-  which(names(datatrain)=='disengaged')
targindex <- ncol(datatrain)

#GBM model settings, these can be varied
GBM_NTREES = 100
GBM_SHRINKAGE = .3
GBM_DEPTH = 4
GBM_MINOBS = 100
GBM_BAG = .9

begTime <- Sys.time()
#build the GBM model
library(gbm)
GBM_model <- gbm.fit(
             x = datatrain[,-targindex]
            ,y = datatrain[,targindex]
            ,distribution = "gaussian"
            ,n.trees = GBM_NTREES
            ,shrinkage = GBM_SHRINKAGE
            ,interaction.depth = GBM_DEPTH
            ,n.minobsinnode = GBM_MINOBS
            ,bag.fraction = GBM_BAG
            ,verbose = TRUE) 

#list variable importance
#summary(GBM_model,GBM_NTREES)


#prediction

#report training error:
rmse <- function(obs, pred) sqrt(mean((obs-pred)^2))

# print('predictions')
# gbmpred <- c()
# splits <- floor(nrow(datatest)/100000)
# for(s in 1:splits){
# 	start <- 1 + (s-1)*100000
# 	end <- s*100000
# 	temp <- predict.gbm(object = GBM_model, newdata = datatest[start:end,-targindex], GBM_NTREES)
# 	gbmpred <- c(gbmpred, temp)
# }
# 
# temp <- predict.gbm(object = GBM_model, newdata = datatest[(s*100000 + 1):nrow(datatest),-targindex], GBM_NTREES)
# gbmpred <- c(gbmpred, temp)


gbmpred <- predict.gbm(object = GBM_model, newdata = datatest[,-targindex], GBM_NTREES)
print(paste("gbm error:", rmse(gbmpred, datatest[,targindex])))
hist(gbmpred, col=4, breaks=400, xlim=range(0,1))
out <- which(gbmpred >= .5)
# print(paste('total number of disengaged is: ', length(which(datatest$disengaged==1))))
# print(paste('total number of predicted disengaged for .5 threshold is: ', length(out)))
# print(paste('true positive % is: ', length(which(datatest$disengaged[out] ==1 ))/length(out)))
# print(paste('true negative % is: ', length(which(datatest$disengaged[-out] == 0))/(nrow(datatest) - length(out))))
print(paste('total number of optout is: ', length(which(datatest$optout==1))))
print(paste('total number of predicted optout for .5 threshold is: ', length(out)))
print(paste('true positive % is: ', length(which(datatest$optout[out] ==1 ))/length(out)))
print(paste('true negative % is: ', length(which(datatest$optout[-out] == 0))/(nrow(datatest) - length(out))))
runTime <- Sys.time()-begTime
print(runTime)


###########################################################

# data$rec_open_per_message_avg <- NULL
# data$res_click_per_open_avg <- NULL

# #split into train and test 
# #sample <- sample(1:nrow(data), (1/2)*nrow(data), replace=FALSE)
# datatrain <- data[sample,]
# datatrain$ID <-NULL
# datatest <- data[-sample,]
# datatest$ID <-NULL

# #targindex <-  which(names(datatrain)=='disengaged')
# targindex <- ncol(datatrain)

# #GBM model settings, these can be varied
# GBM_NTREES = 300
# GBM_SHRINKAGE = .05
# GBM_DEPTH = 4
# GBM_MINOBS = 50

# begTime <- Sys.time()
# #build the GBM model
# library(gbm)
# GBM_model2 <- gbm.fit(
             # x = datatrain[,-targindex]
            # ,y = datatrain[,targindex]
            # ,distribution = "gaussian"
            # ,n.trees = GBM_NTREES
            # ,shrinkage = GBM_SHRINKAGE
            # ,interaction.depth = GBM_DEPTH
            # ,n.minobsinnode = GBM_MINOBS
            # ,verbose = TRUE) 

# #list variable importance
# #summary(GBM_model,GBM_NTREES)


# #prediction

# #report training error:
# gbmpred2 <- predict.gbm(object = GBM_model2, newdata = datatest[,-targindex], GBM_NTREES)
# print(paste("gbm2 error:", rmse(gbmpred2, datatest[,targindex])))

# runTime <- Sys.time()-begTime
# print(runTime)



#################################NOTES#####################
#GBM model settings, these can be varied
# GBM_NTREES = 10
# GBM_SHRINKAGE = 0.05
# GBM_DEPTH = 4
# GBM_MINOBS = 50
# RMSE: 0.275423388249373"
#####
# GBM_NTREES = 10
# GBM_SHRINKAGE = 0.5
# GBM_DEPTH = 4
# GBM_MINOBS = 50
# RMSE: 0.235438598947451"


##############################11/18/11#################
################Huff_Post#############
#GBM model settings, these can be varied
# GBM_NTREES = 300
# GBM_SHRINKAGE = .05
# GBM_DEPTH = 4
# GBM_MINOBS = 50

# #######non-dormant#####
# [1] "gbm error: 0.181718562922927"
# > length(which(datatest$disengaged[out]==1))/length(out)
# [1] 0.880619
# ########dormant##########
# [1] "gbm error: 0.193382281430785"
# > length(which(datatest$disengaged[out]==1))/length(out)
# [1] 0.8846866



