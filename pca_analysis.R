# Load necessary libraries
install.packages("dplyr")
install.packages("car")
install.packages("FactoMineR")
install.packages("factoextra")
library(dplyr)
library(car)
library(FactoMineR)
library(factoextra)

# Read your data
my_data <- read.csv("C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/perfomance_centrality_dataset_z_score.csv", head=TRUE)
my_data <- my_data %>% select(-Swipes)
print(my_data)
set.seed(992228)
my_data <- sample_n(my_data, nrow(my_data))
print(my_data)

# Standardize the data (excluding the response variable)
data_standardized <- (my_data[, -which(names(my_data) == "Student.Achievement")])

summary(data_standardized)
print(data_standardized)
# Perform PCA
my_data.pca <- prcomp(data_standardized)

print(my_data.pca)

# Examine the PCA result
summary(my_data.pca)

loadings<- my_data.pca$rotation[, 1:4]
print(loadings)
cor(my_data)

#biplot(my_data.pca, scale = 0)

eig.val <- get_eigenvalue(my_data.pca)
eig.val

# Visualize PCA
fviz_pca_var(my_data.pca, col.var = "black")
fviz_cos2(my_data.pca, choice = "var", axes = 1:2)
biplot(my_data.pca, cex=0.4)
fviz_eig(my_data.pca, addlabels = TRUE)

cum_var_exp <- cumsum(eig.val$variance.percent)
print(cum_var_exp)
num_components <- 2
print(num_components)

# Create a new dataset with the retained principal components
principal_components <- as.data.frame(my_data.pca$x[, 1:num_components])
principal_components$Student.Achievement <- my_data$Student.Achievement

print(data_standardized)
print(principal_components)

combined_data <- cbind(data_standardized, principal_components)
print(combined_data)
# Split the data into training and test sets
n <- nrow(combined_data)
train_indices <- sample(1:n, size = 0.7 * n)
train_set <- combined_data[train_indices, ]
print(train_set)
test_set <- combined_data[-train_indices, ]
print(test_set)

# Build a linear model using the principal components
lm_pca <- lm(Student.Achievement ~ ., data = train_set)
summary(lm_pca)

# Predict on the test set
test_set$pred <- predict(lm_pca, test_set)

# Evaluate the model
mean_absolute_percentage_error <- mean(abs((test_set$Student.Achievement - test_set$pred) / test_set$Student.Achievement)) * 100
mean_absolute_percentage_error

# Plot actual vs predicted values
my_x <- seq(1, nrow(test_set))
plot(my_x, test_set$Student.Achievement, col = "blue", cex = 0.3, ylab = "Student Achievement", xlab = "Index")
lines(my_x, test_set$Student.Achievement, col = "blue")
points(my_x, test_set$pred, col = "red", cex = 0.3, pch = 2)
lines(my_x, test_set$pred, col = "red")

# Check assumptions of the linear model using PCA components
# Homoskedasticity: Breusch-Pagan test
library(lmtest)
bptest(lm_pca)

cor(combined_data)
# Independence: Durbin-Watson test
dwtest(lm_pca)

# Normality: Shapiro-Wilk test
shapiro.test(lm_pca$residuals)

vif(lm_pca)

