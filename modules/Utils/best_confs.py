## All structs
svmr_array_confs = []
svml_array_confs = []
rf_array_confs = []
el_array_confs = []
array_confs = []
# SVMr
as_svmr_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

as_svmr_array_confs[0][1] = {'PCA_comp': 1, 'C': 6}
as_svmr_array_confs[0][2] = {'PCA_comp': 1, 'C': 169}
as_svmr_array_confs[0][3] = {'PCA_comp': 56, 'C': 1}
as_svmr_array_confs[1][2] = {'PCA_comp': 90, 'C': 6}
as_svmr_array_confs[1][3] = {'PCA_comp': 50, 'C': 30}
as_svmr_array_confs[2][3] = {'PCA_comp': 106, 'C': 1}
svmr_array_confs.append(as_svmr_array_confs)

# SVMl
as_svml_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

as_svml_array_confs[0][1] = {'PCA_comp': 1, 'C': 5}
as_svml_array_confs[0][2] = {'PCA_comp': 1, 'C': 36}
as_svml_array_confs[0][3] = {'PCA_comp': 64, 'C': 1}
as_svml_array_confs[1][2] = {'PCA_comp': 79, 'C': 1}
as_svml_array_confs[1][3] = {'PCA_comp': 128, 'C': 1}
as_svml_array_confs[2][3] = {'PCA_comp': 108, 'C': 1}
svml_array_confs.append(as_svml_array_confs)

# RF
as_rf_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

as_rf_array_confs[0][1] = {'PCA_comp': 1, 'n_estimators': 2, 'max_depth': 1, 'min_samples_split': 10, 'min_samples_leaf': 5, 'max_features_perc': 0.1}
as_rf_array_confs[0][2] = {'PCA_comp': 4, 'n_estimators': 87, 'max_depth': 1, 'min_samples_split': 10, 'min_samples_leaf': 3, 'max_features_perc': 0.1}
as_rf_array_confs[0][3] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 10, 'min_samples_leaf': 3, 'max_features_perc': 0.1}
as_rf_array_confs[1][2] = {'PCA_comp': 1, 'n_estimators': 2, 'max_depth': 1, 'min_samples_split': 1, 'min_samples_leaf': 5, 'max_features_perc': 1.0}
as_rf_array_confs[1][3] = {'PCA_comp': 110, 'n_estimators': 2000, 'max_depth': 6, 'min_samples_split': 4, 'min_samples_leaf': 4, 'max_features_perc': 0.136}
as_rf_array_confs[2][3] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 5, 'min_samples_leaf': 2, 'max_features_perc': 0.1}
as_rf_all_conf = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 3, 'min_samples_split': 9, 'min_samples_leaf': 3, 'max_features_perc': 0.1}
rf_array_confs.append(as_rf_array_confs)

# EL
as_el_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

as_el_array_confs[0][1] = {'PCA_comp': 1, 'C': 0.00018}
as_el_array_confs[0][2] = {'PCA_comp': 3, 'C': 3.69}
as_el_array_confs[0][3] = {'PCA_comp': 128, 'C': 10}
as_el_array_confs[1][2] = {'PCA_comp': 63, 'C': 10}
as_el_array_confs[1][3] = {'PCA_comp': 128, 'C': 1.079}
as_el_array_confs[2][3] = {'PCA_comp': 128, 'C': 10}
el_array_confs.append(as_el_array_confs)


## Left caudate

# SVMr
lc_svmr_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lc_svmr_array_confs[0][1] = {'PCA_comp': 11, 'C': 21}
lc_svmr_array_confs[0][2] = {'PCA_comp': 1, 'C': 1000}
lc_svmr_array_confs[0][3] = {'PCA_comp': 128, 'C': 1000}
lc_svmr_array_confs[1][2] = {'PCA_comp': 128, 'C': 2}
lc_svmr_array_confs[1][3] = {'PCA_comp': 128, 'C': 306}
lc_svmr_array_confs[2][3] = {'PCA_comp': 128, 'C': 6}
svmr_array_confs.append(lc_svmr_array_confs)

