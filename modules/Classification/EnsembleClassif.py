from modules.Classification.ClassifHandler import *


class EnsembleClassif(ClassifHandler):
    def __init__(self, model, base_models, nb_comp, nb_structs, output_size):
        ClassifHandler.__init__(self, nb_comp, nb_structs, output_size)
        self.model = model
        self.base_models = base_models
        self.model.extra_features = len(self.base_models)
        self.hyperparamsNames = self.model.hyperparamsNames
        self.hyperparams = self.model.hyperparams
        self.hyperparamsBounds = self.model.hyperparamsBounds
        self.hyperparamsTypes = self.model.hyperparamsTypes

    def fit(self, data_train, data_gt, data_valid=None, valid_gt=None):
        base_features_train = data_train.copy()
        base_features_valid = data_valid.copy()
        for base_model in self.base_models:
            base_model.classes_id = self.classes_id
            base_model.fit(data_train, data_gt, data_valid=data_valid, valid_gt=valid_gt)
            base_features_train = np.column_stack((base_features_train, base_model.predict(data_train)))
            base_features_valid = np.column_stack((base_features_valid, base_model.predict(data_valid)))
        self.model.classes_id = self.classes_id
        self.model.fit(base_features_train, data_gt, data_valid=base_features_valid, valid_gt=valid_gt)

    def predict(self, data):
        base_features = data.copy()
        for base_model in self.base_models:
            base_model.classes_id = self.classes_id
            pred = base_model.predict(data)
            base_features = np.column_stack((base_features, pred))
        return self.model.predict(base_features)

    def reset(self):
        self.model.reset()
        for base_model in self.base_models:
            base_model.reset()
