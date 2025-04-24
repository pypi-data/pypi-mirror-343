def ass1():
    code = """
import pandas as pd
import numpy as np
from pandas import read_csv

data = pd.read_csv('diabetes.csv')
print(data)
data.isnull().sum()
from sklearn.model_selection import train_test_split

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 8))
sns.heatmap(X.corr(), annot=True, cmap='viridis', fmt=".2f")
plt.show()

# 3. Pairplot
sns.pairplot(X.iloc[:, :4])
plt.show()

# 4. Boxplot
sns.boxplot(x='Outcome', y='Glucose', data=data)
plt.show()
# 3. Pairplot
sns.pairplot(X.iloc[:, :4])
plt.show()

# 4. Boxplot
sns.boxplot(x='Outcome', y='Glucose', data=data)
plt.show()
    """
    print(code)

def ass2():
    code = """

from sklearn import datasets
from sklearn.model_selection import train_test_split

# Load the Iris dataset
iris = datasets.load_iris()
X = iris.data  # Features
y = iris.target  # Target variable (classes)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


import numpy as np

def find_k_nearest_neighbors(distances, k):
    # Find the indices of the K-nearest neighbors for each test sample
    k_nearest_neighbors_indices = np.argsort(distances, axis=1)[:, :k]
    return k_nearest_neighbors_indices

def calculate_euclidean_distance(X_train, X_test):
    num_test = X_test.shape[0]
    num_train = X_train.shape[0]
    distances = np.zeros((num_test, num_train))

    for i in range(num_test):
        for j in range(num_train):
            distances[i, j] = np.sqrt(np.sum((X_test[i, :] - X_train[j, :])**2))

    return distances


k = 5
distances = calculate_euclidean_distance(X_train, X_test) # Calculate distances between test and training data
k_nearest_neighbors_indices = find_k_nearest_neighbors(distances, k)


from scipy.stats import mode

def predict_majority_class(k_nearest_neighbors_indices, y_train):
    # Get the classes of the K-nearest neighbors
    k_nearest_classes = y_train[k_nearest_neighbors_indices]

    # Predict the class based on the majority class among the neighbors
    predictions, _ = mode(k_nearest_classes, axis=1)
    return predictions.ravel()

y_pred = predict_majority_class(k_nearest_neighbors_indices, y_train)


from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
    """
    print(code)

def ass3():
    code = """

from sklearn import datasets
import pandas as pd
wine = datasets.load_wine()
X = pd.DataFrame(data=wine.data, columns=wine.feature_names)
y = pd.DataFrame(wine.target, columns=['Target'])
X.head()


from sklearn.model_selection import train_test_split
X_train , X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=5)
print(len(X_train))
print(len(X_test))
X_train.head()

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

model.score(X_test, y_test)

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, model.predict(X_test))

from six import StringIO
from IPython.display import Image
from sklearn.tree import export_graphviz
import pydotplus
dot_data = StringIO()
export_graphviz(model, out_file=dot_data,
filled=True, rounded=True,
special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())


from sklearn import datasets
import pandas as pd
data1 = pd.read_csv('RTA Dataset.csv')
data1.head()


data_clean = data1.dropna(subset=['Accident_severity'])
X = data_clean.drop(columns=['Accident_severity', 'Weather_conditions', 'Road_surface_type', 'Time', 'Number_of_vehicles_involved', 'Casualty_severity'])  # Removed 'Driver_Age'
y = data_clean['Accident_severity']


from sklearn.model_selection import train_test_split

X_encoded = pd.get_dummies(X)
X_train , X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.33, random_state=5)
print(len(X_train))
print(len(X_test))
X_train.head()


from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)


model.score(X_test, y_test)


from six import StringIO
from IPython.display import Image
from sklearn.tree import export_graphviz
import pydotplus
dot_data = StringIO()
export_graphviz(model, out_file=dot_data,
filled=True, rounded=True,
special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())
    """

    print(code)

def ass4():
    code = """
    import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "Social_Network_Ads.csv"

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "akram24/social-network-ads",
  file_path,
)

print("First 5 records:", df.head())
df.head(10)


X = df.iloc[:, [2, 3]].values
y = df.iloc[:, 4].values
X

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =
0.25, random_state = 0)
X_train



from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_train



from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0)
classifier.fit(X_train, y_train)
SVC(random_state=0)
y_pred = classifier.predict(X_test)
y_pred



from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test,y_pred)


from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop =
X_set[:, 0].max() + 1, step = 0.01),
np.arange(start = X_set[:, 1].min() - 1, stop =
X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(),
X2.ravel()]).T).reshape(X1.shape),
alpha = 0.75, cmap = ListedColormap(('red', 'green')))

plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('SVM (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()
    """
    print(code)


