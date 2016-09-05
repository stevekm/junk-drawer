# http://stackoverflow.com/questions/3789968/generate-a-list-of-primes-in-r-up-to-a-certain-number
primest <- function(n){
  p <- 2:n
  i <- 1
  while (p[i] <= sqrt(n)) {
    p <-  p[p %% p[i] != 0 | p==p[i]]
    i <- i+1
  }
  p
}
x<-primest(1e4)
hist(x)

tapply( x, (seq_along(x)-1) %/% 1, sum)

tapply( x, (seq_along(x)-1) %/% 1, diff)

# http://stackoverflow.com/questions/6262203/measuring-function-execution-time-in-r
# install.packages("microbenchmark")
# library(microbenchmark)
# 
# res<-microbenchmark(primest(1e5),times = 100,unit = "ms")
# 
# 
# # Plot results:
# boxplot(res)
# ## Pretty plot:
# if (require("ggplot2")) {
#   autoplot(res)
# }
# save.image()
