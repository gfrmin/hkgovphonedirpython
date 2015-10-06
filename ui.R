library(shiny)
library(data.table)

shinyUI(
    fluidPage(
        titlePanel("Hong Kong Government Telephone Directory"),
        downloadButton('downloadData', 'Download this data (.csv)'),
        fluidRow(column(12,
                        dataTableOutput('teldir')
                        )
                 )
    )
)

        
