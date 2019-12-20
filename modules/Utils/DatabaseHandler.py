import os
import vtk
from modules.Utils.Score_functions import *

db_curation_params = {"diff_t1_discard_thresh": 360,
                      "anat_disp_max": 5,
                      "anat_disp_min": -10}

def get_disp_from_file(file_path, decim_rate=0):
    if decim_rate == 0:
        disp_data = np.genfromtxt(os.path.join(file_path))
    else:
        input_reader = vtk.vtkPolyDataReader()
        input_reader.SetFileName(os.path.join(file_path.replace(".txt", ".vtk")))
        deci = vtk.vtkDecimatePro()
        deci.SetInputConnection(input_reader.GetOutputPort())
        deci.SetTargetReduction(decim_rate)
        deci.PreserveTopologyOff()
        output_writer = vtk.vtkPolyDataWriter()
        output_writer.SetFileName("temp/disp.vtk")
        output_writer.SetInputConnection(deci.GetOutputPort())
        output_writer.Write()
        old_line = ""
        save_mode = False
        new_file = open("temp/disp.txt", "w")
        with open("temp/disp.vtk") as f:
            for line in f:
                if save_mode:
                    new_file.write(line.replace("\n", "").replace(" ", "\n"))
                if (line == "LOOKUP_TABLE default\n") and (old_line == "SCALARS scalars float\n"):
                    save_mode = True
                old_line = line
            f.close()
            os.remove("temp/disp.vtk")
        new_file.close()
        disp_data = np.genfromtxt("temp/disp.txt")
        os.remove("temp/disp.txt")
    return disp_data

