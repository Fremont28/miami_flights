mia=read.csv("mia_dest.csv")
mean(mia$percent) #0.019 
mia$set_col<-0.019
mia$plus_minus=mia$percent-mia$set_col
mia$plus_minus=round(mia$plus_minus,3)
mia$plus_minus=mia$plus_minus*100

ggplot(mia, aes(x=`DEST`, y=plus_minus, label=plus_minus)) + 
  geom_point(stat='identity', fill="black", size=6)  +
  geom_segment(aes(y = 0, 
                   x = `DEST`, 
                   yend = plus_minus, 
                   xend = `DEST`), 
               color = "black") +
  geom_text(color="white", size=2) +
  labs(title="It's Very Easy to Catch a Flight From Miami to Atlanta")+
  ylim(-2, 6) +
  coord_flip()+ylab("Plus-Minus Against Average Depature Rate (Miami Departures)")+
  xlab("Destination")+theme(plot.title = element_text(hjust = 0.5))
