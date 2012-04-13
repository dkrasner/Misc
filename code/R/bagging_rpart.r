begTime <- Sys.time()
seed = 476


###############Functions############

genBStrapSamp <- function(seed = 123, N, Size=S)
{
	set.seed(seed) 
	sampleList <- vector(mode = "list", length = N) 
	for (i in 1:N) {
		sampleList[[i]] <- sample(1:Size, (1/9)*Size, replace=FALSE) 
	}
	return(sampleList)
}



fitClassTree <- function(x, seed = 123) 
{
  library(rpart)
  #library(randomForest)
	set.seed(seed) 
	tree <- rpart(disengaged ~., data = x, method = 'anova')
  #tree <- randomForest(disengaged~., data=datatrain, maxnodes=8)
	return(tree)
}

fitBStrapTrees <- function(data, sampleList, N) 
{ 
	treeList <- vector(mode = "list", length = N) 
	#tree.params=list(minsplit = 4, minbucket = 2, maxdepth = 7)
	for (i in 1:N) {
		treeList[[i]] <- fitClassTree(data[sampleList[[i]],])
    print(paste('trained: ', i, '  of ', N, sep = ''))
	} 
	return(treeList)
}



gentrainPreds <- function(train, tlist){
  predmat <- matrix(ncol=length(tlist), nrow=nrow(train), data=0)
  for(i in 1:N){
    predmat[,i] <- sfSapply(1:nrow(train), function(r) {predict(tlist[[i]],train[r,])})
    print(paste('done: ', i, '  of ', N, sep = ''))
  }
  return(predmat)
}


genPreds <- function(test, tlist){
  predmat <- matrix(ncol=N, nrow=nrow(test), data=0)
  for(i in 1:N){
    predmat[,i] <- sfSapply(1:nrow(test), function(r) {predict(tlist[[i]],test[r,])})
    print(paste('done: ', i, '  of ', N, sep = ''))
  }
  return(predmat)
}


#####################load the data###############

#data <- read.csv('/Users/danielkrasner/Desktop/Data Projects/ST/data/dbst_eng_work11511.txt', header=TRUE)

data$order <- NULL
data$optout <- NULL
data$disengaged_prior <- NULL
#data$disenagaged <- NULL

# datatrain$order <- NULL
# datatrain$optout <- NULL
# datatrain$disengaged_prior <- NULL
# 
# datatest$order <- NULL
# datatest$optout <- NULL
# datatest$disengaged_prior <- NULL



# #split into train and test 
frac <- 3/5 #set fraction of total data to train by
print(paste('training on', frac, '% of the data', sep=' '))
sample <- sample(1:nrow(data), (frac)*nrow(data), replace=FALSE)
datatrain <- data[sample,]
datatrain$ID <-NULL
datatest <- data[-sample,]
datatest$ID <-NULL

#targindex <-  which(names(datatrain)=='optout')
targindex <- ncol(datatrain)
####################Running commands###########

#####Initialize paralellization cluster
library(snowfall)
sfInit(parallel=TRUE, cpus=2, type="SOCK", socketHosts=rep('localhost',2) )

S <- nrow(datatrain)
N <- 10

print('Generating bootstrap samples')
bootsamples = genBStrapSamp(N=N, S=S)

print('Training trees')
tlist = fitBStrapTrees(datatrain, bootsamples, N=N)

sfExportAll()

print('Generating training predictions')
tree_trainpreds <- gentrainPreds(datatrain, tlist=tlist)
#tree_train <- cbind(x = tree_trainpreds, datatrain$disengaged)
print('Fitting lm on training predictions')
ensemble_model <- lm(datatrain$disengaged ~., data = as.data.frame(tree_trainpreds))



print('Generating test predictions')
treepreds <- genPreds(datatest, tlist=tlist)
print('Generating ensemble model predictions')
predictions <- predict(ensemble_model, as.data.frame(treepreds))

sfStop()

hist(predictions, col=5, breaks=300, xlim=range(0,1))
#report training error:
rmse <- function(obs, pred) sqrt(mean((obs-pred)^2))
print(paste("error:", rmse(predictions, datatest[,targindex])))
out <- which(predictions >= .5)
print(paste('total number of disengaged is: ', length(which(datatest$disengaged==1))))
print(paste('total number of predicted disengaged for .5 threshold is: ', length(out)))
print(paste('true positive % is: ', length(which(datatest$disengaged[out] ==1 ))/length(out)))
print(paste('true negative % is: ', length(which(datatest$disengaged[-out] == 0))/(nrow(datatest) - length(out))))
print(Sys.time()  - begTime)


# plot(tlist[[5]])
# text(tlist[[5]])