for(c_id in c(764, 766)){
  
  
  #var_pv <- make.names(paste('pv', c_id, sep=''))
  #pv <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id,"_pv_trends.txt", sep=''), header=F)
  
  purch <- read.csv(paste("~/Desktop/Data Projects/ST/data/trends/", c_id, "_purch_trends.txt", sep=''), header=F)
  open <- read.csv(paste("~/Desktop/Data Projects/ST/data/trends/", c_id, "_open_trends.txt", sep=''), header=F)
  click <- read.csv(paste("~/Desktop/Data Projects/ST/data/trends/", c_id, "_click_trends.txt", sep=''), header=F)
  
  var_p <- make.names(paste('c_hist', c_id, sep=''))
  var_o <- make.names(paste('o_hist', c_id, sep=''))
  var_c <- make.names(paste('p_hist', c_id, sep=''))
  #var_pv <- make.names(paste('pv_hist', c_id, sep=''))
  
  c_hist = hist(click[which(click[,2] >= 0), 2], breaks = length(unique(click[which(click[,2] >= 0), 2])), main='clicks')
  o_hist = hist(open[which(open[,2] >= 0), 2], breaks = length(unique(open[which(open[,2] >= 0), 2])), main = 'open')
  p_hist = hist(purch[which(purch[,2] >= 0), 2], breaks = length(unique(purch[which(purch[,2] >= 0), 2])), main = 'purchases')
  #pv_hist = hist(pv[which(pv[,2] >= 0), 2], breaks = length(unique(pv[which(pv[,2] >= 0), 2])), main = 'pv')
  
  assign(var_p, p_hist)
  assign(var_o, o_hist)
  assign(var_c, c_hist)
  #assign(var_pv, pv_hist)
  
  c_hist_mean <- mean(c_hist$counts[which(is.na(c_hist$counts)==FALSE)])
  o_hist_mean <- mean(o_hist$counts[which(is.na(o_hist$counts)==FALSE)])
  p_hist_mean <- mean(p_hist$counts[which(is.na(p_hist$counts)==FALSE)])
  #pv_hist_mean <- mean(pv_hist$counts[which(is.na(pv_hist$counts)==FALSE)])
  
  c_plot <- (c_hist$counts - c_hist_mean)/sd(c_hist$counts[which(is.na(c_hist$counts)==FALSE)])
  o_plot <- (o_hist$counts - o_hist_mean)/sd(o_hist$counts[which(is.na(o_hist$counts)==FALSE)])
  p_plot <- (p_hist$counts - p_hist_mean)/sd(p_hist$counts[which(is.na(p_hist$counts)==FALSE)])
  #pv_plot <- (pv_hist$counts - pv_hist_mean)/sd(pv_hist$counts[which(is.na(pv_hist$counts)==FALSE)])
  
  var_p <- make.names(paste('p_plot', c_id, sep=''))
  var_o <- make.names(paste('o_plot', c_id, sep=''))
  var_c <- make.names(paste('c_plot', c_id, sep=''))
  #var_pv <- make.names(paste('pv_plot', c_id, sep=''))
  
  assign(var_p, p_plot)
  assign(var_o, o_plot)
  assign(var_c, c_plot)
  #assign(var_pv, pv_plot)
  
  
}

p_plot <- (p_plot764[0:250] + p_plot766[0:250] + p_plot1600[0:250])/3
c_plot <- (c_plot764[0:250] + c_plot766[0:250] + c_plot1600[0:250])/3
o_plot <- (o_plot764[0:250] + o_plot766[0:250] + o_plot1600[0:250])/3

par(bg='white')
par(lwd='2')
par(font=6, font.axis=2)
plot(c_plot, xlab='Days', yaxt='n', ylab = '',  type='l', col='green')
#plot(c_plot, xlab='Days', yaxt='n', ylab = '', type='l', col='green')

par(new=TRUE)
plot(o_plot, axes=FALSE, ylab = '', xlab='', type='l', col='blue')
par(new=TRUE)
plot(p_plot, axes=FALSE, ylab = '', xlab='', type='l', col='red')
#par(new=TRUE)
#plot(0:23*30, pv_hist$counts[1:24], xlim=range(0, 250), axes=FALSE, ylab = '', xlab='', type='l', col='purple')
legend("topright", c("clicks", "opens",  "purchases"), col=c('green', 'blue', 'red'), lty=1:1, box.lwd=0)


