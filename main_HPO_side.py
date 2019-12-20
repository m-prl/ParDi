from modules.Utils.DatabaseHandler import *
from modules.Compression.PCAComp import *
from modules.Classification.LogRegClassif import *
from modules.Classification.EnsembleClassif import *
from modules.Utils.EvaluationTasks import *

np.random.seed(0)
log_file = open("logs_HPO.txt", "w")
all_structs = ["Xiao_Left_caudate", "Xiao_Right_caudate", "Xiao_Left_putamen", "Xiao_Right_putamen"]
structs_tab = [["Xiao_Left_caudate", "Xiao_Left_putamen"],
               ["Xiao_Right_caudate", "Xiao_Right_putamen"]]
nb_fold = 10
nb_comp = 128
id_classes = [0, 1, 2, 3]
class_names = ["Healthy Control", "Left Start", "Right Start", "All PD"]
db_handler = DatabaseHandler()
db_handler.import_anat("data/Xiao_PPMI_HC/", anat_list=all_structs, from_pickle=True)  # id = 0
db_handler.import_anat("data/Xiao_Rennes_Left/", anat_list=all_structs, from_pickle=False)  # id = 1
db_handler.import_anat("data/Xiao_Rennes_Right/", anat_list=all_structs, from_pickle=False)  # id = 2
db_handler.import_anat("data/Xiao_Rennes_PD/", anat_list=all_structs, from_pickle=True)  # id = 2

db_handler.anat_curate(all_structs)
db_handler.cut_in_folds(nb_fold)

for structs in structs_tab:
    print("\n\n\n STRUCTS: ", structs, "\n\n\n")
    log_file.write("\n\n\nSTRUCTS: " + '-'.join(structs) + "\n\n\n")
    # Compressor
    comp_handler = PCAComp(nb_comp)

    # Handler to optimize
    result_matrix_el = np.zeros(shape=(len(id_classes), len(id_classes)))
    for c1 in id_classes:
        for c2 in id_classes:
            if c1 == c2:
                result_matrix_el[c1, c2] = -1
            elif c1 < c2:
                log_file.close()
                log_file = open("logs_HPO_side.txt", "a")

                svmr_handler = SVMClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                svmr_handler.model.kernel = 'rbf'
                conf_svmr, score_svmr, metric_svmr = bayesian_HPO_classif(db_handler, comp_handler, svmr_handler, structs, id_classes=[c1, c2])

                svm_handler = SVMClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                conf_svm, score_svm, metric_svm = bayesian_HPO_classif(db_handler, comp_handler, svm_handler, structs, id_classes=[c1, c2])

                rf_handler = RFClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                conf_rf, score_rf, metric_rf = bayesian_HPO_classif(db_handler, comp_handler, rf_handler, structs, id_classes=[c1, c2])

                base_handler = LogRegClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
                svmr_handler.hyperparams = conf_svmr
                svm_handler.hyperparams = conf_svm
                rf_handler.hyperparams = conf_rf
                el_handler = EnsembleClassif(base_handler, [svmr_handler, svm_handler, rf_handler], nb_comp=nb_comp,
                                             nb_structs=len(structs), output_size=db_handler.source_count)
                conf_el, score_el, metric_el = bayesian_HPO_classif(db_handler, comp_handler, el_handler, structs, id_classes=[c1, c2])

                result_matrix_el[c1, c2] = score_el
                result_matrix_el[c2, c1] = score_el

                print('\nScore of', class_names[c1], 'VS', class_names[c2], ':', score_el)
                log_file.write('\nScore of ' + class_names[c1] + ' VS ' + class_names[c2] + ': ' + str(score_el))

                print('\nConfs for', class_names[c1], 'VS', class_names[c2])
                log_file.write('\nConfs for ' + class_names[c1] + ' VS ' + class_names[c2])

                print("\nBest_conf_el")
                log_file.write("\nBest_conf_el\n")
                print(conf_el)
                for k, v in conf_el.items():
                    log_file.write(str(k) + ' >>> ' + str(v) + '\n')

                print("\nConf_mat_el")
                log_file.write("\nConf_mat_el\n")
                print(metric_el.conf_mat)
                log_file.write(str(metric_el.conf_mat[0][0]) + " " + str(metric_el.conf_mat[0][1]) + "\n" +
                               str(metric_el.conf_mat[1][0]) + " " + str(metric_el.conf_mat[1][1]))
                print("\nScore_tab_el")
                print(metric_el.score_tab_)
                log_file.write(' '.join('{:.3f}'.format(x) for x in metric_el.score_tab_))

log_file.close()
