plot(message.blast.20120201[1:k,], type='l', col='1', main='Blast Click Half-Life', xlab='minutes', ylab='clicks')
par(new=TRUE)
plot(message.blast.20120202[1:k,], type='l', col='2', xlab='', ylab='', axes=F)
par(new=TRUE)
plot(message.blast.20120131[1:k,], type='l', col='3', xlab='', ylab='', axes=F)
par(new=TRUE)
plot(message.blast.20120130[1:k,], type='l', col='4', xlab='', ylab='', axes=F)
par(new=TRUE)
plot(message.blast.20120129[1:k,], type='l', col='5', xlab='', ylab='', axes=F)
par(new=TRUE)
plot(message.blast.20120128[1:k,], type='l', col='6', xlab='', ylab='', axes=F)
par(new=TRUE)
plot(message.blast.20120127[1:k,], type='l', col='7', xlab='', ylab='', axes=F)
par(new=TRUE)
plot(message.blast.20120126[1:k,], type='l', col='8', xlab='', ylab='', axes=F)
par(new=TRUE)
plot(message.blast.20120125[1:k,], type='l', col='9', xlab='', ylab='', axes=F)


# for(i in 1:5000){
#   if(sum(message.blast.20120125[1:i, 2]) > sum(message.blast.20120125[, 2])/2 ){
#     print(i)
#     break}}
    