library("shiny")
library("plotly")
library("ggplot2")
library("reshape2")

p <- volcano %>%
  melt() %>% 
  ggplot(aes(Var1, Var2, fill = value)) + geom_tile()

p <- ggplotly(p)


# ~~~~~ UI ~~~~~ #
ui <- shinyUI(fluidPage(
  verbatimTextOutput("heatmap_hover"),
  verbatimTextOutput("heatmap_selected"),
  verbatimTextOutput("eventdata"),
  
  # Shiny
  fixedRow(
    column(6, plotlyOutput("volcano_plot", height = "400px"))
  )
))



# ~~~~~ SERVER ~~~~~ #
server <-  shinyServer(function(input, output,session) {
  
  # Heatmap
  output$volcano_plot <- renderPlotly({
    p %>% layout(dragmode = "select")
  })
  
  
  output$heatmap_hover <- renderPrint({
    d <- event_data("plotly_hover")
    if (is.null(d)) "Hover on a point!" else d
  })
  output$heatmap_selected <- renderPrint({
    # d <- event_data("plotly_selected")
    # if (is.null(d)) "Select some points!" else d
    event_data("plotly_selected")
  })
  output$eventdata <- renderPrint({
    str(event_data())
  })
  
})
shinyApp(ui = ui, server = server)