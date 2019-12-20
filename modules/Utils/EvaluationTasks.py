import datetime as dt

from modules.Utils.gp import *
from modules.Utils.Metrics import *
from modules.Classification.SVMClassif import *
from modules.Classification.RFClassif import *


def k_fold_CV_comp(db_handler, comp_handler, list_struct, verbose=False):
    mectric_train = MetricsReg2D()
    mectric_test = MetricsReg2D()
    for fold in range(db_handler.nb_fold):
        if verbose:
            print(str(dt.datetime.now().hour)+":"+str(dt.datetime.now().minute)+":"+str(dt.datetime.now().second)+". On fold "+str(fold))
        folds = np.delete(np.arange(db_handler.nb_fold), fold).tolist()
        for struct in list_struct:
            # Db management
            training_data = db_handler.construct_nda(anat_list=list_struct, fold_list=folds, return_fields=[struct])
            test_data = db_handler.construct_nda(anat_list=list_struct, fold_list=[fold], return_fields=[struct])
            # Compression management
            comp_handler.validation_data = test_data
            comp_handler.input_size = training_data.shape[1]
            # Evaluation
            res_train, res_test = comp_handler.evaluate(training_data, testing_data=test_data)
            mectric_train.append(res_train)
            mectric_test.append(res_test)
            comp_handler.reset()
    if verbose:
        print("On training base:")
        mectric_train.print()
        print("On test base:")
        mectric_test.print()
    return mectric_train, mectric_test


# draw and change selected hyperparameters of provided handler, with respect to the bounds, with a bayesian process
#
def bayesian_HPO_comp(db_handler, comp_handler, list_struct, n=None, best_score=None):
    #define the random objective to minimize
    def objective(params):
        container = comp_handler.get_hyperparams()
        i = 0
        for k in container:
            container[k] = params[i]
            i += 1
        comp_handler.set_hyperparams_from_uniform(container)
        comp_handler.print_hyperparams()
        _, metrics = k_fold_CV_comp(db_handler, comp_handler, list_struct)
        if not np.isfinite(metrics.score):
            if metrics.minimize:
                metrics.score = np.finfo('float64').max
            else:
                metrics.score = 0
            print("    Score (on validation fold): NaN error", flush=True)
        else:
            print("    Score (on validation fold): ", metrics.score, flush=True)
        if best_score is not None:
            if (best_score[0] < metrics.score) and not metrics.minimize:
                best_score[0] = metrics.score
            if (best_score[0] > metrics.score) and metrics.minimize:
                best_score[0] = metrics.score
        return metrics.score

    #define the bounds of the solution space
    number = comp_handler.get_number_hyperparams()
    spaceBounds = np.zeros((number, 2))
    spaceBounds[:, 1] = 1.0

    #create and run minimizer
    startingParams = comp_handler.get_hyperparams_as_uniform(comp_handler.get_hyperparams())
    startingParamsList = []
    for k in startingParams:
        startingParamsList.append(startingParams[k])
    initParams = [startingParamsList]
    if n is None:
        numGuesses = min(256, pow(len(comp_handler.get_hyperparams()) + 1, 2))
    else:
        numGuesses = n-1
    optx, opty = bayesian_optimisation(numGuesses, objective, spaceBounds, x0=initParams, minimize=True)
    best_conf = optx[np.argmin(opty),:]
    print("Debug scores1:", opty)
    print("Best conf score=", np.min(opty))
    #transform solution to meaningful co-ordinates and return
    best_conf_container = comp_handler.get_hyperparams()
    i = 0
    for k in best_conf_container:
        best_conf_container[k] = best_conf[i]
        i += 1
    best_conf = comp_handler.get_hyperparams_from_uniform(best_conf_container)

    print("Best params: ", flush=True)
    comp_handler.print_hyperparams(best_conf)
    return best_conf


