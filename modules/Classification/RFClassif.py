from modules.Classification.ClassifHandler import *
from sklearn.ensemble import RandomForestClassifier


class RFClassif(ClassifHandler):
    def __init__(self, nb_comp=-1, nb_structs=-1, output_size=-1):
        ClassifHandler.__init__(self, nb_comp, nb_structs, output_size)
        self.hyperparamsNames = self.hyperparamsNames + \
                                ['n_estimators',
                                 'max_depth',
                                 'min_samples_split',
                                 'min_samples_leaf',
                                 'max_features_perc']
        self.hyperparams.update({'n_estimators': 50,
                                 'max_depth': 5,
                                 'min_samples_split': 2,
                                 'min_samples_leaf': 1,
                                 'max_features_perc': 0.5})
        self.hyperparamsBounds.update({'n_estimators': [2, 2000],
                                       'max_depth': [1, 10],
                                       'min_samples_split': [1, 10],
                                       'min_samples_leaf': [1, 5],
                                       'max_features_perc': [0.1, 1.0]})
        self.hyperparamsTypes.update({'n_estimators': 'integer',
                                      'max_depth': 'integer',
                                      'min_samples_split': 'integer',
                                      'min_samples_leaf': 'integer',
                                      'max_features_perc': 'logistic'})
        self.model = RandomForestClassifier(class_weight='balanced', criterion='entropy',
                                            n_estimators=self.hyperparams['n_estimators'],
                                            max_depth=self.hyperparams['max_depth'],
                                            max_features=self.hyperparams['max_features_perc'])

    def fit(self, data_train, data_gt, data_valid=None, valid_gt=None):
        data_train_red, data_gt_red = reduce_classes(data_train, data_gt, self.classes_id)
        data_train_red = reduce_PCA_nbcomp(data_train_red, self.nb_structs, self.hyperparams["PCA_comp"], extra_features=self.extra_features)
        self.model.fit(data_train_red, data_gt_red.ravel())

    def predict(self, data):
        data_red = reduce_PCA_nbcomp(data, self.nb_structs, self.hyperparams["PCA_comp"], extra_features=self.extra_features)
        return self.model.predict(data_red)

    def reset(self):
        self.model = RandomForestClassifier(class_weight='balanced', criterion='entropy',
                                            n_estimators=self.hyperparams['n_estimators'],
                                            max_depth=self.hyperparams['max_depth'],
                                            max_features=self.hyperparams['max_features_perc'])

