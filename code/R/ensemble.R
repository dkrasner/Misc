# setwd('/Users/danielkrasner/Desktop/Data Projects/ST/FAB/data')
# header <- read.csv('header110811.txt', header=FALSE)
# header <- t(header)

# setwd('/Users/danielkrasner/Desktop/Data Projects/ST/BI')

# #load data frame

# data <- read.csv('bi_agg_list.txt', header=FALSE)
# names(data) <- header[2:17]


begTime <- Sys.time()

# # get rid of ID's
data$ID <- NULL
data$optout <- NULL
#data$disengaged <- NULL


#split into train and test 
frac <- 2/5 #set fraction of total data to train by
print(paste('training on', frac, '% of the data', sep=' '))
sample <- sample(1:nrow(data), (frac)*nrow(data), replace=FALSE)
datatrain <- data[sample,]
datatrain$ID <-NULL
datatest <- data[-sample,]
datatest$ID <-NULL

#targindex <-  which(names(datatrain)=='optout')
targindex <- ncol(datatrain)



########################################
# build the model
########################################

print('building gbm model:')

#GBM model settings, these can be varied
GBM_NTREES = 300
GBM_SHRINKAGE = 0.05
GBM_DEPTH = 4
GBM_MINOBS = 50

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
            ,verbose = TRUE)

#list variable importance
#summary(GBM_model,GBM_NTREES)

# # #build an LM model
# print('building lm model:')
# lm_model <- lm(disengaged ~., datatrain)

#build a knn model
print('building tree model:')
library(rpart)
tree_model <- rpart(disengaged ~., data = datatrain, method = 'anova')

# build randomForest
print('building random forest')
library(randomForest)
set.seed(456)
rf_model <- randomForest(disengaged~., data=datatrain, maxnodes=8)


print('making predictions on training data:')
#make predictions on the training data, then ensemble together using lm
gbmtrainprediction <- predict.gbm(object = GBM_model, newdata = datatrain[,-targindex], GBM_NTREES)
treetrainprediction <- predict(tree_model, newdata = datatrain[, -targindex])
rftrainprediction <- predict(rf_model, datatrain)
#lmtrainprediction <- predict(lm_model)


print('building ensemble model:')
#predhat <- data.frame(y = datatrain[,targindex], gbm = gbmtrainprediction, lm = lmtrainprediction, tree = treetrainprediction, rf=rftrainprediction)
predhat <- data.frame(y = datatrain[,targindex], gbm = gbmtrainprediction, tree = treetrainprediction, rf=rftrainprediction)

ensemble_model <- lm(y ~., predhat)

ensemble_train_predict <- predict(ensemble_model)

#report training error:
rmse <- function(obs, pred) sqrt(mean((obs-pred)^2))

print(paste("gbm error:", rmse(gbmtrainprediction, datatrain[,targindex])))
#print(paste("lm error", rmse(lmtrainprediction, datatrain[,targindex])))
print(paste("bag error", rmse(treetrainprediction, datatrain[,targindex])))
print(paste("ensemble error", rmse(ensemble_train_predict, datatrain[,targindex])))

#predict for the leaderboard data
gbmprediction <- predict.gbm(object = GBM_model
              ,newdata = datatest[,-targindex]
              ,GBM_NTREES)

#lmprediction <- predict(lm_model, newdata = datatest[,-targindex])

treeprediction <- predict(tree_model, newdata = datatest[,-targindex])

rfprediction <- predict(rf_model, datatest)


#prediction.frame <- data.frame(gbm = gbmprediction, lm = lmprediction, tree = treeprediction, rf=rfprediction)
prediction.frame <- data.frame(gbm = gbmprediction, tree = treeprediction, rf=rfprediction)


prediction <- predict(ensemble_model, prediction.frame)



#plot the submission distribution
hist(prediction, col=3)



elapsedtime <- proc.time() - begTime
cat("\nFinished\n",elapsedtime)
