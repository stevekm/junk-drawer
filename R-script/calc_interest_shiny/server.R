library(shiny)

shinyServer(function(input, output) {
  
  myInvestment <- function(my_principal,my_rate,num_periods,my_years_invested) {
    total_value<-my_principal*((1+my_rate/num_periods)^(num_periods*my_years_invested))
    return(total_value)
  }
  output$ratePlot <- renderPlot({
    rate <- input$rate
    Principal<-input$Principal
    years<-input$years
    periods<-input$periods
    Dollars<-sapply(Principal, function(x) myInvestment(my_principal = x,my_rate = rate,num_periods = periods,my_years_invested = years))
    
    Dollar_Years<-seq(from=1,to=years,by=1)
    Dollar_Years<-sapply(Dollar_Years, function(x) myInvestment(my_principal = Principal,my_rate = rate,num_periods = periods,my_years_invested = x))
    
    plot(Dollar_Years,main = paste0("$",round(Dollars,digits = 2)," Final Value"),ylab = "Dollars",xlab = "Years",col="darkgreen",pch=20)
  })
  
})
