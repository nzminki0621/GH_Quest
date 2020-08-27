app_store = read.csv("/Users/imingi/Documents/code/growth_hackers/app_store_modified.csv")


cor.test(app_store$Reviews,app_store$Rating, method = "pearson")
cor.test(app_store$Reviews_logscale,app_store$Rating, method = "pearson")
cor.test(app_store$Installs,app_store$Rating, method = "pearson")
cor.test(app_store$Installs_logscale,app_store$Rating, method = "pearson")
cor.test(app_store$NPriceD,app_store$Rating, method = "pearson")
cor.test(app_store$NSizeM,app_store$Rating, method = "pearson")
