from modules.Compression.CompHandler import *
from sklearn.decomposition import PCA, SparsePCA
from sklearn.preprocessing import MinMaxScaler


class PCAComp(CompHandler):
    def __init__(self, nb_comp, sparse=False):
        CompHandler.__init__(self)

        if sparse:
            self.model = SparsePCA(n_components=nb_comp, normalize_components=True)
        else:
            self.model = PCA(n_components=nb_comp)
        self.preprocesser = MinMaxScaler()
        self.nb_comp = nb_comp
        self.isSparse = sparse

    def fit(self, data):
        tr_data = self.model.fit_transform(data)
        self.preprocesser.fit(tr_data)

    def compress(self, data):
        tr_data = self.model.transform(data)
        return self.preprocesser.transform(tr_data)

    def uncompress(self, data):
        tr_data = self.preprocesser.inverse_transform(data)
        if self.isSparse:
            tr_data = np.dot(tr_data, self.model.components_) + self.model.mean_
        else:
            tr_data = self.model.inverse_transform(tr_data)
        return tr_data

    def reset(self):
        if self.isSparse:
            self.model = SparsePCA(n_components=self.nb_comp)
        else:
            self.model = PCA(n_components=self.nb_comp)
        self.preprocesser = MinMaxScaler()
