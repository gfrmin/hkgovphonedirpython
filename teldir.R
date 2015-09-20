library(jsonlite)
library(data.table)
library(stringr)
library(tidyr)

teldir <- data.table(fromJSON("teldir.json"))
teldir[,department := str_replace_all(department, c("\r" = "", "\n" = "", "[ ]+" = " "))]
teldir[,department := str_replace_all(department, c("<h1>" = "", "</h1>" = "", "<br><br>" = "<br>", "<br>$" = "", "&amp;" = ""))]
teldirdeps <- str_split(teldir$department, "<br>")
teldirdeps <- sapply(sapply(teldirdeps, unique), str_c, collapse="<br>")
teldir[,department := teldirdeps]
teldir[,department := str_replace_all(department, c("<br>" = " - "))]
teldir[,title := str_replace_all(title, c("<(.*?)>" = "", "&amp;" = ""))]
teldir[,name := str_replace_all(name, "<(.*?)>", "")]
teldir[,tel := str_replace(tel, "<td(.*?)>", "")]
teldir[,tel := str_replace(tel, "</td(.*?)>", "")]
teldir[,tel := str_replace(tel, "<br>$", "")]
teldirtels <- data.table(str_split_fixed(teldir$tel, "<br>", 4))
setnames(teldirtels, c("tel1", "tel2", "tel3", "tel4"))
teldir <- cbind(teldir, teldirtels)
teldir[,tel := NULL]
teldiremails <- str_match(teldir$email, "var email = '(.*?)';var domain = '(.*?)'")
teldiremails <- str_c(teldiremails[,2], teldiremails[,3], sep="@")
teldir[,email := teldiremails]
teldir <- teldir %>% gather(teltype, tel, tel1:tel4) %>% data.table
#teldir <- teldir %>% gather(deptype, subdep, dep1:dep9) %>% data.table
                                        #teldir[,`:=`(deptype = NULL, teltype = NULL)]
teldir[,teltype := NULL]
teldir <- unique(teldir)
teldir <- teldir[,ifelse(length(tel) == 1, tel, tel[-which(tel == "")]), by="department,title,email,name"]
setnames(teldir, "V1", "tel")

write.csv(teldir, file = "teldir.csv", row.names = FALSE)