def ass5():
    code = """
    from sklearn import datasets
iris = datasets.load_iris()

    print(iris.target_names)
print(iris.feature_names)

print(iris.data[0:5])
print(iris.target)


import pandas as pd
data=pd.DataFrame({
    'sepal length':iris.data[:,0],
    'sepal width':iris.data[:,1],
    'petal length':iris.data[:,2],
    'petal width':iris.data[:,3],
    'species':iris.target
})
data.head()

from sklearn.model_selection import train_test_split

X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


from sklearn.ensemble import RandomForestClassifier

clf=RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train,y_train)
y_pred=clf.predict(X_test)



from sklearn import metrics

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


BOOSTING 

from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

adaboost_model = AdaBoostClassifier(n_estimators=100, random_state=42)
gradient_boosting_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
xgboost_model = XGBClassifier(n_estimators=100, random_state=42)

adaboost_model.fit(X_train, y_train)
gradient_boosting_model.fit(X_train, y_train)
xgboost_model.fit(X_train, y_train)

adaboost_pred = adaboost_model.predict(X_test)
gradient_boosting_pred = gradient_boosting_model.predict(X_test)
xgboost_pred = xgboost_model.predict(X_test)


from sklearn.metrics import accuracy_score

adaboost_accuracy = accuracy_score(y_test, adaboost_pred)
gradient_boosting_accuracy = accuracy_score(y_test, gradient_boosting_pred)
xgboost_accuracy = accuracy_score(y_test, xgboost_pred)

print("AdaBoost Model Accuracy:", adaboost_accuracy)
print("Gradient Boosting Model Accuracy:", gradient_boosting_accuracy)
print("XGBoost Model Accuracy:", xgboost_accuracy)




Ensemble Model Using Voting Classifier




from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

decision_tree = DecisionTreeClassifier()
knn = KNeighborsClassifier()


from sklearn.ensemble import VotingClassifier

ensemble_model = VotingClassifier(estimators=[('dt', decision_tree), ('knn', knn)], voting='hard')


ensemble_model.fit(X_train, y_train)

y_pred = ensemble_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Ensemble Model Accuracy:", accuracy)



Bagging classifier using Decision Tree as the base estimator


from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bagging_model = BaggingClassifier(estimator=DecisionTreeClassifier(), n_estimators=10, random_state=42)
bagging_model.fit(X_train, y_train)


bagging_pred = bagging_model.predict(X_test)
bagging_accuracy = accuracy_score(y_test, bagging_pred)
print("Bagging Model Accuracy:", bagging_accuracy)


from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

base_learners = [
    ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
    ('svm', SVC(probability=True, random_state=42)),
    ('dt', DecisionTreeClassifier(random_state=42))
]

meta_model = LogisticRegression()
stacking_model = StackingClassifier(estimators=base_learners, final_estimator=meta_model)
stacking_model.fit(X_train, y_train)
y_pred_stack = stacking_model.predict(X_test)
stacking_accuracy = accuracy_score(y_test, y_pred_stack)
print("Stacking Model Accuracy:", stacking_accuracy)



from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(5, 20),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 10)
}

random_search_rf = RandomizedSearchCV(RandomForestClassifier(random_state=42), param_dist, n_iter=10, cv=5, random_state=42)
random_search_rf.fit(X_train, y_train)

print("Best parameters for Random Forest:", random_search_rf.best_params_)
rf_best_model = random_search_rf.best_estimator_

rf_best_pred = rf_best_model.predict(X_test)
rf_best_accuracy = accuracy_score(y_test, rf_best_pred)
print("Random Forest with Randomized Search Accuracy:", rf_best_accuracy)

    """
    print(code)



def ass6():
    code = """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans, SpectralClustering, DBSCAN
from sklearn.metrics import silhouette_score


iris = load_iris()
X = iris.data
y = iris.target

#finding the optimal k using the elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

#finding the optimal k using silhouette score
silhouette_scores = []
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X)
    labels = kmeans.labels_
    silhouette_scores.append(silhouette_score(X, labels))

plt.plot(range(2, 11), silhouette_scores)
plt.title('Silhouette Score')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.show()



kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(X)
kmeans_labels = kmeans.labels_

spectral = SpectralClustering(n_clusters=3, affinity='nearest_neighbors', assign_labels='kmeans', random_state=0)
spectral_labels = spectral.fit_predict(X)

dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(X)

kmeans_score = silhouette_score(X, kmeans_labels)
spectral_score = silhouette_score(X, spectral_labels)
dbscan_score = silhouette_score(X, dbscan_labels)

print(f"K-means silhouette score: {kmeans_score:.4f}")
print(f"Spectral Clustering silhouette score: {spectral_score:.4f}")
print(f"DBSCAN silhouette score: {dbscan_score:.4f}")


plt.figure(figsize=(10, 7))
plt.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap=matplotlib.colors.ListedColormap(['yellow', 'red', 'blue']), s=15)
plt.title('K-means Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()



plt.figure(figsize=(10, 7))
plt.scatter(X[:, 0], X[:, 1], c=spectral_labels, cmap=matplotlib.colors.ListedColormap(['yellow', 'red', 'blue']), s=15)
plt.title('Spectral Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()



plt.figure(figsize=(10, 7))
dbscan_colors = ['gray', 'yellow', 'red', 'blue']
plt.scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap=matplotlib.colors.ListedColormap(dbscan_colors), s=15)
plt.title('DBSCAN Clustering', fontsize=20)
plt.xlabel('Feature 1', fontsize=14)
plt.ylabel('Feature 2', fontsize=14)
plt.show()
    """
    print(code)