# SVMl
lc_svml_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lc_svml_array_confs[0][1] = {'PCA_comp': 1, 'C': 1000}
lc_svml_array_confs[0][2] = {'PCA_comp': 15, 'C': 23}
lc_svml_array_confs[0][3] = {'PCA_comp': 24, 'C': 1}
lc_svml_array_confs[1][2] = {'PCA_comp': 120, 'C': 2}
lc_svml_array_confs[1][3] = {'PCA_comp': 128, 'C': 1000}
lc_svml_array_confs[2][3] = {'PCA_comp': 128, 'C': 1}
svml_array_confs.append(lc_svml_array_confs)

# RF
lc_rf_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lc_rf_array_confs[0][1] = {'PCA_comp': 22, 'n_estimators': 947, 'max_depth': 1, 'min_samples_split': 5, 'min_samples_leaf': 2, 'max_features_perc': 0.606}
lc_rf_array_confs[0][2] = {'PCA_comp': 59, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 2, 'min_samples_leaf': 2, 'max_features_perc': 0.212}
lc_rf_array_confs[0][3] = {'PCA_comp': 102, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 3, 'min_samples_leaf': 5, 'max_features_perc': 0.342}
lc_rf_array_confs[1][2] = {'PCA_comp': 103, 'n_estimators': 1293, 'max_depth': 2, 'min_samples_split': 3, 'min_samples_leaf': 1, 'max_features_perc': 0.883}
lc_rf_array_confs[1][3] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 10, 'min_samples_split': 10, 'min_samples_leaf': 5, 'max_features_perc': 0.1}
lc_rf_array_confs[2][3] = {'PCA_comp': 110, 'n_estimators': 1172, 'max_depth': 3, 'min_samples_split': 10, 'min_samples_leaf': 1, 'max_features_perc': 0.1}
rf_array_confs.append(lc_rf_array_confs)

# EL
lc_el_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lc_el_array_confs[0][1] = {'PCA_comp': 39, 'C': 4.99e-05}
lc_el_array_confs[0][2] = {'PCA_comp': 65, 'C': 0.0018}
lc_el_array_confs[0][3] = {'PCA_comp': 1, 'C': 0.0063}
lc_el_array_confs[1][2] = {'PCA_comp': 125, 'C': 0.0302}
lc_el_array_confs[1][3] = {'PCA_comp': 114, 'C': 0.0343}
lc_el_array_confs[2][3] = {'PCA_comp': 128, 'C': 0.00906}
el_array_confs.append(lc_el_array_confs)



## Right caudate

# SVMr
rc_svmr_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rc_svmr_array_confs[0][1] = {'PCA_comp': 64, 'C': 1}
rc_svmr_array_confs[0][2] = {'PCA_comp': 64, 'C': 1}
rc_svmr_array_confs[0][3] = {'PCA_comp': 90, 'C': 171}
rc_svmr_array_confs[1][2] = {'PCA_comp': 70, 'C': 7}
rc_svmr_array_confs[1][3] = {'PCA_comp': 99, 'C': 2}
rc_svmr_array_confs[2][3] = {'PCA_comp': 128, 'C': 2}
svmr_array_confs.append(rc_svmr_array_confs)

# SVMl
rc_svml_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rc_svml_array_confs[0][1] = {'PCA_comp': 64, 'C': 1}
rc_svml_array_confs[0][2] = {'PCA_comp': 64, 'C': 1}
rc_svml_array_confs[0][3] = {'PCA_comp': 94, 'C': 14}
rc_svml_array_confs[1][2] = {'PCA_comp': 64, 'C': 1}
rc_svml_array_confs[1][3] = {'PCA_comp': 98, 'C': 1}
rc_svml_array_confs[2][3] = {'PCA_comp': 128, 'C': 2}
svml_array_confs.append(rc_svml_array_confs)

