from modules.Prediction.PredHandler import *


class BaselinePred(PredHandler):
    def __init__(self, metric_handler):
        PredHandler.__init__(self, metric_handler)
        self.predictor_list = []

    def fit(self, data_train, data_gt, time_diff=None):
        for i in range(len(self.metric_list)):
            mask = ~np.isnan(data_gt[:, i])
            new_gt = data_gt[:, i]
            new_gt = new_gt[mask]
            if type(self.metric_list[i]) is MetricsClassif:
                counts = np.bincount(new_gt.astype(int))
                self.predictor_list.append(np.argmax(counts))
            elif type(self.metric_list[i] is MetricsReg):
                self.predictor_list.append(np.mean(new_gt))

    def predict(self, data, time_diff=None, predictor_ind=0):
        return np.repeat(self.predictor_list[predictor_ind], data.shape[0])

    def reset(self):
        PredHandler.reset(self)
        self.predictor_list = []

