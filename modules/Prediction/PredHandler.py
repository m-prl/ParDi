from modules.Utils.Metrics import *


class PredHandler:
    def __init__(self, metric_handler):
        self.predictor_list = []
        self.metric_list = metric_handler.gen_metric_list()

    def fit(self, data_train, data_gt, time_diff=None):
        raise NotImplementedError()

    def predict(self, data, time_diff=None, predictor_ind=0):
        raise NotImplementedError()

    def evaluate(self, data_test, data_gt, time_diff=None):
        if len(self.metric_list) != data_gt.shape[1]:
            print("ClassifHandler: self.used_outputs and data_gt.shape inconsistent:", len(self.metric_list), "vs", data_gt.shape[1])
        else:
            for i in range(len(self.metric_list)):
                mask = ~np.isnan(data_gt[:, i])
                new_data = data_test[mask]
                new_gt = data_gt[:, i]
                new_gt = new_gt[mask]
                if time_diff is not None:
                    new_tf = time_diff[mask]
                else:
                    new_tf = None
                pred = self.predict(new_data, new_tf, predictor_ind=i)
                self.metric_list[i].update(pred, new_gt)
        return self.metric_list

    def reset(self):
        self.predictor_list = []
