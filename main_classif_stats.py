from modules.Utils.DatabaseHandler import *
from modules.Compression.PCAComp import *
from modules.Classification.LogRegClassif import *
from modules.Classification.EnsembleClassif import *
from modules.Utils.EvaluationTasks import *
from modules.Utils.best_confs import *


np.random.seed(0)

structs = ["Xiao_Left_caudate", "Xiao_Right_caudate",
           "Xiao_Left_putamen", "Xiao_Right_putamen"]
nb_fold = 10
nb_comp = 128
id_classes = [0, 1, 2, 3]
class_names = ["Prodromal", "Healthy Control", "Early PD", "DBS PD", "Essential Tremor"]
db_handler = DatabaseHandler()
db_handler.import_anat("data/Xiao_PPMI_PRO/", anat_list=structs, from_pickle=True)  # id = 0
db_handler.import_anat("data/Xiao_PPMI_HC/", anat_list=structs, from_pickle=True)  # id = 1
db_handler.import_anat("data/Xiao_PPMI_PD/", anat_list=structs, from_pickle=True)  # id = 2
db_handler.import_anat("data/Xiao_Rennes_PD/", anat_list=structs, from_pickle=True)  # id = 3
db_handler.import_anat("data/Xiao_Rennes_Tr/", anat_list=structs, from_pickle=True)  # id = 4
db_handler.anat_curate(structs)
db_handler.cut_in_folds(nb_fold)

# Compressor
comp_handler = PCAComp(nb_comp)
for c1 in id_classes:
    for c2 in id_classes:
        if c1 < c2:
            print('\nSVM rbf')
            svmr_handler = SVMClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
            svmr_handler.model.kernel = 'rbf'
            svmr_handler.hyperparams = svmr_array_confs[c1][c2]
            metric_svmr = k_fold_CV_classif(db_handler, comp_handler, svmr_handler, structs, id_classes=[c1, c2])
            print('Score +/- std of', class_names[c1], 'VS', class_names[c2], ':', metric_svmr.score, '+/-', metric_svmr.score_stdev)
            print('\nSVM linear')
            svm_handler = SVMClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
            svm_handler.hyperparams = svml_array_confs[c1][c2]
            metric_svm = k_fold_CV_classif(db_handler, comp_handler, svm_handler, structs, id_classes=[c1, c2])
            print('Score +/- std of', class_names[c1], 'VS', class_names[c2], ':', metric_svm.score, '+/-', metric_svmr.score_stdev)

            print('\nRF')
            rf_handler = RFClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
            rf_handler.hyperparams = rf_array_confs[c1][c2]
            metric_rf = k_fold_CV_classif(db_handler, comp_handler, rf_handler, structs, id_classes=[c1, c2])
            print('Score +/- std of', class_names[c1], 'VS', class_names[c2], ':', metric_rf.score, '+/-', metric_svmr.score_stdev)

            print('\nEnsemble learning')
            base_handler = LogRegClassif(nb_comp=nb_comp, nb_structs=len(structs), output_size=db_handler.source_count)
            svmr_handler.hyperparams = svmr_array_confs[c1][c2]
            svm_handler.hyperparams = svml_array_confs[c1][c2]
            rf_handler.hyperparams = rf_array_confs[c1][c2]
            el_handler = EnsembleClassif(base_handler, [svmr_handler, svm_handler, rf_handler], nb_comp=nb_comp,
                                         nb_structs=len(structs), output_size=db_handler.source_count)
            metric_el = k_fold_CV_classif(db_handler, comp_handler, el_handler, structs, id_classes=[c1, c2])

            print('Score +/- std of', class_names[c1], 'VS', class_names[c2], ':', metric_el.score, '+/-', metric_svmr.score_stdev)