# RF
rc_rf_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rc_rf_array_confs[0][1] = {'PCA_comp': 25, 'n_estimators': 1222, 'max_depth': 1, 'min_samples_split': 3, 'min_samples_leaf': 1, 'max_features_perc': 0.141}
rc_rf_array_confs[0][2] = {'PCA_comp': 6, 'n_estimators': 546, 'max_depth': 1, 'min_samples_split': 5, 'min_samples_leaf': 2, 'max_features_perc': 0.797}
rc_rf_array_confs[0][3] = {'PCA_comp': 128, 'n_estimators': 1110, 'max_depth': 1, 'min_samples_split': 6, 'min_samples_leaf': 5, 'max_features_perc': 1.0}
rc_rf_array_confs[1][2] = {'PCA_comp': 95, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 10, 'min_samples_leaf': 5, 'max_features_perc': 0.1}
rc_rf_array_confs[1][3] = {'PCA_comp': 87, 'n_estimators': 2000, 'max_depth': 7, 'min_samples_split': 6, 'min_samples_leaf': 1, 'max_features_perc': 0.195}
rc_rf_array_confs[2][3] = {'PCA_comp': 128, 'n_estimators': 1260, 'max_depth': 2, 'min_samples_split': 1, 'min_samples_leaf': 1, 'max_features_perc': 0.1}
rf_array_confs.append(rc_rf_array_confs)

# EL
rc_el_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rc_el_array_confs[0][1] = {'PCA_comp': 1, 'C': 0.0159}
rc_el_array_confs[0][2] = {'PCA_comp': 31, 'C': 8.957e-06}
rc_el_array_confs[0][3] = {'PCA_comp': 80, 'C': 10}
rc_el_array_confs[1][2] = {'PCA_comp': 9, 'C': 0.00725}
rc_el_array_confs[1][3] = {'PCA_comp': 42, 'C': 0.00078}
rc_el_array_confs[2][3] = {'PCA_comp': 57, 'C': 10}
el_array_confs.append(rc_el_array_confs)



## Left putamen

# SVMr
lp_svmr_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lp_svmr_array_confs[0][1] = {'PCA_comp': 38, 'C': 2}
lp_svmr_array_confs[0][2] = {'PCA_comp': 57, 'C': 1000}
lp_svmr_array_confs[0][3] = {'PCA_comp': 115, 'C': 1}
lp_svmr_array_confs[1][2] = {'PCA_comp': 127, 'C': 1000}
lp_svmr_array_confs[1][3] = {'PCA_comp': 90, 'C': 319}
lp_svmr_array_confs[2][3] = {'PCA_comp': 128, 'C': 3}
svmr_array_confs.append(lp_svmr_array_confs)

# SVMl
lp_svml_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lp_svml_array_confs[0][1] = {'PCA_comp': 128, 'C': 1000}
lp_svml_array_confs[0][2] = {'PCA_comp': 64, 'C': 1}
lp_svml_array_confs[0][3] = {'PCA_comp': 88, 'C': 220}
lp_svml_array_confs[1][2] = {'PCA_comp': 112, 'C': 1000}
lp_svml_array_confs[1][3] = {'PCA_comp': 88, 'C': 1000}
lp_svml_array_confs[2][3] = {'PCA_comp': 128, 'C': 74}
svml_array_confs.append(lp_svml_array_confs)

# RF
lp_rf_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lp_rf_array_confs[0][1] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 1, 'min_samples_leaf': 5, 'max_features_perc': 0.450}
lp_rf_array_confs[0][2] = {'PCA_comp': 11, 'n_estimators': 1297, 'max_depth': 1, 'min_samples_split': 5, 'min_samples_leaf': 5, 'max_features_perc': 0.133}
lp_rf_array_confs[0][3] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 1, 'min_samples_leaf': 1, 'max_features_perc': 0.1}
lp_rf_array_confs[1][2] = {'PCA_comp': 1, 'n_estimators': 697, 'max_depth': 6, 'min_samples_split': 7, 'min_samples_leaf': 3, 'max_features_perc': 1.0}
lp_rf_array_confs[1][3] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 10, 'min_samples_split': 10, 'min_samples_leaf': 1, 'max_features_perc': 0.128}
lp_rf_array_confs[2][3] = {'PCA_comp': 103, 'n_estimators': 1611, 'max_depth': 1, 'min_samples_split': 6, 'min_samples_leaf': 4, 'max_features_perc': 0.166}
rf_array_confs.append(lp_rf_array_confs)

