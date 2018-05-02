install.packages("XML")
install.packages("frbs")

trainingData <- read.table("training_data2.txt")
colnames(trainingData) <- c("Front", "Left", "Right", "Back")

trainingDataY <- cbind(trainingData["Front"], trainingData["Back"])
outY <- trainingData["Back"] - trainingData["Front"]
trainY <- cbind(trainingDataY, outY)
trainY <- trainY / max(trainY)
#trainY <- frbs::norm.data(trainY, matrix(c(0, max(trainY), 0, max(trainY), 0, max(trainY[,3])), nrow = 2, ncol = 3))
colnames(trainY) <- c("First", "Second", "out")
#trainY[,3] <- trainY[,3] + 1

trainingDataX <- cbind(trainingData["Left"], trainingData["Right"])
outX <- trainingData["Right"] - trainingData["Left"]
trainX <- cbind(trainingDataX, outX)
trainX <- trainX / max(trainX)
#trainX <- frbs::norm.data(trainX, matrix(c(0, max(trainX), 0, max(trainX), 0, max(trainX[,3])), nrow = 2, ncol = 3))
colnames(trainX) <- c("First", "Second", "out")
#trainX[,3] <- trainX[,3] + 1

trainXY <- rbind(trainX, trainY)
#trainXY <- frbs::norm.data(trainXY, matrix(c(0, max(trainXY), 0, max(trainXY), 0, max(trainXY)), nrow = 2, ncol = 3))
#trainXY <- trainXY / max(trainXY)
#trainXY[,3] <- trainXY[,3] + 1

testData <- read.table("test_data.txt")
colnames(testData) <- c("Front", "Left", "Right", "Back")
testDataY <- testData[c("Front", "Back")]
testDataY <- testDataY / max(testDataY)
testDataX <- testData[c("Left", "Right")]
testDataX <- testDataX / max(testDataX)

dataRange <- matrix(c(0, 1, 0, 1, 0, 2), nrow = 2, ncol = 3)
anfisControl <- list(num.labels = 3, max.iter = 25, step.size = 0.01, type.snorm = "MAX",
                      type.tnorm = "MIN", type.implication.func = "ZADEH", name = "anfisY")
anfisObject <- frbs::frbs.learn(trainX, dataRange, "ANFIS", anfisControl)
summary(anfisObject)
summary(anfisObjectX)
testResultY = predict(anfisObject, testDataY)
testResultX = predict(anfisObject, testDataX)
frbs::plotMF(anfisObject)
frbs::write.frbsPMML(frbs::frbsPMML(anfisObject), "anfis")