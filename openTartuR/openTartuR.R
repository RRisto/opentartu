library(rvest)
url="http://www.tartu.ee/?page_id=1256&lang_id=1&menu_id=2&lotus_url=/webaktid.nsf/WebOtsused?OpenView&Start=1&Count=400&RestrictToCategory=Tartu_Linnavolikogu_8._koosseis_(alates_20.10.13)"

page=read_html(url)
pealkiri=page %>% 
  html_node("ul") %>%
  html_text()

pealkiri=page %>% 
  html_nodes("li") %>%
  html_text()

pealkiri

link=page %>%  #tuleb loopida sealt kus on child 3 edasi
  html_nodes("span.deftxt > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)") %>%
  html_text()
link

page %>% html_nodes("span.deftxt > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)") %>% html_attr("href")

lingid=c()
pealkiri=c()
for(i in 1:394) {
  selektor=paste0("span.deftxt > ul:nth-child(1) > li:nth-child(",i+2,
                  ") > a:nth-child(1)")
  pealkiri[i]=page %>%  #tuleb loopida sealt kus on child 3 edasi
    html_nodes(selektor) %>%
    html_text()
  
  lingid[i]=page %>% 
    html_nodes(selektor) %>% 
    html_attr("href")
  
  print(i)
}

#volikogu otsuste tabel
volikogu_otsused=data.frame(pealkiri, lingid)
write.table(volikogu_otsused, "volikoguOtsused.csv", sep=";", row.names = F)

#stenogrammid
url="http://www.tartu.ee/?page_id=3427&lang_id=1&menu_id=2&lotus_url=/webaktid.nsf/WebIstungiStenogrammid?OpenView&Start=1&Count=100&RestrictToCategory=Tartu_Linnavolikogu_8._koosseis_(alates_20.10.13)"
page=read_html(url)
link=page %>%  #tuleb loopida sealt kus on child 3 edasi
  html_nodes("#sisu .deftxt a") %>%
  html_attr("href")

#stenogrammi sisu
steno=c()
for(i in 1:3) {
  url=link[i]
  page=read_html(url)
  steno[i]=page %>%  #tuleb loopida sealt kus on child 3 edasi
    html_nodes("img , b:nth-child(1) font , ul , ul font , td~ td+ td") %>%
    html_text()
}


###########andmed sisse
data=read.csv("output2_minu.csv", sep=";")
write.table(data,"output2_minu.csv", sep=";", row.names = F)

####haldusjaotus
library(shapefiles)
dbf <- read.dbf("maakond_20161001.dbf")
maaamet=as.data.frame(dbf)