class DatabaseHandler:
    def __init__(self):
        self.dataframe = pd.DataFrame()
        self.patient_list = None
        self.source_count = 0
        self.nb_fold = -1

    def import_clinical_Rennes(self, path):
        clinical_df = pd.read_csv(path, delimiter=";")
        clinical_df.set_index("ID", inplace=True)
        clinical_df = clinical_df[clinical_df['diff_t1_clinic'] < db_curation_params['diff_t1_discard_thresh']]
        clinical_df = (clinical_df - clinical_df.min()) / (clinical_df.max() - clinical_df.min())
        clinical_df = pd.concat([clinical_df], keys=["Clinical"], axis=1)
        self.dataframe = pd.concat((self.dataframe, clinical_df))
        #TODO: Recheck that if import clinical is called after or before import_anat

    def import_updrs_PPMI(self, path, mode="value", alpha=0, time_after_dose_thresh=6.0):
        indices = self.dataframe.index.values.tolist()
        updrs_nda = np.empty(shape=0)
        slope_nda = np.empty(shape=0)
        if len(indices) == 0:
            print("Please import anatomical data prior to import PPMI clinical data.")
        clinical_df = pd.read_csv(path, delimiter=",")
        for id in indices:
            id = str(id)
            # check if patient is from PPMI and not from Rennes
            if len(id) == 10:
                patient = int(id[:4])
                year = int(id[4:8])
                month = int(id[8:])
                clinical_df_patient = clinical_df.loc[clinical_df["PATNO"] == patient]
                clinical_df_patient = clinical_df_patient.loc[(clinical_df_patient["TIME_AFTER_DOSE"] >= time_after_dose_thresh) |
                                                              (clinical_df_patient["TIME_AFTER_DOSE"].isnull())]
                # UPDRS score calculation
                if mode == "value":
                    mds_updrs3 = value_mdsupdrs_calc(clinical_df_patient, year, month, alpha)
                elif mode == "slope":
                    slope_mdsupdrs3, mds_updrs3 = slope_mdsupdrs_calc(clinical_df_patient, year, month)
                    slope_nda = np.append(slope_nda, slope_mdsupdrs3)
                else:
                    print("import_updrs_PPMI: mode unknown", mode)
                    mds_updrs3 = -1
                updrs_nda = np.append(updrs_nda, mds_updrs3)
            else:
                updrs_nda = np.append(updrs_nda, np.nan)
                if mode == "slope":
                    slope_nda = np.append(slope_nda, np.nan)
        updrs_nda = (updrs_nda - updrs_nda.mean()) / updrs_nda.std()
        self.dataframe["Clinical", "MDS-UPDRS3"] = updrs_nda
        if mode == "slope":
            slope_nda = (slope_nda - slope_nda.mean()) / slope_nda.std()
            self.dataframe["Clinical", "Slope_MDS-UPDRS3"] = slope_nda

    def import_anat(self, root_path, anat_list, from_pickle=True, decim_rate=0):
        if not from_pickle:
            anat_df = None
            for _, _, files in os.walk(os.path.join(root_path, anat_list[0])):
                for file in files:
                    if ".surf_inout.txt" in file:
                        patient_id = file.replace("sub-", "").replace(".surf_inout.txt", "")
                        present_in_all = True
                        for anat in anat_list:
                            if not os.path.isfile(os.path.join(root_path, anat, file)):
                                present_in_all = False
                        if present_in_all:
                            to_add_tab = []
                            for anat in anat_list:
                                to_add_tab.append(get_disp_from_file(os.path.join(root_path, anat, file), decim_rate=decim_rate))
                            if anat_df is None:
                                labels = [[], []]
                                for i in range(len(to_add_tab)):
                                    labels[0] = labels[0]+(np.repeat(anat_list[i], to_add_tab[i].shape[0]).tolist())
                                    labels[1] = labels[1]+(np.arange(to_add_tab[i].shape[0]).tolist())
                                columns = pd.MultiIndex.from_tuples(list(zip(*labels)))
                                anat_df = pd.DataFrame(columns=columns)
                            for i in range(len(to_add_tab)):
                                anat_df.loc[int(patient_id), anat_list[i]] = to_add_tab[i]
            s = "-".join(anat_list)
            pickle_name = root_path + "pickle-" + s + "-dm_" + str(decim_rate)
            anat_df.to_pickle(pickle_name, compression=None)
        else:
            s = "-".join(anat_list)
            pickle_name = root_path + "pickle-" + s + "-dm_" + str(decim_rate)
            anat_df = pd.read_pickle(pickle_name, compression=None)
        anat_df[anat_df > db_curation_params["anat_disp_max"]] = db_curation_params["anat_disp_max"]
        anat_df[anat_df < db_curation_params["anat_disp_min"]] = db_curation_params["anat_disp_min"]
        anat_df["Clinical", "Source"] = np.repeat(self.source_count, anat_df.shape[0])
        self.source_count = self.source_count + 1
        self.dataframe = pd.concat((self.dataframe, anat_df))

    def anat_curate(self, anat_list, curr="norm"):
        if curr is "norm":
            max = self.dataframe.loc[slice(None), (anat_list, slice(None))].max(axis=0)
            min = self.dataframe.loc[slice(None), (anat_list, slice(None))].min(axis=0)
            self.dataframe.loc[slice(None), (anat_list, slice(None))] = self.dataframe.loc[slice(None), (anat_list, slice(None))] - min
            self.dataframe.loc[slice(None), (anat_list, slice(None))] = self.dataframe.loc[slice(None), (anat_list, slice(None))] / (max - min)

        elif curr is "stand":
            mean = self.dataframe.loc[slice(None), (anat_list, slice(None))].mean(axis=0)
            std = self.dataframe.loc[slice(None), (anat_list, slice(None))].std(axis=0)
            self.dataframe.loc[slice(None), (anat_list, slice(None))] = self.dataframe.loc[slice(None), (anat_list, slice(None))] - mean
            self.dataframe.loc[slice(None), (anat_list, slice(None))] = self.dataframe.loc[slice(None), (anat_list, slice(None))] / std

    def cut_in_folds(self, nb_fold):
        self.nb_fold = nb_fold
        dict_fold = {}
        for source in range(self.source_count):
            # Source tabs initialization
            s_fold = []
            s_patient_list = []
            s_index_list = []
            s_nb_lines = []
            for i in range(nb_fold):
                s_fold.append(i)
                s_patient_list.append([])
                s_nb_lines.append(0)

            # Retriving index of current source
            sources_list = self.dataframe[("Clinical", "Source")].values
            index_list = self.dataframe.index.values
            index_list = index_list[sources_list == source]
            for index in index_list:
                # If PPMI index and not Rennes, index is PPPPYYYYMM
                if index > 9999:
                    patient = int(index/1000000)
                else:
                    patient = index
                found = False
                to_add_fold = -1
                # If patient already in a fold
                for i in range(nb_fold):
                    if patient in s_patient_list[i]:
                        to_add_fold = i
                        found = True
                        break
                # If not, finding tiniest fold to add patient
                if not found:
                    to_add_fold = s_nb_lines.index(min(s_nb_lines))
                s_patient_list[to_add_fold].append(patient)
                s_nb_lines[to_add_fold] = s_nb_lines[to_add_fold] + 1
                dict_fold[index] = to_add_fold
            print("Source", source)
            for i in range(nb_fold):
                print("Fold/count:", i, s_nb_lines[i])
                s_nb_lines.append(0)
        self.patient_list = self.dataframe.index.values.tolist()
        folds_list = []
        for patient in self.patient_list:
            folds_list.append(dict_fold[patient])
        self.dataframe.index = [folds_list, self.patient_list]
        self.dataframe.index.names = ["fold", "index"]
        self.dataframe.sort_index(level=0, inplace=True)
        return nb_fold

    def construct_nda(self, anat_list=None, clinical_list=None, fold_list=None, return_fields=None, return_mode="stacked"):
        if anat_list is None:
            anat_list = []
        if clinical_list is None:
            clinical_list = []
        if anat_list and clinical_list:
            nda = pd.concat((self.dataframe.loc[(fold_list, slice(None)), ("Clinical", clinical_list)],
                             self.dataframe.loc[(fold_list, slice(None)), (anat_list, slice(None))]), axis=1)
            #TODO pourquoi nda plus petit (axis=0) après cette opération ?
        elif anat_list:
            nda = self.dataframe.loc[(fold_list, slice(None)), (anat_list, slice(None))]
        elif clinical_list:
            nda = self.dataframe.loc[(fold_list, slice(None)), ("Clinical", clinical_list)]
        else:
            print("No data columns selected.")
            nda = None
        if anat_list:
            nda = nda[(~(pd.isnull(nda.loc[slice(None), (anat_list, slice(None))])).any(axis=1))]
        if clinical_list:
            nda = nda[(~(pd.isnull(nda.loc[slice(None), ("Clinical", clinical_list)])).all(axis=1))]
        to_return_list = []
        for return_field in return_fields:
            if return_field is "all_anat":
                to_return_list.append(nda.loc[slice(None), (anat_list, slice(None))].values)
            elif return_field is "all_clinical":
                to_return_list.append(nda.loc[slice(None), ("Clinical", clinical_list)].values)
            elif return_field is "all_clinical_no_time":
                to_return_list.append(nda.loc[slice(None), ("Clinical", [x for x in clinical_list if x is not "diff_t1_clinic"])].values)
            elif return_field is "patient":
                to_return_list.append(nda.index.get_level_values(1).values)
            else:
                if return_field in nda.columns.get_level_values(0).values.tolist():
                    to_return_list.append(nda.loc[slice(None), (return_field, slice(None))].values)
                elif return_field in nda.columns.get_level_values(1).values.tolist():
                    to_return_list.append(nda.loc[slice(None), (slice(None), return_field)].values)
                else:
                    print("Field unknown:", return_field)
        if return_mode == "split":
            return to_return_list
        elif return_mode == "stacked":
            return np.column_stack(to_return_list)
        else:
            print("Unkown return mode:", return_mode)
            return None

    def get_patient_list(self):
        return self.patient_list
