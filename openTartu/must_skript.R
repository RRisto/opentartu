data=read.csv("output2_koordinaatidega.csv", sep=";")
summary(data)
data3=read.csv("output3_minu.csv", sep=";")

#dataAll=merge(data, data3, by.x="")

otsused=data3[,1:9]
eelnoud=data3[,10:21]
otsused$type="otsus"
eelnoud$type="eelnõu"
otsused$id=1:394
eelnoud$id=1:394
names(otsused)[7]="kuupäev"
names(eelnoud)[8]="kuupäev"

aktid=otsused[,c("type", "id", "kuupäev")]
aktid=rbind(aktid, eelnoud[,c("type", "id", "kuupäev")])

write.table(aktid, "aktid.csv", sep=";", row.names = F)
#nüüd paneme ka inimeste nimed juurde
aktid=rep(as.character(eelnoud$Koostaja),2)

for (i in 1:nrow(otsused)) {
#for (i in 1:3) {
  nimi=otsused$kuupäev[i]
  write.table(otsused$Pealkiri[i], paste0("./tekst/",i,"fail_",nimi,"_.txt"), 
              row.names=F)
  print(i)
}

