from modules.Utils.DatabaseHandler import *
from modules.Compression.PCAComp import *
from modules.Classification.LogRegClassif import *
from modules.Classification.EnsembleClassif import *
from modules.Utils.EvaluationTasks import *

np.random.seed(0)
log_file = open("logs_HPO.txt", "w")
structs_tab = [["Xiao_Left_caudate", "Xiao_Right_caudate",
                "Xiao_Left_putamen", "Xiao_Right_putamen"],
               ["Xiao_Left_caudate"],
               ["Xiao_Right_caudate"],
               ["Xiao_Left_putamen"],
               ["Xiao_Right_putamen"]]
nb_fold = 10
nb_comp = 128
id_classes = [0, 1, 2, 3]
class_names = ["Prodromal", "Healthy Control", "Early PD", "DBS PD", "Essential Tremor"]
db_handler = DatabaseHandler()
db_handler.import_anat("data/Xiao_PPMI_PRO/", anat_list=structs_tab[0], from_pickle=True)  # id = 0
db_handler.import_anat("data/Xiao_PPMI_HC/", anat_list=structs_tab[0], from_pickle=True)  # id = 1
db_handler.import_anat("data/Xiao_PPMI_PD/", anat_list=structs_tab[0], from_pickle=True)  # id = 2
db_handler.import_anat("data/Xiao_Rennes_PD/", anat_list=structs_tab[0], from_pickle=True)  # id = 3

db_handler.anat_curate(structs_tab[0])
db_handler.cut_in_folds(nb_fold)

