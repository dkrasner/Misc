hist(bi11$click_total, breaks=50, col='blue', xlim=range(0, 10000), xlab="Total Clicks", main="Total Clicks for Years 2010 vs 2011")
par(new=TRUE)
hist(bi10$click_total, breaks=25, col='red', xlim=range(0,10000), ylim=range(0,800),xlab='', main='', ylab='', axes=FALSE)
legend("center", c("2010", "2011"), col=c('red', 'blue'), lty=1:1)


par(mfrow=c(1,2))
hist(bi10$pv/bi10$count, breaks=20000, col='blue',  xlim = range(0,.8), xlab="Page View Rates", main="Page View Rates 2010")
hist(bi11$pv/bi11$count, breaks=1000, col='blue',  xlim = range(0,.8), xlab="Page View Rates", main="Page View Rates 2011")


hist(bi11$pv/bi11$count, breaks=1000, col='blue',  xlim = range(0,.8), xlab="Page View Rates", main="Page View Rates 2010 vs 2011")
par(new=TRUE)
hist(bi10$pv/bi10$count, breaks=20000, col='red',  xlim = range(0,.8), xlab="", main="", axes=FALSE)
legend("center", c("2010", "2011"), col=c('red', 'blue'), lty=1:1)