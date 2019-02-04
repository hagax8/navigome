import umap
import sys
import numpy as np
from sklearn import manifold
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import Imputer
from ugtm import eGTM
import math

data = np.genfromtxt(sys.argv[1], delimiter=",", dtype=np.float64)
k = int(math.sqrt(5 * math.sqrt(data.shape[0]))) + 2
print("GTM resolution = %s*%s" % (k, k))
m = int(math.sqrt(k))
print("GTM RBF grid size = %s*%s" % (m, m))
l = 0.1
s = 0.3

missing = Imputer(strategy='median').fit_transform(data)
std = StandardScaler().fit_transform(missing)
pca = PCA(n_components=0.90).fit_transform(std)
data = pca

paramlist = [5, 10, 20, 30, 40, 50]
regul_param = [0.0001, 0.001, 0.01, 0.1, 1, 10]

for i in paramlist:
    print(i)
    data_r = umap.UMAP(n_components=2, random_state=1234, n_neighbors=i,
                       min_dist=0.1).fit_transform(data)
    np.savetxt(sys.argv[2] + 'umap' + "_" + str(i), data_r, delimiter=',',
               header="x,y", comments="")
    data_r = manifold.TSNE(n_components=2, init='pca',
                           random_state=1234,
                           perplexity=i,
                           early_exaggeration=12.0).fit_transform(data)
    np.savetxt(sys.argv[2] + 'tsne' + "_" + str(i), data_r, delimiter=',',
               header="x,y", comments="")

for i in regul_param:
    data_r = eGTM(k=k, m=m, regul=i, s=s,
                  random_state=1234).fit_transform(data)
    np.savetxt(sys.argv[2] + 'gtm' + "_" + str(i), data_r, delimiter=',',
               header="x,y", comments="")
