import numpy as np
import keras.backend as K
from sklearn.metrics import balanced_accuracy_score


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def bal_accuracy(y_true, y_pred):
    return balanced_accuracy_score(y_true.eval(), y_pred.eval())


def reduce_classes(data, gt, id_classes, reassign=True):
    if id_classes is not None:
        assert np.diff(np.array(id_classes)).all() >= 0
        mask = np.zeros(shape=(data.shape[0]), dtype='bool')
        gt_red = gt.copy()
        for i in range(len(id_classes)):
            # Creating masks
            mask[gt_red.reshape(-1) == id_classes[i]] = True
            if reassign:
                gt_red[gt_red[:, 0] == id_classes[i]] = i
        data_red = data[mask]
        gt_red = gt_red[mask]
        return data_red, gt_red
    else:
        return data, gt


def reduce_PCA_nbcomp(data, nb_structs, nb_comp, extra_features=0):
    if nb_structs*nb_comp > data.shape[1]:
        print("nb_structs", nb_structs)
        print("nb_comp", nb_comp)
        print("data.shape[1]", data.shape[1])
        assert nb_structs*nb_comp <= data.shape[1]
    new_data = np.empty(shape=(data.shape[0], 0))
    data_tab = np.split(data[:, :data.shape[1]-extra_features], nb_structs, axis=1)
    for data_struct in data_tab:
        new_data = np.column_stack((new_data, data_struct[:, :int(nb_comp)]))
    if extra_features > 0:
        extra_features_array = data[:, -extra_features:]
        new_data = np.column_stack((new_data, extra_features_array))
    return new_data
