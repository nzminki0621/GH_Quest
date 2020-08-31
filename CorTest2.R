app_store = read.csv("/Users/imingi/Documents/code/growth_hackers/app_store_modified_3.csv")


cor.test(app_store$stds_rating,app_store$Rating, method = "pearson")



