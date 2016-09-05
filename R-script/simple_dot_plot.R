# create a simple plot to show the relationship between different formulas on a sequence of values
# this was created to try to model different ways to automatically adjust par(mar) values based on the
# number of characters (nchar) in sample names
NChar_Nums<-seq(1:100)
Mar_Nums_1x5<-sapply(X = NChar_Nums,FUN = function(x) max(4.1,x/1.5))
Mar_Nums_2x0<-sapply(X = NChar_Nums,FUN = function(x) max(4.1,x/2))
Mar_Nums_2x5<-sapply(X = NChar_Nums,FUN = function(x) max(4.1,x/2.5))
Mar_Nums_3x0<-sapply(X = NChar_Nums,FUN = function(x) max(4.1,x/3))

tmp_colors<-rainbow(5)

# plot(c(NChar_Nums,Mar_Nums),main = "nchar vs. mar",col=c("red","blue"))
plot(NChar_Nums,
     main=c("nchar() length vs. mar value"),
     col=tmp_colors[1],
     xlab="Index",
     ylab="Value")
points(Mar_Nums_1x5,
       col=tmp_colors[2])
points(Mar_Nums_2x0,
       col=tmp_colors[3])
points(Mar_Nums_2x5,
       col=tmp_colors[4])
points(Mar_Nums_3x0,
       col=tmp_colors[5])
legend("topleft",
       legend=c("nchar","Mar_Nums_1x5","Mar_Nums_2x0","Mar_Nums_2x5","Mar_Nums_3x0"),fill=tmp_colors,bty = "n")
