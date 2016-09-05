# http://www.thecalculatorsite.com/articles/finance/compound-interest-formula.php

# # the principal investment amount (the initial deposit or loan amount)
# Principal<-5000
# 
# # the annual interest rate (decimal) ; 5/100 = 5% or 0.05
# rate<-5/100
# 
# # the number of times that interest is compounded per year ; 365 = daily, 12 = monthly, 52 = weekly
# num_periods<-12 
# 
# # the number of years the money is invested or borrowed for ; 1 = 1 year
# time_invested<-1
# 
# # Annual Compound Interest Formula:A = P(1+r/n)^nt
# AmountTotal<-Principal*((1+rate/num_periods)^(num_periods*time_invested))
# AmountTotal


# custom function
myInvestment <- function(principal,rate,num_periods,years_invested) {
  total_value<-principal*((1+rate/num_periods)^(num_periods*years_invested))
  return(total_value)
}

myInvestment(principal = 5000,rate = 5/100,num_periods = 12,years_invested = 1)
# [1] 5255.809

Dollars<-sapply(seq(from=1000,to=10000,by=1000), function(x) myInvestment(principal = x,rate = 5/100,num_periods = 12,years_invested = 1))
#  [1]  1051.162  2102.324  3153.486  4204.648  5255.809  6306.971  7358.133  8409.295  9460.457 10511.619
plot(Dollars)
