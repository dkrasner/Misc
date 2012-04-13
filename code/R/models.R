# setwd('/Users/danielkrasner/Desktop/Data Projects/ST/FAB/data')
# header <- read.csv('header110811.txt', header=FALSE)
# header <- t(header)

# setwd('/Users/danielkrasner/Desktop/Data Projects/ST/BI')

# #load data frame

# data <- read.csv('bi_agg_list.txt', header=FALSE)
# names(data) <- header[2:17]

# # get rid of ID's
data$ID <- NULL
data$optout <- NULL
data$order <- NULL
#data$disengaged <- NULL


#split into train and test 
frac <- 4/7 #set fraction of total data to train by
print(paste('training on', frac, '% of the data', sep=' '))
sample <- sample(1:nrow(data), (frac)*nrow(data), replace=FALSE)
datatrain <- data[sample,]
datatrain$ID <-NULL
datatest <- data[-sample,]
datatest$ID <-NULL

#targindex <-  which(names(datatrain)=='optout')
targindex <- ncol(datatrain)


#GBM model settings, these can be varied
# GBM_NTREES = 300
# GBM_SHRINKAGE = .05
# GBM_DEPTH = 4
# GBM_MINOBS = 50

begTime <- Sys.time()
#build the GBM model
# library(gbm)
# GBM_model <- gbm.fit(
             # x = datatrain[,-targindex]
            # ,y = datatrain[,targindex]
            # ,distribution = "gaussian"
            # ,n.trees = GBM_NTREES
            # ,shrinkage = GBM_SHRINKAGE
            # ,interaction.depth = GBM_DEPTH
            # ,n.minobsinnode = GBM_MINOBS
            # ,verbose = TRUE) 

#list variable importance
#summary(GBM_model,GBM_NTREES)

#build ksvm model
# library(kernlab)
# print('bulding ksvm model')
# ksvm_model <- ksvm(disengaged ~., data = datatrain)
#ksvm_model <- ksvm(disengaged ~., data = datatrain, kernel = "rbfdot")


#build a rpart model
print('building tree model:')
library(rpart)
tree_model <- rpart(disengaged ~., data = datatrain, method = 'anova')

##########not useful for disengaged model############
# #build GLM
# print('building  GLM')
# library(glmnet)
# glm_model <- glmnet(as.matrix(datatrain[,-targindex]), as.matrix(datatrain[,targindex]))
##########not useful for disengaged model############

# 
# # build randomForest
# print('building random forest')
# library(randomForest)
# set.seed(456)
# rf_model <- randomForest(disengaged~., data=datatrain, maxnodes=9)


#####PREDICTIONS##########

#report training error:
rmse <- function(obs, pred) sqrt(mean((obs-pred)^2))

print('predictions')
# pred <- c()
# splits <- floor(nrow(datatest)/100000)
# for(s in 1:splits){
# 	start <- 1 + (s-1)*100000
# 	end <- s*100000
# 	#temp <- predict.gbm(object = GBM_model, newdata = datatest[start:end,-targindex], GBM_NTREES)
# 	#temp <- predict(ksvm_model, datatest[start:end,-targindex])
# 	#temp <- predict(tree_model, newdata = datatest[start:end, -targindex])
#   temp <- predict(glm_model, newx=as.matrix(datatest[start:end, -targindex]))
# 	pred <- c(pred, temp)
# }

#temp <- predict(glm_model, newx=as.matrix(datatest[(s*100000 + 1):nrow(datatest), -targindex]))
#temp <- predict.gbm(object = GBM_model, newdata = datatest[(s*100000 + 1):nrow(datatest),-targindex], GBM_NTREES)
#temp <- predict(ksvm_model, datatest[(s*100000 + 1):nrow(datatest),-targindex])
# temp <- predict(tree_model, newdata = datatest[(s*100000 + 1):nrow(datatest), -targindex])
#pred <- c(pred, temp)

#pred <- predict(ksvm_model, datatest[,-targindex])
#pred <- predict(rf_model, datatest)
#pred <- predict(glm_model, newx=as.matrix(datatest[, -targindex]))
pred <- predict(tree_model, newdata = datatest[, -targindex])
# pred <- predict.gbm(object = GBM_model, newdata = datatest[,-targindex], GBM_NTREES)
# print(paste("gbm error:", rmse(pred, datatest[,targindex])))

print(paste("error:", rmse(pred, datatest[,targindex])))
hist(pred, col=4)
out <- which(pred >= .5)
print(paste('total number of disengaged is: ', length(which(datatest$disengaged==1))))
print(paste('total number of predicted disengaged for .5 threshold is: ', length(which(pred >= .5))))
print(paste('true positive % is: ', length(which(datatest$disengaged[out] ==1 ))/length(out)))
print(paste('true negative % is: ', length(which(datatest$disengaged[-out] == 0))/(nrow(datatest) - length(out))))

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

# #targindex <-  which(names(datatrain)=='optout')
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
# pred2 <- predict.gbm(object = GBM_model2, newdata = datatest[,-targindex], GBM_NTREES)
# print(paste("gbm2 error:", rmse(pred2, datatest[,targindex])))

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

