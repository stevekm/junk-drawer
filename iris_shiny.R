library("shiny")
library("plotly")
library("ggplot2")

species_choices <- setNames(levels(iris[["Species"]]), levels(iris[["Species"]]))

ui <- fluidPage(
  headerPanel('Iris plot'),
  mainPanel(
    plotlyOutput("plot")),
  sidebarPanel(selectInput(inputId = "species", 
                           label = "Choose a species of Iris:", 
                           choices = species_choices, 
                           selected = species_choices[1])),
  textOutput("result")

)


server <- shinyServer(function(input, output, session){
  selectedData <- reactive({
    iris[which(iris[["Species"]] == input$species), ]
  })
  
  output$result <- renderText({
    paste("You chose", input$species)
  })
  
  output$plot <- renderPlotly({
    ggplot(data = selectedData(), aes(x = Sepal.Length, y = Petal.Length)) + geom_point() + ggtitle(sprintf("Species: %s", input$species))
  })
  
})

shinyApp(ui = ui, server = server)

