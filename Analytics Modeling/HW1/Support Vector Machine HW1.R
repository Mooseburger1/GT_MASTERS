require("kernlab")
require("caret")
data <- read.csv("credit_card_data-headers.csv", header = TRUE)
X <- as.matrix(data[,1:10])
y <- as.matrix(data[,11])

C = c(0.1, 1, 10, 50, 100, 500, 1000)

for(i in C){
model <- ksvm(x = X, y = y, type = "C-svc", kernel = "rbfdot",
              C = i, scaled = TRUE)

pred <- predict(model, X)


percentage <- sum(pred == y) / nrow(X)



a <- colSums(model@xmatrix[[1]] * model@coef[[1]])

a0 <- -model@b


cat("For C=", i, "\n")
print(confusionMatrix(table(pred, y), positive = "1"))
}