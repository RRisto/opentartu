library(tm)

docs <- Corpus(DirSource("./tekst"))

#normaliseerimine, puhastamine
library(dplyr)
TextCleaner=.%>%
  #function to clean/transform corpus of docs; INPUT: docs - corpus of documents; OUTPUT: -corpus of cleaned/transformed documents
  tm_map(content_transformer(tolower))%>%
  tm_map(removeNumbers)%>%
  tm_map(removePunctuation)%>%
  #tm_map(removeWords, stopwords("english"))%>%
  tm_map(stripWhitespace)%>%
  #tm_map(stemDocument)%>%
  tm_map(content_transformer(function(x,pattern)gsub("ā€™|ā€“"," ", x)))%>%
  tm_map(removeWords, c("ja","või","ning", "tartu", "linna"))

docs=TextCleaner(docs)
dtm <- DocumentTermMatrix(docs)
#model
library(corpustools) 
set.seed(1)  
#Hitler
lda = lda.fit(dtm, K=3, alpha=.3)
#run it once, helps to make separate folder for vis to upload it to the web
# invisible(lapply(
#   file.path("https://raw.githubusercontent.com/trinker/topicmodels_learning/master/functions",
#             c("topicmodels2LDAvis.R", "optimal_k.R")),devtools::source_url))
#interactive visualization
library(LDAvis)
lda %>%
  topicmodels2LDAvis() %>%
  LDAvis::serVis(out.dir = './visualisations/ldavis', open.browser = F)


topics=c("Detailplaneering","loa andmine","linnavolikogu")
#plotime ajalise jagunemise
library(reshape2) 
library(ggplot2)

ldaTime=lda%>% ##calculate each topic median in each year and plot it
  topicmodels::posterior()%>% #get posterior probabilities
  with(topics)%>% #select list element topics
  as.data.frame(na.rm=T)%>% #turn into df
  `colnames<-`(topics)%>% #add topics names
  cbind(year=gsub("^[0-9]*fail_|_\\.txt","", names(docs)))%>% #add the year
  melt()

ldaTime$year=as.character(as.factor(ldaTime$year))
ldaTime$year2=gsub( "^[0-9]{2}\\.","",ldaTime$year)
  
ldaTime2=ldaTime%>% #turn into long format
  group_by(year2, variable)%>% #group by year and topic
  summarise(median=median(value))%>%
  `colnames<-`(c("aasta", "teema","mediaan"))
  
p=ggplot(ldaTime2, aes(x=aasta, y=mediaan, colour=teema, group=teema))+ #plot it
  geom_line(size=1)+
  theme_minimal()+
  theme(axis.text.x = element_text(angle=90))+
  xlab("Aasta")+
  ylab("Teema populaarsus") 

library(plotly) 
ggplotly(p) 

plotly_POST(p)