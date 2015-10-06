library(shiny)
library(data.table)

teldir <- fread("teldir.csv")
setnames(teldir, c("Department", "Title", "Email", "Name", "Telephone number"))

shinyServer(function(input, output) {
    output$teldir <- renderDataTable({
        teldir
    })

    output$downloadData <- downloadHandler(
        filename = "teldir.csv",
        content = function(file) {
            write.csv(teldir, file)
        }
    )
})
