import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier

#Metodo para obtener la distancia euclidiana de 2 parametros
def dist(x1, y1, x2, y2):
    var = pow((x2 - x1), 2) + pow((y2 - y1), 2)
    return math.sqrt(var)

def KNNimpu(train, test, tmp, axX, axY, Ks):
    #Creacion de dataframe temporal cpn distancia y la clase sobre la que se itero
    neighs = pd.DataFrame({'dist' : [], tmp : []})
    #Iteraciones de test sobre train
    for indexi, i in test.iterrows():
        for indexj, j in train.iterrows():
            tmpdist = dist(i[axX], i[axY], j[axX], j[axY])
            #Llenado del data frame temporal
            neighs = pd.concat([neighs, pd.DataFrame({'dist' : [tmpdist], tmp : j[tmp]})], ignore_index=True)
        neighs = neighs.sort_values(by=['dist'])
        #Aqui se clasifica la variable especie en base a la moda de los Ks indices con menor distancia 
        test.loc[indexi, tmp] = neighs[tmp].iloc[0:Ks].mode().values[0]
        #Se vacia de nuevo el dataframe temporal
        neighs = pd.DataFrame({'dist' : [], tmp : []})

    return test

data = load_wine(as_frame=True)
df = data['frame']
df.rename(columns = {'od280/od315_of_diluted_wines':'diluted_wine'}, inplace = True)
X_train, X_test, y_train, y_test = train_test_split(df, df['target'], stratify=df['target'], test_size=0.3, random_state=None)
model = KNNimpu(X_train, X_test, 'target', 'diluted_wine', 'flavanoids', 7)
score = accuracy_score(y_test, model['target'])
print(score)
print(confusion_matrix(y_test, model['target']))
knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)
print(confusion_matrix(y_test, y_pred))

