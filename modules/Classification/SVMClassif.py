from modules.Classification.ClassifHandler import *
from sklearn.svm import SVC


class SVMClassif(ClassifHandler):
    def __init__(self, nb_comp=-1, nb_structs=-1, output_size=-1):
        ClassifHandler.__init__(self, nb_comp, nb_structs, output_size)
        self.hyperparamsNames = self.hyperparamsNames + \
                                ['C']
        self.hyperparams.update({'C': 1})
        self.hyperparamsBounds.update({'C': [1, 1000]})
        self.hyperparamsTypes.update({'C': 'logint'})
        self.model = SVC(kernel='linear', class_weight='balanced', gamma='scale', C=self.hyperparams['C'])

    def fit(self, data_train, data_gt, data_valid=None, valid_gt=None):
        data_train_red, data_gt_red = reduce_classes(data_train, data_gt, self.classes_id)
        data_train_red = reduce_PCA_nbcomp(data_train_red, self.nb_structs, self.hyperparams["PCA_comp"], extra_features=self.extra_features)
        self.model.fit(data_train_red, data_gt_red.ravel())

    def predict(self, data):
        data_red = reduce_PCA_nbcomp(data, self.nb_structs, self.hyperparams["PCA_comp"], extra_features=self.extra_features)
        return self.model.predict(data_red)

    def reset(self):
        self.model = SVC(kernel='linear', class_weight='balanced', gamma='scale', C=self.hyperparams['C'])
