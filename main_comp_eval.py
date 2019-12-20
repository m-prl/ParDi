from modules.Utils.DatabaseHandler import *
from modules.Utils.EvaluationTasks import *
from modules.Compression.PCAComp import *
import matplotlib.pyplot as plt

nb_folds = 5
structs = ["Xiao_Left_caudate", "Xiao_Right_caudate",
           "Xiao_Left_putamen", "Xiao_Right_putamen"]

nb_comp_tab = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
valid_mse = np.empty(shape=(len(structs), len(nb_comp_tab)))
db_handler = DatabaseHandler()
db_handler.import_anat("data/Xiao_PPMI_PRO/", anat_list=structs, from_pickle=True)
db_handler.import_anat("data/Xiao_PPMI_HC/", anat_list=structs, from_pickle=True)
db_handler.import_anat("data/Xiao_PPMI_PD/", anat_list=structs, from_pickle=True)
db_handler.import_anat("data/Xiao_Rennes_PD/", anat_list=structs, from_pickle=True)
db_handler.anat_curate(structs)
db_handler.cut_in_folds(nb_folds)
fig, ax = plt.subplots()
for i in range(len(structs)):
    for j in range(len(nb_comp_tab)):
        comp_handler = PCAComp(nb_comp_tab[j])
        metric_training, metric_test = k_fold_CV_comp(db_handler, comp_handler, [structs[i]], verbose=False)
        valid_mse[i, j] = metric_test.mse
    ax.plot(nb_comp_tab, valid_mse[i, :], label=structs[i])
np.save("valid_mse_compression", valid_mse)
ax.legend(loc='upper right')
ax.set_xlabel("nb components")
ax.set_ylabel("mean square error")
ax.set_yscale('log')
xtick_labels = [i for i in nb_comp_tab]
ax.set_xticklabels(xtick_labels)
plt.show()
