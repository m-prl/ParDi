import numpy as np
from sklearn.metrics import confusion_matrix, cohen_kappa_score, accuracy_score, balanced_accuracy_score


class Metrics:

    def __init__(self, pred=None, gt=None):
        self.score = -1
        self.pred = pred
        self.gt = gt
        self.minimize = False

    def append(self, metrics):
        print("Abstract Metrics class")

    def print(self):
        print("Abstract Metrics class")


class MetricsClassif(Metrics):
    def __init__(self, pred=None, gt=None):
        if pred is not None and gt is not None:
            Metrics.__init__(self, pred=pred.astype(int), gt=gt.astype(int))
        else:
            Metrics.__init__(self)
        self.score_tab_ = []
        if self.pred is None:
            self.kappa = -1
            self.accuracy = -1
            self.bal_accuracy = -1
            self.conf_mat = None
            self.score = -1
            self.score_stdev = -1
        else:
            self.kappa = cohen_kappa_score(self.gt, self.pred)
            self.accuracy = accuracy_score(self.gt, self.pred)
            self.bal_accuracy = balanced_accuracy_score(self.gt, self.pred)
            self.conf_mat = confusion_matrix(self.gt, self.pred)
            self.score = self.bal_accuracy
            self.score_tab_.append(self.score)
            self.score_stdev = np.std(np.array(self.score_tab_))
        self.minimize = False

    def append(self, metrics):
        if self.pred is None:
            self.pred = metrics.pred.astype(int)
            self.gt = metrics.gt.astype(int)
        else:
            self.gt = np.concatenate((self.gt.astype(int), metrics.gt.astype(int)))
            self.pred = np.concatenate((self.pred.astype(int), metrics.pred.astype(int)))
        self.kappa = cohen_kappa_score(self.gt, self.pred)
        self.accuracy = accuracy_score(self.gt, self.pred)
        self.bal_accuracy = balanced_accuracy_score(self.gt, self.pred)
        self.conf_mat = confusion_matrix(self.gt, self.pred)
        self.score = self.bal_accuracy
        self.score_tab_.append(self.score)
        self.score_stdev = np.std(np.array(self.score_tab_))

    def update(self, pred, gt):
        new_metric = MetricsClassif(pred=pred, gt=gt)
        self.append(new_metric)

    def print(self):
        metrics_to_print = {'kappa': self.kappa,
                            'accuracy': self.accuracy,
                            'bal_accuracy': self.bal_accuracy,
                            'conf_mat\n': self.conf_mat}
        for metric, score in metrics_to_print.items():
            print(metric+" "+str(score))
        return metrics_to_print


class MetricsReg(Metrics):
    def __init__(self, pred=None, gt=None):
        Metrics.__init__(self, pred=pred, gt=gt)
        if self.pred is None:
            self.mse = -1
            self.mae = -1
        else:
            self.mse = np.mean(np.square(self.gt - self.pred))
            self.mae = np.mean(np.abs(self.gt - self.pred))
        self.minimize = True
        self.score = self.mse

    def append(self, metrics):
        if self.pred is None:
            self.pred = metrics.pred
            self.gt = metrics.gt
        else:
            self.gt = np.concatenate((self.gt.astype(int), metrics.gt))
            self.pred = np.concatenate((self.pred.astype(int), metrics.pred))
        self.mse = np.mean(np.square(self.gt - self.pred))
        self.mae = np.mean(np.abs(self.gt - self.pred))
        self.score = self.mse

    def update(self, pred, gt):
        new_metric = MetricsReg(pred=pred, gt=gt)
        self.append(new_metric)

    def print(self):
        metrics_to_print = {'mse': self.mse,
                            'mae': self.mae}
        for metric, score in metrics_to_print.items():
            print(metric+": "+str(score))
        return metrics_to_print


class MetricsReg2D(Metrics):
    def __init__(self, pred=None, gt=None):
        Metrics.__init__(self, pred=pred, gt=gt)
        if self.pred is None:
            self.mse = -1
            self.mae = -1
            self.nb_rows = 0
        else:
            self.mse = np.mean(np.square(self.gt - self.pred))
            self.mae = np.mean(np.abs(self.gt - self.pred))
            self.nb_rows = pred.shape[0]
        self.minimize = True
        self.score = self.mse

    def append(self, metrics):
        if self.nb_rows == 0:
            self.mse = metrics.mse
            self.mae = metrics.mae
        else:
            self.mse = (self.mse*self.nb_rows) + (metrics.mse*metrics.nb_rows)
            self.mse = self.mse/(self.nb_rows + metrics.nb_rows)
            self.mae = (self.mae*self.nb_rows) + (metrics.mae*metrics.nb_rows)
            self.mae = self.mae/(self.nb_rows + metrics.nb_rows)
        self.score = self.mse
        self.nb_rows = self.nb_rows + metrics.gt.shape[0]

    def update(self, pred, gt):
        new_metric = MetricsReg2D(pred=pred, gt=gt)
        self.append(new_metric)

    def print(self):
        metrics_to_print = {'mse': self.mse,
                            'mae': self.mae}
        for metric, score in metrics_to_print.items():
            print(metric+": "+str(score))
        return metrics_to_print


class MetricHandler:
    def __init__(self):
        self.dict_type = {"has_ah": "classif",
                          "has_t": "classif",
                          "updrs3": "reg",
                          "hy": "reg",
                          "se": "reg",
                          "duration": "reg",
                          "slope": "reg",
                          "source": "classif"}

        self.dict_enabled = {"has_ah": False,
                             "has_t": False,
                             "updrs3": False,
                             "hy": False,
                             "se": False,
                             "duration": False,
                             "slope": False,
                             "source": False}

    def enable(self, score_list):
        for score in score_list:
            if score not in self.dict_enabled:
                print("Score unkown:", score)
            else:
                self.dict_enabled[score] = True

    def gen_metric_list(self):
        metric_list = []
        for key in self.dict_type:
            if self.dict_type[key] is "classif" and self.dict_enabled[key]:
                metric_list.append(MetricsClassif())
            elif self.dict_type[key] is "reg" and self.dict_enabled[key]:
                metric_list.append(MetricsReg())
        return metric_list


def compare_metrics(metric1, metric2, verbose=False):
    diff = ((metric1.score - metric2.score)/metric1.score)*100
    if verbose:
        print(diff, "%")
    return diff