#############PV################
for(c_id in c(1623, 864, 828)){
  
  
  var_pv <- make.names(paste('pv', c_id, sep=''))

  pv <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id,"_pv_trends.txt", sep=''), header=F)

  var_pv <- make.names(paste('pv_hist', c_id, sep=''))
  
  pv_use = round(pv[which(pv[,2] >= 0), 2]/30)
  
  pv_hist = hist(pv_use, breaks = length(unique(pv_use)), main = 'pv')

  assign(var_pv, pv_hist)
  
  pv_hist_mean <- mean(pv_hist$counts[which(is.na(pv_hist$counts)==FALSE)])
  
  pv_plot <- (pv_hist$counts - pv_hist_mean)/sd(pv_hist$counts[which(is.na(pv_hist$counts)==FALSE)])
  
  var_pv <- make.names(paste('pv_plot', c_id, sep=''))
  
  assign(var_pv, pv_plot)
  
  
}

pv_plot <- (pv_plot766[0:8] + pv_plot1600[0:8] + pv_plot450[0:8] + pv_plot1623[0:8] + pv_plot864[0:8] + pv_plot828[0:8])/6

par(bg='white')
par(lwd='2')
par(font=6, font.axis=2)


plot(pv_plot, xlab='Months', yaxt='n', ylab = '', type='l', col='purple')
legend("topright", c("pageviews"), col=c('purple'), lty=1:1, box.lwd=0)

#######################################

# par(bg='white')
# par(lwd='2')
# par(font=6, font.axis=2)
# #plot(c_hist$counts[0:250], xlab='Days', yaxt='n', ylab = '',main=paste(c_id, ' Trends', sep=''), type='l', col='green')
# plot(c_hist$counts[0:220], xlab='Days', yaxt='n', ylab = '', type='l', col='green')
# 
# par(new=TRUE)
# plot(o_hist$counts[0:220], axes=FALSE, ylab = '', xlab='', type='l', col='blue')
# par(new=TRUE)
# plot(p_hist$counts[0:220], axes=FALSE, ylab = '', xlab='', type='l', col='red')
# #par(new=TRUE)
# #plot(0:23*30, pv_hist$counts[1:24], xlim=range(0, 250), axes=FALSE, ylab = '', xlab='', type='l', col='purple')
# legend("topright", c("clicks", "opens",  "purchases"), col=c('green', 'blue', 'red'), lty=1:1, box.lwd=0)
# 
# #legend("topright", c("clicks", "opens", "purchases", "pageviews"), col=c('green', 'blue', 'red', 'purple'), lty=1:1, box.lwd=0)
# 
# 

#######################
# c_id = 764
# #pv <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id,"_pv_trends.txt", sep=''), header=F)
# purch1 <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id, "_purch_trends.txt", sep=''), header=F)
# open1 <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id, "_open_trends.txt", sep=''), header=F)
# click1 <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id, "_click_trends.txt", sep=''), header=F)
# 
# c_hist1 = hist(click[which(click1[,2] >= 0), 2], breaks = length(unique(click1[which(click1[,2] >= 0), 2])), main='clicks')
# o_hist1 = hist(open[which(open1[,2] >= 0), 2], breaks = length(unique(open1[which(open1[,2] >= 0), 2])), main = 'open')
# p_hist1 = hist(purch[which(purch1[,2] >= 0), 2], breaks = length(unique(purch1[which(purch1[,2] >= 0), 2])), main = 'purchases')
# #pv_use = round(pv[which(pv[,2] >= 0), 2]/30)
# #pv_hist = hist(pv_use, breaks = length(unique(pv_use)), main = 'pv')
# 
# c_id = 1600
# #pv <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id,"_pv_trends.txt", sep=''), header=F)
# purch2 <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id, "_purch_trends.txt", sep=''), header=F)
# open2 <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id, "_open_trends.txt", sep=''), header=F)
# click2 <- read.csv(paste("~/Desktop/Data Projects/ST/data/", c_id, "_click_trends.txt", sep=''), header=F)
# 
# c_hist2 = hist(click[which(click2[,2] >= 0), 2], breaks = length(unique(click2[which(click2[,2] >= 0), 2])), main='clicks')
# o_hist2 = hist(open[which(open2[,2] >= 0), 2], breaks = length(unique(open2[which(open2[,2] >= 0), 2])), main = 'open')
# p_hist2 = hist(purch[which(purch2[,2] >= 0), 2], breaks = length(unique(purch2[which(purch2[,2] >= 0), 2])), main = 'purchases')
# 
# 
# c_hist$counts[0:250] = (c_hist$counts[0:250] + c_hist1$counts[0:250] + c_hist2$counts[0:250])/3
# o_hist$counts[0:250] = (o_hist$counts[0:250] + o_hist1$counts[0:250] + o_hist2$counts[0:250])/3
# p_hist$counts[0:250] = (p_hist$counts[0:250] + p_hist1$counts[0:250] + p_hist2$counts[0:250])/3