for structs in structs_tab:
    print("\n\n\n STRUCTS: ", structs, "\n\n\n")
    log_file.write("\n\n\nSTRUCTS: " + '-'.join(structs) + "\n\n\n")
    # Compressor
    comp_handler = PCAComp(nb_comp)

    # Handler to optimize
    result_matrix_svmr = np.zeros(shape=(len(id_classes), len(id_classes)))
    result_matrix_svm = np.zeros(shape=(len(id_classes), len(id_classes)))
    result_matrix_rf = np.zeros(shape=(len(id_classes), len(id_classes)))
    result_matrix_el = np.zeros(shape=(len(id_classes), len(id_classes)))
    for c1 in id_classes:
        for c2 in id_classes:
            if c1 == c2:
                result_matrix_svmr[c1, c2] = -1
                result_matrix_svm[c1, c2] = -1
                result_matrix_rf[c1, c2] = -1
                result_matrix_el[c1, c2] = -1
            elif c1 < c2:
                log_file.close()
                log_file = open("logs_HPO_side.txt", "a")
                print('\nSVM rbf')
                log_file.write("\nSVM rbf")
                svmr_handler = SVMClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                svmr_handler.model.kernel = 'rbf'
                conf_svmr, score_svmr, metric_svmr = bayesian_HPO_classif(db_handler, comp_handler, svmr_handler, structs, id_classes=[c1, c2])
                result_matrix_svmr[c1, c2] = score_svmr
                result_matrix_svmr[c2, c1] = score_svmr
                print('Score of', class_names[c1], 'VS', class_names[c2], ':', score_svmr)
                log_file.write('\nScore of ' + class_names[c1] + ' VS ' + class_names[c2] + ': ' + str(score_svmr))

                print('\nSVM linear')
                log_file.write('\nSVM linear')
                svm_handler = SVMClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                conf_svm, score_svm, metric_svm = bayesian_HPO_classif(db_handler, comp_handler, svm_handler, structs, id_classes=[c1, c2])
                result_matrix_svm[c1, c2] = score_svm
                result_matrix_svm[c2, c1] = score_svm
                print('Score of', class_names[c1], 'VS', class_names[c2], ':', score_svm)
                log_file.write('\nScore of ' + class_names[c1] + ' VS ' + class_names[c2] + ': ' + str(score_svm))

                print('\nRF')
                log_file.write('\nRF')
                rf_handler = RFClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                conf_rf, score_rf, metric_rf = bayesian_HPO_classif(db_handler, comp_handler, rf_handler, structs, id_classes=[c1, c2])
                result_matrix_rf[c1, c2] = score_rf
                result_matrix_rf[c2, c1] = score_rf
                print('Score of', class_names[c1], 'VS', class_names[c2], ':', score_rf)
                log_file.write('\nScore of ' + class_names[c1] + ' VS ' + class_names[c2] + ': ' + str(score_rf))

                print('\nEnsemble learning')
                log_file.write('\nEnsemble learning')
                base_handler = LogRegClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                svmr_handler.hyperparams = conf_svmr
                svm_handler.hyperparams = conf_svm
                rf_handler.hyperparams = conf_rf
                el_handler = EnsembleClassif(base_handler, [svmr_handler, svm_handler, rf_handler], nb_comp=nb_comp,
                                             nb_structs=len(structs), output_size=db_handler.source_count)
                conf_el, score_el, metric_el = bayesian_HPO_classif(db_handler, comp_handler, el_handler, structs, id_classes=[c1, c2])

                result_matrix_el[c1, c2] = score_el
                result_matrix_el[c2, c1] = score_el

                print('Score of', class_names[c1], 'VS', class_names[c2], ':', score_el)
                log_file.write('\nScore of ' + class_names[c1] + ' VS ' + class_names[c2] + ': ' + str(score_el))

                print('Confs for', class_names[c1], 'VS', class_names[c2])
                log_file.write('\nConfs for ' + class_names[c1] + ' VS ' + class_names[c2])

                print("\nBest_conf_svm_rbf")
                log_file.write("\nBest_conf_svm_rbf")
                print(conf_svmr)
                for k, v in conf_svmr.items():
                    log_file.write(str(k) + ': ' + str(v) + '\n')

                print("\nBest_conf_svm_linear")
                log_file.write("\nBest_conf_svm_linear")
                print(conf_svm)
                for k, v in conf_svm.items():
                    log_file.write(str(k) + ' >>> ' + str(v) + '\n')

                print("\nBest_conf_rf")
                log_file.write("\nBest_conf_rf")
                print(conf_rf)
                for k, v in conf_rf.items():
                    log_file.write(str(k) + ' >>> ' + str(v) + '\n')

                print("\nBest_conf_el")
                log_file.write("\nBest_conf_el")
                print(conf_el)
                for k, v in conf_el.items():
                    log_file.write(str(k) + ' >>> ' + str(v) + '\n')

                print("\nConf_mat_svmr")
                log_file.write("\nConf_mat_svmr\n")
                print(metric_svmr.conf_mat)
                log_file.write(str(metric_svmr.conf_mat[0][0]) + " " + str(metric_svmr.conf_mat[0][1]) + "\n" +
                               str(metric_svmr.conf_mat[1][0]) + " " + str(metric_svmr.conf_mat[1][1]))
                print("\nScore_tab_svmr")
                log_file.write("\nScore_tab_svmr")
                print(metric_svmr.score_tab_)
                log_file.write(' '.join('{:.3f}'.format(x) for x in metric_svmr.score_tab_))

                print("\nConf_mat_svml")
                log_file.write("\nConf_mat_svml")
                print(metric_svm.conf_mat)
                log_file.write(str(metric_svm.conf_mat[0][0]) + " " + str(metric_svm.conf_mat[0][1]) + "\n" +
                               str(metric_svm.conf_mat[1][0]) + " " + str(metric_svm.conf_mat[1][1]))
                print("\nScore_tab_svml")
                print(metric_svm.score_tab_)
                log_file.write(' '.join('{:.3f}'.format(x) for x in metric_svm.score_tab_))

                print("\nConf_mat_rf")
                log_file.write("\nConf_mat_rf")
                print(metric_rf.conf_mat)
                log_file.write(str(metric_rf.conf_mat[0][0]) + " " + str(metric_rf.conf_mat[0][1]) + "\n" +
                               str(metric_rf.conf_mat[1][0]) + " " + str(metric_rf.conf_mat[1][1]))
                print("\nScore_tab_rf")
                print(metric_rf.score_tab_)
                log_file.write(' '.join('{:.3f}'.format(x) for x in metric_rf.score_tab_))

                print("\nConf_mat_el")
                log_file.write("\nConf_mat_el")
                print(metric_el.conf_mat)
                log_file.write(str(metric_el.conf_mat[0][0]) + " " + str(metric_el.conf_mat[0][1]) + "\n" +
                               str(metric_el.conf_mat[1][0]) + " " + str(metric_el.conf_mat[1][1]))
                print("\nScore_tab_el")
                print(metric_el.score_tab_)
                log_file.write(' '.join('{:.3f}'.format(x) for x in metric_el.score_tab_))

log_file.close()
