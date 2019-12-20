from modules.Utils.Metrics import *
from modules.Utils.utils import *
import copy
import math


class ClassifHandler:
    def __init__(self, nb_comp, nb_structs, output_size):
        self.model = None
        self.nb_comp = nb_comp
        self.nb_structs = nb_structs
        self.output_size = output_size
        self.classes_id = None
        self.extra_features = 0
        self.hyperparamsNames = ["PCA_comp"]
        self.hyperparams = {"PCA_comp": nb_comp/2}
        self.hyperparamsBounds = {"PCA_comp": [1, nb_comp]}
        self.hyperparamsTypes = {"PCA_comp": "integer"}

    def fit(self, data_train, data_gt, data_valid=None, valid_gt=None):
        raise NotImplementedError()

    def predict(self, data):
        raise NotImplementedError()

    def evaluate(self, data_train, train_gt, data_test, test_gt):
        self.fit(data_train, train_gt, data_valid=data_test, valid_gt=test_gt)
        data_test_red, gt_test_red = reduce_classes(data_test, test_gt, self.classes_id)
        pred = self.predict(data_test_red)
        return MetricsClassif(pred, gt_test_red)

    def reset(self):
        self.model = None

    def get_number_hyperparams(self):
        return len(self.hyperparams)

    def get_hyperparams_as_uniform(self, params):
        retparams = self.get_hyperparams()
        for k in params:
            type = self.hyperparamsTypes[k]
            if type == "interval":
                retparams[k] = (float(params[k])-float(self.hyperparamsBounds[k][0])) / (float(self.hyperparamsBounds[k][1])-float(self.hyperparamsBounds[k][0]))
            elif type == "logistic":
                prelog = np.log(float(params[k]))
                retparams[k] = (prelog-np.log(float(self.hyperparamsBounds[k][0]))) / (np.log(float(self.hyperparamsBounds[k][1]))-np.log(float(self.hyperparamsBounds[k][0])))
            elif type == "integer":
                retparams[k] = (float(params[k])-float(self.hyperparamsBounds[k][0])+0.5) / (float(self.hyperparamsBounds[k][1])-float(self.hyperparamsBounds[k][0]))
            elif type == "logint":
                prelog = np.log(float(params[k]))
                retparams[k] = (prelog - np.log(float(self.hyperparamsBounds[k][0]))) / (
                                np.log(float(self.hyperparamsBounds[k][1])) - np.log(float(self.hyperparamsBounds[k][0])))
            elif type == "categorical":
                index = 0
                for j in range(len(self.hyperparamsBounds[k])):
                    if params[k] == self.hyperparamsBounds[k][j]:
                        index = j
                retparams[k] = (float(index)+0.5) / float(len(self.hyperparamsBounds[k]))
        return retparams

    def get_hyperparams_from_uniform(self, params):
        retparams = self.get_hyperparams()
        for k in params:
            type = self.hyperparamsTypes[k]
            if type == "interval":
                retparams[k] = float(self.hyperparamsBounds[k][0] + params[k] *
                                    (self.hyperparamsBounds[k][1]-self.hyperparamsBounds[k][0]))
            elif type == "logistic":
                prelog = float(math.log(self.hyperparamsBounds[k][0]) + params[k] *
                         (math.log(self.hyperparamsBounds[k][1]) - np.log(self.hyperparamsBounds[k][0])))
                retparams[k] = np.exp(prelog)
            elif type == "integer":
                retparams[k] = self.hyperparamsBounds[k][0] + int(params[k] *
                                      (float(self.hyperparamsBounds[k][1])-float(self.hyperparamsBounds[k][0])+0.999))
            elif type == "logint":
                prelog = np.log(self.hyperparamsBounds[k][0]) + (params[k] *
                         (np.log(self.hyperparamsBounds[k][1]) - np.log(self.hyperparamsBounds[k][0])))
                retparams[k] = int(np.exp(prelog)+0.5)
            elif type == "categorical":
                index = int(params[k] * float(len(self.hyperparamsBounds[k])))
                retparams[k] = self.hyperparamsBounds[k][index]
        return retparams

    def set_hyperparams_from_uniform(self, params):
        transformedParams = self.get_hyperparams_from_uniform(params)
        for k in self.hyperparams:
            self.hyperparams[k] = transformedParams[k]

    def print_hyperparams(self, params=None):
        if len(self.hyperparams) == 0:
            print("No hyperparameters")
            return
        if params is None:
            params = self.hyperparams
        for k in self.hyperparams:
            print(k, '\t(',  self.hyperparamsTypes[k], ')\t', params[k])

    def get_hyperparams(self):
        return copy.copy(self.hyperparams)

    def set_hyperparams(self, params):
        for k in self.hyperparams:
            self.hyperparams[k] = params[k]