def k_fold_CV_classif(db_handler, comp_handler, classif_handler, list_struct, verbose=False, id_classes=None, reset=True):
    mectric = MetricsClassif()
    for fold in range(db_handler.nb_fold):
        if verbose:
            print(str(dt.datetime.now().hour)+":"+str(dt.datetime.now().minute)+":"+str(dt.datetime.now().second)+". On fold "+str(fold))
        # Db management
        folds = np.delete(np.arange(db_handler.nb_fold), fold).tolist()
        training_data_structs = []
        test_data_structs = []
        for struct in list_struct:
            training_data_structs.append(db_handler.construct_nda(anat_list=list_struct, fold_list=folds, clinical_list=["Source"], return_fields=[struct]))
            test_data_structs.append(db_handler.construct_nda(anat_list=list_struct, fold_list=[fold], clinical_list=["Source"], return_fields=[struct]))
        test_gt = db_handler.construct_nda(anat_list=list_struct, fold_list=[fold], clinical_list=["Source"], return_fields=['Source'])
        train_gt = db_handler.construct_nda(anat_list=list_struct, fold_list=folds, clinical_list=["Source"], return_fields=['Source'])

        # Compression management
        training_data = np.empty(shape=(train_gt.shape[0], 0))
        test_data = np.empty(shape=(test_gt.shape[0], 0))
        for i in range(len(list_struct)):
            comp_handler.input_size = training_data_structs[i].shape[1]
            comp_handler.validation_data = test_data_structs[i]
            comp_handler.fit(training_data_structs[i])
            train_to_add = comp_handler.compress(training_data_structs[i])
            training_data = np.column_stack((training_data, train_to_add))
            test_to_add = comp_handler.compress(test_data_structs[i])
            test_data = np.column_stack((test_data, test_to_add))
            comp_handler.reset()
        # Filter rows to discard
        # Classification management
        classif_handler.classes_id = id_classes
        mectric.append(classif_handler.evaluate(training_data, train_gt, test_data, test_gt))
        if reset:
            classif_handler.reset()
    if verbose:
        mectric.print()
    return mectric


# draw and change selected hyperparameters of provided handler, with respect to the bounds, with a bayesian process
#
def bayesian_HPO_classif(db_handler, comp_handler, classif_handler, list_struct, n=None, best_score=None, id_classes=None):
    #define the random objective to minimize
    def objective(params):
        container = classif_handler.get_hyperparams()
        i = 0
        for k in container:
            container[k] = params[i]
            i += 1
        classif_handler.set_hyperparams_from_uniform(container)
        classif_handler.print_hyperparams()
        metrics = k_fold_CV_classif(db_handler, comp_handler, classif_handler, list_struct, id_classes=id_classes)
        if not np.isfinite(metrics.score):
            if metrics.minimize:
                metrics.score = np.finfo('float64').max
            else:
                metrics.score = 0
            print("    Score (on validation fold): NaN error", flush=True)
        else:
            print("    Score (on validation fold): ", metrics.score, flush=True)
        if best_score is not None:
            if (best_score[0] < metrics.score) and not metrics.minimize:
                best_score[0] = metrics
            if (best_score[0] > metrics.score) and metrics.minimize:
                best_score[0] = metrics
        return metrics

    #define the bounds of the solution space
    number = classif_handler.get_number_hyperparams()
    spaceBounds = np.zeros((number, 2))
    spaceBounds[:, 1] = 1.0

    #create and run minimizer
    startingParams = classif_handler.get_hyperparams_as_uniform(classif_handler.get_hyperparams())
    startingParamsList = []
    for k in startingParams:
        startingParamsList.append(startingParams[k])
    initParams = [startingParamsList]
    if n is None:
        numGuesses = min(256, pow(len(classif_handler.get_hyperparams()) + 1, 2))
    else:
        numGuesses = n-1
    optx, opty, metrics = bayesian_optimisation(numGuesses, objective, spaceBounds, x0=initParams, minimize=False)
    best_conf = optx[np.argmax(opty), :]
    print("Debug scores2:", opty)
    print("Best conf score=", np.max(opty))

    #transform solution to meaningful co-ordinates and return
    best_conf_container = classif_handler.get_hyperparams()
    i = 0
    for k in best_conf_container:
        best_conf_container[k] = best_conf[i]
        i += 1
    best_conf = classif_handler.get_hyperparams_from_uniform(best_conf_container)
    best_metric = metrics[np.argmax(opty)]

    print("Best params: ", flush=True)
    classif_handler.print_hyperparams(best_conf)
    return best_conf, np.max(opty), best_metric


