from modules.Prediction.PredHandler import *
from keras import Model
from keras.layers import Input, Dense, Activation, Concatenate, InputLayer
from modules.Utils.Metrics import *
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping


class ANNPred(PredHandler):
    def __init__(self, metric_handler, input_dim=-1):
        PredHandler.__init__(self, metric_handler)
        self.depth = 3
        self.width = 10
        self.input_dim = input_dim
        self.time_diff_enable = False
        self.lr = 0.0001
        self.epochs = 50
        self.batch_size = 32

    def fit(self, data_train, data_gt, time_diff=None):
        self.build()
        cut_point = int(0.8*data_train.shape[0])
        es = EarlyStopping(patience=4)
        if time_diff is not None:
            input_list = [data_train[:cut_point,:], time_diff[:cut_point,:]]
            valid_input_list = [data_train[cut_point:,:], time_diff[cut_point:,:]]
        else:
            input_list = [data_train[:cut_point,:]]
            valid_input_list = [data_train[cut_point:,:]]
        output_list = []
        valid_output_list = []
        for i in range(data_gt.shape[1]):
            output_list.append(data_gt[:cut_point, i])
            valid_output_list.append(data_gt[cut_point:, i])
        self.predictor_list[0].fit(input_list, output_list, validation_data=[valid_input_list, valid_output_list],
                                   epochs=self.epochs, batch_size=self.batch_size, callbacks=[es])

    def predict(self, data, time_diff=None, predictor_ind=0):
        if time_diff is not None:
            input_list = [data, time_diff]
        else:
            input_list = [data]
        predictions = self.predictor_list[0].predict(input_list)
        print(predictions[predictor_ind])
        return predictions[predictor_ind]

    def build(self):
        input_list = []
        output_list = []
        loss_dict = {}
        loss_weights_dict = {}
        input_main = Input(shape=(self.input_dim,))
        input_list.append(input_main)
        flow = input_main
        if self.time_diff_enable:
            input_time_diff = Input(shape=(1,))
            input_list.append(input_time_diff)
            input_time_layer = InputLayer()(input_time_diff)
            flow = Concatenate([input_main, input_time_layer])
        for _ in range(self.depth):
            flow = Dense(self.width)(flow)
            flow = Activation("relu")(flow)
        for i in range(len(self.metric_list)):
            if type(self.metric_list[i]) is MetricsClassif:
                out = Dense(1, activation="softmax", name="out" + str(i))(flow)
                output_list.append(out)
                out_type = "binary_crossentropy"
            elif type(self.metric_list[i]) is MetricsReg:
                out = Dense(1, activation="sigmoid", name="out" + str(i))(flow)
                output_list.append(out)
                out_type = "mse"
            loss_dict["out"+str(i)] = out_type
        model = Model(inputs=input_list, outputs=output_list)
        model.compile(loss=loss_dict, optimizer=Adam(lr=self.lr))
        self.predictor_list.append(model)

