library(dplyr)
library(car)

my_data = read.csv("C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/perfomance_centrality_dataset_withswipes.csv",head=TRUE)
head(my_data)

my_data = sample_n(my_data, nrow(my_data))
head(my_data)

my_data = my_data[,c("Closeness", "Betweenness", "Eigenvector", "Swipes", "Rigorous.Instruction")]

# Next Steps :
cor(my_data)
# 0. Add any additional columns you feel can help
# 1. Look at the correlation Matrix 
# 2. Look at vif 
# 3. Take a decision on dropping some columns
# 4. Linear models

lm1 = lm(Rigorous.Instruction ~  Closeness + Betweenness + Eigenvector +Swipes , data = my_data)
vif(lm1)
summary(lm1)

my_nrows = nrow(my_data)
train_rows_num = .7*my_nrows
test_rows_num = my_nrows-train_rows_num
my_training_set = my_data[(1:train_rows_num),]
my_test_set = my_data[((train_rows_num+1):my_nrows),]

lm2 = lm(Rigorous.Instruction ~ Closeness + Betweenness +Eigenvector+Swipes , my_training_set)
summary(lm2)

my_test_set$pred = predict(lm2, my_test_set)

my_x = seq(1, nrow(my_test_set))

plot(my_x, my_test_set$Rigorous.Instruction, col = "blue", cex = 0.3)
lines(my_x, my_test_set$Rigorous.Instruction, col = "blue")
points(my_x, my_test_set$pred, col = "red", cex=0.3, pch = 2)
lines(my_x, my_test_set$pred, col = "red")

my_test_set$error = my_test_set$Rigorous.Instruction - my_test_set$pred 
my_test_set$abs_error = abs(my_test_set$Rigorous.Instruction - my_test_set$pred)
my_test_set$abs_pct_error = ((my_test_set$abs_error)/(my_test_set$.Rigorous.Instruction))*100.0
mean(my_test_set$abs_pct_error)

my_lm2_residuals = as.numeric(lm2$residuals)

qqnorm(my_lm2_residuals)
# Plot the Q-Q line
qqline(my_lm2_residuals)

# V I N 0 

# Assumption: Variance of the Residuals is Constant i.e. Homoskedasticity

# Breusch Pagan Test

# H0: The variance of the Residuals is Constant
# Ha: The variance of the Residuals is NOT constant

library(lmtest)
bptest(lm2)
# p-value = 0.09742
# p-value = 0.09742 WHICH IS NOT less than 0.05
# WE DO NOT REJECT H0
# => WE HAVE EVIDENCE TO SUPPORT H0
# i.e. The variance of the Residuals is Constant and we can say this with 95% Confidence!

# Assumption: the Residuals are Independent

# Durbin Watson test

# H0: The residuals are independent
# Ha: The residuals are NOT independent

dwtest(lm2)

# p-value = 0.005229 WHICH IS less than 0.05
# WE REJECT H0
# => We have evidence to support Ha
# i.e. The residuals are NOT independent and we can say this with 95% Confidence!

# Assumption: the Residuals are Normally Distributed

# 1: Shapiro Wilk Test
# 2: Anderson Darling Test

# H0: The residuals are normally distributed
# Ha: The residuals are NOT normally distributed

library(nortest)
shapiro.test(lm2$residuals)

# The p-value is 0.4065 which is greater than 0.05 so we DO NO Reject H0
# therefore, we can say with 95% Confidence that the residuals are Normally Distributed 

ad.test(lm2$residuals)

# 0 i.e. The Mean of the residuals should be 0

mean(lm2$residuals)

# -8.196913e-18

# we can say that 10^{-18} is pretty close to 0

#### Multicollinearity
library(car)
vif(lm2)









