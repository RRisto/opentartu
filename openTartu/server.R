
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

shinyServer(function(input, output) {

  output$frame <- renderUI({
    #töötav link#https://fusiontables.googleusercontent.com/embedviz?q=select+col11+from+1Rr0ZL5zj0YsYZVvgNnGZMhfH0XvcEybFUX9VviGk&viz=MAP&h=false&lat=58.394272076384816&lng=26.73053584013678&t=1&z=12&l=col11&y=2&tmplt=2&hml=TWO_COL_LAT_LNG
    
    my_test <- tags$iframe(src="https://fusiontables.google.com/embedviz?q=select+col11+from+1cTaywdO73-Q8kURMoC-hZjC94DSyZyxg2XqI9MBy&viz=MAP&h=false&lat=58.374165291714334&lng=26.722027873141556&t=1&z=12&l=col11&y=2&tmplt=2&hml=TWO_COL_LAT_LNG",
                           height=600, width=535)
    print(my_test)
    my_test

  })

})