def compute_struct_importance(db_handler, comp_handler, classif_handler, list_struct, nb_fold=10, verbose=False, id_classes=None):
    feature_importance = np.empty(shape=[len(list_struct), nb_fold])
    for fold in range(db_handler.nb_fold):
        M_tab = []
        if verbose:
            print(str(dt.datetime.now().hour)+":"+str(dt.datetime.now().minute)+":"+str(dt.datetime.now().second)+". On fold "+str(fold))
        # Db management
        folds = np.delete(np.arange(db_handler.nb_fold), fold).tolist()
        training_data_structs = []
        for struct in list_struct:
            training_data_structs.append(db_handler.construct_nda(anat_list=list_struct, fold_list=folds, clinical_list=["Source"], return_fields=[struct]))
        train_gt = db_handler.construct_nda(anat_list=list_struct, fold_list=folds, clinical_list=["Source"], return_fields=['Source'])

        # Compression management
        training_data = np.empty(shape=(train_gt.shape[0], 0))
        for i in range(len(list_struct)):
            comp_handler.input_size = training_data_structs[i].shape[1]
            comp_handler.fit(training_data_structs[i])
            train_to_add = comp_handler.compress(training_data_structs[i])
            training_data = np.column_stack((training_data, train_to_add))
            M_tab.append(comp_handler.model.components_)
            comp_handler.reset()
        # Filter rows to discard
        # Classification management
        classif_handler.classes_id = id_classes

        # Computing feature importance
        for i in range(nb_fold):
            classif_handler.fit(training_data, train_gt)
            if isinstance(classif_handler, SVMClassif):
                feature_importance_ = abs(classif_handler.model.coef_)
                feature_importance_ = feature_importance_/np.sum(feature_importance_)
                feature_importance_ = feature_importance_.reshape(-1)
            elif isinstance(classif_handler, RFClassif):
                feature_importance_ = abs(classif_handler.model.feature_importances_)
                feature_importance_ = feature_importance_/np.sum(feature_importance_)
            else:
                print("Cannot compute feature importance for classifier", type(classif_handler))
                return 0
            # Splitting per struct
            fi_tab = np.split(feature_importance_, len(list_struct))
            for j in range(len(list_struct)):
                feature_importance[j, i] = np.sum(fi_tab[j])
            classif_handler.reset()
        return feature_importance.mean(axis=1), feature_importance.std(axis=1)


def compute_point_importance(db_handler, comp_handler, classif_handler, list_struct, id_classes=None):
        # Db management
        folds = np.arange(db_handler.nb_fold).tolist()
        training_data_structs = []
        for struct in list_struct:
            training_data_structs.append(db_handler.construct_nda(anat_list=list_struct, fold_list=folds, clinical_list=["Source"], return_fields=[struct]))
        train_gt = db_handler.construct_nda(anat_list=list_struct, fold_list=folds, clinical_list=["Source"], return_fields=['Source'])

        # Compression management
        training_data = np.empty(shape=(train_gt.shape[0], 0))
        M_tab = []
        for i in range(len(list_struct)):
            comp_handler.input_size = training_data_structs[i].shape[1]
            comp_handler.fit(training_data_structs[i])
            train_to_add = comp_handler.compress(training_data_structs[i])
            training_data = np.column_stack((training_data, train_to_add))
            M_tab.append(comp_handler.model.components_)
            comp_handler.reset()
        # Filter rows to discard
        # Classification management
        classif_handler.classes_id = id_classes

        feature_importance = None
        # Computing feature importance
        classif_handler.fit(training_data, train_gt)
        if isinstance(classif_handler, SVMClassif):
            feature_importance_ = classif_handler.model.coef_
            feature_importance_ = feature_importance_/np.sum(feature_importance_)
            if feature_importance is None:
                feature_importance = feature_importance_.reshape(-1)
            else:
                feature_importance = feature_importance + feature_importance_.reshape(-1)
        elif isinstance(classif_handler, RFClassif):
            if feature_importance is None:
                feature_importance = classif_handler.model.feature_importances_
            else:
                feature_importance = feature_importance + classif_handler.model.feature_importances_
        else:
            print("Cannot compute feature importance for classifier", type(classif_handler))
            return 0
        # Splitting per struct
        fi_structwise = np.split(feature_importance, len(list_struct))
        point_importance_tab = []
        for i in range(len(list_struct)):
            M = M_tab[i]
            fi_structwise[i] = np.pad(fi_structwise[i], (0, (M.shape[0] - fi_structwise[i].shape[0])), mode="constant", constant_values=(0, 0))
            point_importance = np.matmul(fi_structwise[i], M)
            point_importance_tab.append(point_importance)
        return point_importance_tab
