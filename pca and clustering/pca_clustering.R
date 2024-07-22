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

run_pca <- function(data, num_components, seed) {
  set.seed(seed)
  data_standardized <- data
  
  print(summary(data_standardized))
  print(data_standardized)
  
  pca_result <- prcomp(data_standardized)
  print(pca_result)
  
  print(summary(pca_result))
  
  loadings <- pca_result$rotation[, 1:num_components]
  print(loadings)
  
  eig.val <- get_eigenvalue(pca_result)
  print(eig.val)
  
  fviz_pca_var(pca_result, col.var = "black")
  fviz_cos2(pca_result, choice = "var", axes = 1:2)
  biplot(pca_result, cex = 0.4)
  fviz_eig(pca_result, addlabels = TRUE)
  fviz_pca_var(pca_result,
               col.var = "cos2", 
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

# 
# linear_reg <- function(train_set, test_set, Predictor) {
#   print(test_set$Predictor)
#   train_set<-as.data.frame(train_set)
#   test_set<-as.data.frame(test_set)
#   lm_pca <- lm(Predictor ~ ., data = train_set)
#   summary_lm <- summary(lm_pca)
#   
#   test_set$pred <- predict(lm_pca, test_set)
#   
#   mean_absolute_percentage_error <- mean(abs((test_set$Predictor - test_set$pred) / test_set$Predictor)) * 100
#   
#   my_x <- seq(1, nrow(test_set))
#   plot(my_x, test_set$Predictor, col = "blue", cex = 0.3, ylab = Predictor, xlab = "Index")
#   lines(my_x, test_set$Predictor, col = "blue")
#   points(my_x, test_set$pred, col = "red", cex = 0.3, pch = 2)
#   lines(my_x, test_set$pred, col = "red")
#   
#   #Homoskedasticity: Breusch-Pagan test
#   bp_test <- bptest(lm_pca)
#   
#   #Independence: Durbin-Watson test
#   dw_test <- dwtest(lm_pca)
#   
#   #Normality: Shapiro-Wilk test
#   shapiro_test <- shapiro.test(lm_pca$residuals)
#   
#   #Variance Inflation Factor
#   vif_values <- vif(lm_pca)
#   
#   results <- list(
#     model_summary = summary_lm,
#     mean_absolute_percentage_error = mean_absolute_percentage_error,
#     bp_test = bp_test,
#     dw_test = dw_test,
#     shapiro_test = shapiro_test,
#     vif_values = vif_values
#   )
#   return(results)
# }

plot_kmeans <- function(combined_data, n_clusters, seed, name, x_col, y_col) {
  data_for_clustering <- combined_data[, c(name, x_col, y_col)]
  print(data_for_clustering[, 1:3])
  colnames(data_for_clustering) <- c('Station', 'X', 'Y')
  
  #Elbow Method
  fviz_nbclust(data_for_clustering[, 2:3], kmeans, method = "wss")
  
  set.seed(seed)
  kmeans_result <- kmeans(data_for_clustering[, 2:3], centers = n_clusters, nstart = 25)
  data_for_clustering$Cluster <- factor(kmeans_result$cluster)
  
  cluster_plot <- fviz_cluster(kmeans_result, data = data_for_clustering[, 2:3])
  print(cluster_plot)
  
  print(data_for_clustering)
  
  kmeans_ggplot <- ggplot(data_for_clustering, aes(x = X, y = Y, color = Cluster, label = Station)) +
    geom_point(size = 4, alpha = 0.8, shape = 19) +
    geom_text(vjust = -1, hjust = 1, check_overlap = TRUE) +
    scale_color_manual(name = "Cluster", values = c("red", "green", "blue", "purple")) +
    labs(x = x_col, y = y_col, title = "K-means Clustering") +
    theme_minimal()
  print(kmeans_ggplot)
  
  #Generate ggplot for PCA visualization without lines
  pca_ggplot <- ggplot(data_for_clustering, aes(x =X, y =Y)) +
    geom_point(size = 4, alpha = 0.8, shape = 19) +
    geom_text(aes(label = Station), vjust = -1, hjust = 1, check_overlap = TRUE) + 
    labs(x = x_col, y = y_col, title = "Principal Component Analysis") +
    theme_minimal()
  print(pca_ggplot)
  
  #Generate ggplot for PCA with METHOD = " "
  pca_smooth_ggplot <- ggplot(data_for_clustering, aes(x = X, y = Y)) +
    geom_point(size = 4, alpha = 0.8, shape = 19) +
    geom_smooth(method = "loess", se = FALSE, color = "blue") +
    geom_text(aes(label = Station), vjust = -1, hjust = 1, check_overlap = TRUE) +  
    labs(x = x_col, y = y_col, title = "Principal Component Analysis with Smoothing") +
    theme_minimal()
  print(pca_smooth_ggplot)
}

my_data <-read.csv("C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/zscore_subwaynames_hsnames.csv", head=TRUE)
set.seed(9922)
my_data <- sample_n(my_data, nrow(my_data))
print(my_data)

station <- data.frame(Station = my_data$Station)
columns_to_delete <-c("Station", "Swipes", "School")
my_data <- my_data[, -which(names(my_data) %in% columns_to_delete)]
print(my_data)

data_standardized <-my_data

pca_results<- run_pca(data_standardized, num_components = 3, seed = 123)

pca_result <- pca_results$pca_result
loadings <- pca_results$loadings
print(loadings)
eig_values <- pca_results$eig_values
cumulative_variance_explained <- pca_results$cumulative_variance_explained
pcs <- pca_results$principal_components

fviz_pca_var(pca_result,
             col.var = "cos2", # Color by the quality of representation
             gradient.cols = c("darkorchid4", "gold", "darkorange"),
             repel = TRUE
)

combined_data <- pcs
print(combined_data)

# n <- nrow(combined_data)
# train_indices <- sample(1:n, size = 0.7 * n)
# train_set <- combined_data[train_indices, ]
# test_set <- combined_data[-train_indices, ]
# print(test_set)

#output <- linear_reg(train_set, test_set, 'PC2')
#print(output)

cor(combined_data)
combined_data <- cbind(combined_data, station)
print(combined_data)
data_for_clustering <- combined_data[, c('Station', 'PC3', 'PC2')]


plot_kmeans(combined_data, n_clusters = 3, seed = 123, "Station", "PC1", "PC2")



