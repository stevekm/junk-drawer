library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Calculate investment value! :)"),
  
  # Sidebar with a slider input 
  sidebarLayout(
    sidebarPanel(
      sliderInput("rate",
                  "Interest rate:",
                  min = 0.01,
                  max = 0.1,
                  value = 0.05,
                  step=0.01),
      sliderInput("Principal",
                  "Principal Amount invested",
                  min = 100,
                  max = 10000,
                  value = 5000,
                  step=100),
      sliderInput("years",
                  "Years Invested",
                  min = 1,
                  max = 100,
                  value = 5,
                  step=1),
      sliderInput("periods",
                  "Number of times interest is compounded per year (12 = monthly, 365 = daily)",
                  min = 1,
                  max = 365,
                  value = 12,
                  step=1)
    ),
    
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("ratePlot")
    )
  )
))

# to run the Shiny, use these commands on the R console:
# library(shiny)
# runApp("~/R-scripts/calc_interest_shiny/")