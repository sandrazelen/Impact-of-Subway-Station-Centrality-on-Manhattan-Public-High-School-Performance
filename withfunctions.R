# Load necessary libraries
install.packages("dplyr")
install.packages("car")
install.packages("FactoMineR")
install.packages("factoextra")
install.packages("janitor")
library(dplyr)
library(car)
library(FactoMineR)
library(factoextra)
library(janitor)

my_data <-read.csv("C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/z_score_stationnames.csv", head=TRUE)
set.seed(9922)
my_data <- sample_n(my_data, nrow(my_data))
print(my_data)
station <- data.frame(Node = my_data$Node)
columns_to_delete <-c("Node", "Swipes")

#columns_to_delete <- c("Node", "Rigorous.Instruction", "Collaborative.Teachers", "Supportive.Environment", "Effective.School.Leadership", "Strong.Family.Community.Ties", "Trust")

my_data <- my_data[, -which(names(my_data) %in% columns_to_delete)]
print(my_data)

#dependent <- data.frame(Student.Achievement = my_data$Student.Achievement)
#print(dependent)

data_standardized <-my_data

run_pca <- function(data, num_components = 2, seed = 123) {
  set.seed(seed)
  data_standardized <- data
  
  print(summary(data_standardized))
  print(data_standardized)
  
  pca_result <- prcomp(data_standardized)
  print(pca_result)
  
  print(summary(pca_result))
  
  loadings <- pca_result$rotation[, 1:num_components]
  print(loadings)
  
  # Get eigenvalues
  eig.val <- get_eigenvalue(pca_result)
  print(eig.val)
  
  #Visualize
  fviz_pca_var(pca_result, col.var = "black")
  fviz_cos2(pca_result, choice = "var", axes = 1:2)
  biplot(pca_result, cex = 0.4)
  fviz_eig(pca_result, addlabels = TRUE)
  fviz_pca_var(pca_result,
               col.var = "cos2", # Color by the quality of representation
               gradient.cols = c("darkorchid4", "gold", "darkorange"),
               repel = TRUE
  )
  
  cum_var_exp <- cumsum(eig.val$variance.percent)
  print(cum_var_exp)
  print(num_components)
  
  pcs <- as.matrix(data_standardized) %*% as.matrix(loadings)
  colnames(pcs) <- paste0("PC", 1:num_components)
  print(pcs)
  
  results <- list(
    pca_result = pca_result,
    loadings = loadings,
    eig_values = eig.val,
    cumulative_variance_explained = cum_var_exp,
    principal_components = pcs
  )
  return(results)
}

pca_results<- run_pca(data_standardized, num_components = 2, seed = 123)

pca_result <- pca_results$pca_result
loadings <- pca_results$loadings
eig_values <- pca_results$eig_values
cumulative_variance_explained <- pca_results$cumulative_variance_explained
pcs <- pca_results$principal_components

fviz_pca_var(pca_result,
             col.var = "cos2", # Color by the quality of representation
             gradient.cols = c("darkorchid4", "gold", "darkorange"),
             repel = TRUE
)

#combined_data <- as.data.frame(cbind(my_data, pcs))
#combined_data <- as.data.frame(cbind(combined_data, dependent))

#combined_data <- as.data.frame(cbind(principal_components, dependent))
#combined_data <- as.data.frame(cbind(pcs, dependent))

combined_data <- pcs

print(combined_data)
# Split the data into training and test sets
n <- nrow(combined_data)
train_indices <- sample(1:n, size = 0.7 * n)
train_set <- combined_data[train_indices, ]
print(train_set)
test_set <- combined_data[-train_indices, ]
print(test_set)

linear_reg <- function(train_set, test_set, Predictor) {
  train_set<-as.data.frame(train_set)
  test_set<-as.data.frame(test_set)
  lm_pca <- lm(Student.Achievement ~ ., data = train_set)
  summary_lm <- summary(lm_pca)
  
  test_set$pred <- predict(lm_pca, test_set)
  
  mean_absolute_percentage_error <- mean(abs((test_set$Predictor - test_set$pred) / test_set$Predictor)) * 100
  
  my_x <- seq(1, nrow(test_set))
  plot(my_x, test_set$Student.Achievement, col = "blue", cex = 0.3, ylab = Predictor, xlab = "Index")
  lines(my_x, test_set$Student.Achievement, col = "blue")
  points(my_x, test_set$pred, col = "red", cex = 0.3, pch = 2)
  lines(my_x, test_set$pred, col = "red")
  
  # Check assumptions of the linear model using PCA components
  # Homoskedasticity: Breusch-Pagan test
  bp_test <- bptest(lm_pca)
  
  # Independence: Durbin-Watson test
  dw_test <- dwtest(lm_pca)
  
  # Normality: Shapiro-Wilk test
  shapiro_test <- shapiro.test(lm_pca$residuals)
  
  # Variance Inflation Factor
  vif_values <- vif(lm_pca)
  
  results <- list(
    model_summary = summary_lm,
    mean_absolute_percentage_error = mean_absolute_percentage_error,
    bp_test = bp_test,
    dw_test = dw_test,
    shapiro_test = shapiro_test,
    vif_values = vif_values
  )
  return(results)
}
output <- linear_reg(train_set, test_set, PC2)
print(output)


cor(combined_data)
combined_data <- cbind(combined_data, station)
print(my_data)

print(combined_data)
print(my_data)

data_for_clustering <- my_data[, c('Node', 'Closeness', 'Trust')]

# Print to verify data selection
print(data_for_clustering[,1:3])

fviz_nbclust(data_for_clustering[,2:3], kmeans, method = "wss")

# Apply k-means clustering with the chosen number of clusters (e.g., 3 clusters)
set.seed(123)
kmeans_result <- kmeans(data_for_clustering[, 2:3], centers = 4, nstart = 25)
data_for_clustering$Cluster <- factor(kmeans_result$cluster)

fviz_cluster(kmeans_result, data = data_for_clustering[,2:3])
cluster_plot <- fviz_cluster(kmeans_result, data = data_for_clustering[,2:3])

print(data_for_clustering)

# Add text labels for "Node"
cluster_plot + 
  geom_text(aes(x = data_for_clustering[, 2], y = data_for_clustering[, 3], label = data_for_clustering$Node), vjust = -0.2, hjust = 0.2, check_overlap = TRUE) +
  labs(title = "K-means Clustering with Node Labels") +
  theme_minimal()

ggplot(data_for_clustering, aes(x = Closeness, y = Trust, color = Cluster, label = Node)) +
  geom_point(size = 4, alpha = 0.8, shape = 19) +
  geom_text(vjust = -1, hjust = 1, check_overlap = TRUE) +
  scale_color_manual(name = "Cluster", values = c("red", "green", "blue", "purple")) +
  labs(x = "Station Centrality", y = "Performance Metric", title = "K-means Clustering") +
  theme_minimal()

print(combined_data)
ggplot(combined_data, aes(x = PC1, y = PC2, color = Student.Achievement)) +
  geom_point(size = 4, alpha = 0.8, shape = 19) +
  geom_smooth(method = "lm", se = FALSE, color = "black", linetype = "dashed") +
  geom_text(aes(label = Node), vjust = -1, hjust = 1, check_overlap = TRUE) +  # Add check_overlap to prevent label overlap
  scale_color_continuous(name = "Student Achievement") +  
  labs(x = "PC1", y = "PC2", title = "Principal Component Analysis") +
  theme_minimal()

