require("kknn")

data = read.csv("credit_card_data-headers.csv", header = TRUE)

accuracy_percentage <- rep(0,20)
for(j in 1:20){
      pred = rep(0, nrow(data))
      for(i in 1:nrow(data)){
        
            model <- kknn(R1~., data[-i,], data[i,], k = j, scale = TRUE)
            pred[i] <- round(fitted(model))
      
      }
      
      acc <- sum(pred == as.vector(data[,11])) / nrow(data)
      accuracy_percentage[j] = acc
      cat("Finished trying model with", j, "nearest neightbors","\n")
}

cat("\n\nBest performing model is model", which.max(accuracy_percentage),"with an accuracy score of", max(accuracy_percentage))
plot(accuracy_percentage, main = "KNN Accuracy", xlab = "K Nearest Neighbors", ylab = "Accuracy", col = "blue", pch=20, cex = 2, axes = FALSE)
axis(1, seq(1,20,1), col = NA, col.ticks = 1)
axis(2, seq(0.80, 0.87, 0.005), col = NA, col.ticks = 1, las=2)
abline(h=seq(0.80, 0.87, 0.005),lty=2,col="black")