def ass7():
    code = """



#with sklearn
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
lr = LinearRegression()

X = np.array([ 10,9,2, 15, 10, 16, 11, 16], dtype=np.float64)
y = np.array([95, 80, 10, 50, 45, 98, 38, 93], dtype=np.float64)
lr.fit(X.reshape(-1,1),y.reshape(-1,1))
line_y = lr.predict(X.reshape(-1,1))
plt.plot(X,line_y)
plt.scatter(X,y)
plt.xlabel('Number of hours spent driving')
plt.ylabel('Risk score on scale of 0-100')
plt.show()

#slope
lr.coef_

#intercept
lr.intercept_

from sklearn.datasets import fetch_california_housing
housing = fetch_california_housing()

X = housing.data
y = housing.target

print(X.shape)
print(y.shape)
y = housing.target

print(X.shape)
print(y.shape)



#visualize data
import pandas as pd
pd.DataFrame(housing.data, columns=housing.feature_names).head()



from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(housing.data,
housing.target, test_size=0.1)
lr = LinearRegression()
lr.fit(X_train, Y_train)

#accuracy
lr.score(X_test, Y_test)



from sklearn.model_selection import cross_val_score
scores = cross_val_score(lr, housing.data, housing.target, cv=7,
scoring='neg_mean_squared_error')


scores.mean()

scores.std()


from sklearn.model_selection import cross_val_score
scores = cross_val_score(lr, housing.data, housing.target, cv=10,
scoring='r2')


scores.mean()
scores.std()
print('y = ' + str(lr.intercept_) + ' ')
for i, c in enumerate(lr.coef_):
    print(str(c) + ' * x' + str(i))

from sklearn.linear_model import LinearRegression, Ridge
lr = LinearRegression()

#cross-val scores
rg = Ridge(0.001)
lr_scores = cross_val_score(lr, housing.data, housing.target, cv=10)
lr_scores.mean()
rg_scores = cross_val_score(rg, housing.data, housing.target, cv=10)
rg_scores.mean()


#visualize data
import matplotlib.pyplot as plt
import seaborn as sns

sns.heatmap(housing.data)
plt.show()


#without sklearn
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean


X = np.array([ 10,9,2, 15, 10, 16, 11, 16], dtype=np.float64)
y = np.array([95, 80, 10, 50, 45, 98, 38, 93], dtype=np.float64)



m = (((mean(X)* mean(y)) - mean(X*y)) /
	((mean(X)*mean(X)) - mean(X*X)))

b = mean(y) - m*mean(X)

line_y = [res for res in (m*X+b)]

plt.plot(X, line_y)
plt.scatter(X, y)
plt.xlabel('Number of hours spent driving')
plt.ylabel('Risk score on scale of 0-100')
plt.show()



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
%matplotlib inline



!pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "zaraavagyan/weathercsv",
  "weather.csv"
)

print("First 5 records:", df.head())



df.shape
df.describe()
df.plot(x='MinTemp', y='MaxTemp', style='o')
plt.title('MinTemp vs MaxTemp')
plt.xlabel('MinTemp')
plt.ylabel('MaxTemp')
plt.show()


X = df['MinTemp'].values.reshape(-1,1)
y = df['MaxTemp'].values.reshape(-1,1)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)



regressor = LinearRegression()
regressor.fit(X_train, y_train)



#to retrieve the intercept:
print(regressor.intercept_)
#for retrieving the slope:
print(regressor.coef_)



y_pred = regressor.predict(X_test)



df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
df



df1 = df.head(25)
df1.plot(kind='bar',figsize=(16,10))
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.show()



print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    """
    print(code)


def info():
    
    info = """

1. preprocessing 
2. knn 
3. decision tree 
4. SVM 
5. Random forest ensemble 
6. Clustering 
7. Linear and Multi regression"""


    print(info)