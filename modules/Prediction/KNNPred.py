from modules.Prediction.PredHandler import *
from sklearn.neighbors import KNeighborsClassifier


class KNNPred(PredHandler):
    def __init__(self, metric_handler):
        PredHandler.__init__(self, metric_handler)
        for i in range(len(self.metric_list)):
            if type(self.metric_list[i]) is MetricsClassif:
                self.predictor_list.append(KNeighborsClassifier(n_neighbors=2, n_jobs=6, weights="distance"))
            elif type(self.metric_list[i]) is MetricsReg:
                print("KNN does not support regression.")

    def fit(self, data_train, data_gt, time_diff=None):
        if time_diff is not None:
            train_with_td = np.column_stack((data_train, time_diff))
        else:
            train_with_td = data_train
        for i in range(len(self.metric_list)):
            mask = ~np.isnan(data_gt[:, i])
            new_data = train_with_td[mask]
            new_gt = data_gt[:, i]
            new_gt = new_gt[mask]
            self.predictor_list[i].fit(new_data, new_gt)

    def predict(self, data, time_diff=None, predictor_ind=0):
        if time_diff is not None:
            new_data = np.column_stack((data, time_diff))
        else:
            new_data = data
        return self.predictor_list[predictor_ind].predict(new_data)

    def reset(self):
        PredHandler.reset(self)
        for i in range(len(self.metric_list)):
            if type(self.metric_list[i]) is MetricsClassif:
                self.predictor_list.append(KNeighborsClassifier(n_neighbors=2, weights="uniform"))
            elif type(self.metric_list[i]) is MetricsReg:
                print("KNN does not support regression.")