# EL
lp_el_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

lp_el_array_confs[0][1] = {'PCA_comp': 83, 'C': 0.000408}
lp_el_array_confs[0][2] = {'PCA_comp': 64, 'C': 1.0}
lp_el_array_confs[0][3] = {'PCA_comp': 85, 'C': 10}
lp_el_array_confs[1][2] = {'PCA_comp': 22, 'C': 0.00089}
lp_el_array_confs[1][3] = {'PCA_comp': 128, 'C': 2.606e-05}
lp_el_array_confs[2][3] = {'PCA_comp': 128, 'C': 0.000945}
el_array_confs.append(lp_el_array_confs)


## Right putamen

# SVMr
rp_svmr_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rp_svmr_array_confs[0][1] = {'PCA_comp': 128, 'C': 1}
rp_svmr_array_confs[0][2] = {'PCA_comp': 128, 'C': 3}
rp_svmr_array_confs[0][3] = {'PCA_comp': 64, 'C': 1}
rp_svmr_array_confs[1][2] = {'PCA_comp': 128, 'C': 1000}
rp_svmr_array_confs[1][3] = {'PCA_comp': 108, 'C': 9}
rp_svmr_array_confs[2][3] = {'PCA_comp': 106, 'C': 1}
svmr_array_confs.append(rp_svmr_array_confs)

# SVMl
rp_svml_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rp_svml_array_confs[0][1] = {'PCA_comp': 128, 'C': 1}
rp_svml_array_confs[0][2] = {'PCA_comp': 37, 'C': 41}
rp_svml_array_confs[0][3] = {'PCA_comp': 89, 'C': 17}
rp_svml_array_confs[1][2] = {'PCA_comp': 128, 'C': 1000}
rp_svml_array_confs[1][3] = {'PCA_comp': 111, 'C': 12}
rp_svml_array_confs[2][3] = {'PCA_comp': 128, 'C': 1}
svml_array_confs.append(rp_svml_array_confs)

# RF
rp_rf_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                  [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rp_rf_array_confs[0][1] = {'PCA_comp': 49, 'n_estimators': 492, 'max_depth': 1, 'min_samples_split': 1, 'min_samples_leaf': 4, 'max_features_perc': 0.171}
rp_rf_array_confs[0][2] = {'PCA_comp': 12, 'n_estimators': 490, 'max_depth': 1, 'min_samples_split': 6, 'min_samples_leaf': 4, 'max_features_perc': 0.525}
rp_rf_array_confs[0][3] = {'PCA_comp': 58, 'n_estimators': 1423, 'max_depth': 1, 'min_samples_split': 1, 'min_samples_leaf': 5, 'max_features_perc': 0.1}
rp_rf_array_confs[1][2] = {'PCA_comp': 1, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 6, 'min_samples_leaf': 5, 'max_features_perc': 1.0}
rp_rf_array_confs[1][3] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 6, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features_perc': 0.1}
rp_rf_array_confs[2][3] = {'PCA_comp': 128, 'n_estimators': 2000, 'max_depth': 1, 'min_samples_split': 6, 'min_samples_leaf': 1, 'max_features_perc': 0.1}
rf_array_confs.append(rp_rf_array_confs)

# EL
rp_el_array_confs = [[{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}],
                    [{'null', -1}, {'null', -1}, {'null', -1}, {'null', -1}]]

rp_el_array_confs[0][1] = {'PCA_comp': 1, 'C': 0.000386}
rp_el_array_confs[0][2] = {'PCA_comp': 68, 'C': 0.00369}
rp_el_array_confs[0][3] = {'PCA_comp': 128, 'C': 10}
rp_el_array_confs[1][2] = {'PCA_comp': 103, 'C': 1.568}
rp_el_array_confs[1][3] = {'PCA_comp': 128, 'C': 0.00103}
rp_el_array_confs[2][3] = {'PCA_comp': 102, 'C': 0.0311}
el_array_confs.append(rp_el_array_confs)

array_confs.append(svmr_array_confs)
array_confs.append(svml_array_confs)
array_confs.append(rf_array_confs)
array_confs.append(el_array_confs)
