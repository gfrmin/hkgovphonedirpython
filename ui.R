library(shiny)
library(data.table)

shinyUI(
    fluidPage(
        titlePanel("Hong Kong Government Telephone Directory"),
        fluidRow(column(12,
                        dataTableOutput('teldir')
                        )
                 )
    )
)

        
