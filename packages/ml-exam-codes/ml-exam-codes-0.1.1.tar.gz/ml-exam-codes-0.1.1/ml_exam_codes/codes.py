"""
Module containing ML code snippets for exam preparation.
Call show_code(index) to display a code snippet by index (1 to 10).
"""

ML_CODES = {
    1: """
# find s
import numpy as np
import pandas as pd

# Read dataset
data = pd.read_csv("Data.csv")

# Automatically split features and class label
features = data.columns[:-1]
label_col = data.columns[-1]

# Extract input (X) and output (y)
X = data[features].values
y = data[label_col].values

# Initialize hypothesis with the first positive example
for i in range(len(X)):
    if y[i] == 'Yes':
        hypothesis = X[i].copy()
        break
else:
    raise ValueError("No positive example (label='Yes') found.")

# Apply Find-S algorithm
for i in range(len(X)):
    if y[i] == 'Yes':
        for j in range(len(features)):
            if hypothesis[j] != X[i][j]:
                hypothesis[j] = '?'

# Print the final hypothesis
print("Final Hypothesis (after Find-S):")
print(hypothesis)

# Optional: Log contradictions for 'No' examples
contradictions = []

for i in range(len(X)):
    if y[i] != 'Yes':
        mismatch = []
        for j in range(len(features)):
            if hypothesis[j] != X[i][j]:
                mismatch.append((features[j], hypothesis[j], X[i][j]))  # (feature, hypo_val, neg_val)
        contradictions.append(mismatch)

# Display contradiction info
print("\nContradictions from negative examples:")
for idx, entry in enumerate(contradictions):
    print(f"Example {idx + 1}:")
    for feature, hypo_val, actual_val in entry:
        print(f"  Feature '{feature}': hypothesis='{hypo_val}' vs actual='{actual_val}'")

""",
    2: """
# candidate elimination
import pandas as pd
import numpy as np

# Load the dataset
data = pd.read_csv("Data.csv")

# Split into input and output
X = np.array(data.iloc[:, :-1])   # All columns except the last
y = np.array(data.iloc[:, -1])    # Last column (target)

# Initialize S (Specific hypothesis) to first positive example
S = None
for i in range(len(y)):
    if y[i] == "Yes":
        S = X[i].copy()
        break

# If no positive example is found, exit
if S is None:
    print("No positive example found.")
    exit()

# Initialize G (General hypothesis)
G = [["?" for _ in range(len(S))]]

# Iterate through all examples
for i in range(len(X)):
    if y[i] == "Yes":  # Positive example
        for j in range(len(S)):
            if S[j] != X[i][j]:
                S[j] = "?"
        # Remove hypotheses from G that are inconsistent with the new S
        G = [g for g in G if all(g[j] == "?" or g[j] == S[j] for j in range(len(S)))]
    
    elif y[i] == "No":  # Negative example
        G_new = []
        for g in G:
            for j in range(len(S)):
                if g[j] == "?":
                    if S[j] != X[i][j]:
                        g_copy = g.copy()
                        g_copy[j] = S[j]
                        if all(g_copy[k] == "?" or g_copy[k] != X[i][k] for k in range(len(S))):
                            G_new.append(g_copy)
        G = G_new

# Remove duplicates
G = [list(x) for x in set(tuple(x) for x in G)]

# Output the final S and G
print("Final Specific Hypothesis (S):", S)
print("Final General Hypotheses (G):", G)

""",
    3: """
# Naive Bayes Classifier with Social Network Ads Dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv(r"/home/student/Documents/ML_DATASET/Social_Network_Ads.csv")
print(df.head())
print(df.size)

# Extract input and output
input = df.iloc[:, 0:2]
print(input)
output = df["Purchased"]
print(output)

# Convert to numpy arrays
in_np = np.array(input)
out_np = np.array(output)
print(in_np)

# Split the dataset
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=42)
print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
print(y_train.shape)

# Store X_test for plotting
X_test_n = X_test

# Scale the features
from sklearn.preprocessing import StandardScaler, RobustScaler
sc = RobustScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
print(X_train)
print(X_test)

# Train Naive Bayes model
from sklearn.naive_bayes import BernoulliNB
model = BernoulliNB()
model.fit(X_train, y_train)

# Predict for a single input
print(model.predict(sc.transform([[30, 87000]])))

# Predict on test set
y_pred = model.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

# Check prediction shape and type
print(y_pred.shape)
print(y_pred.dtype)

# Evaluate model
from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(accuracy_score(y_test, y_pred))

# Plot predictions
plt.scatter(X_test_n[:, 0], y_pred)
print(X_test[:, 0].size)
print(y_pred.size)
plt.show()
""",
    4: """
# decision tree car evaluation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"/home/student/Documents/ML_DATASET/car_evaluation.csv", header=None)
df.head()

sum(df.isnull())
df.info

col_nam = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
df.columns = col_nam
df.head()

df['buying'].value_counts()
df['buying'].unique()

for var in col_nam:
    print(df[var].value_counts())

for var in col_nam:
    print(df[var].unique())

for var in col_nam:
    print(df[var].dtype)

df['doors'].replace('5more', '5', inplace=True)
df['persons'].replace('more', '5', inplace=True)

df['doors'] = df['doors'].astype(int)
df['persons'] = df['persons'].astype(int)

df.info()

from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
categories = [var for var in col_nam if df[var].dtype == 'object']
encoder = OrdinalEncoder()
df[categories] = encoder.fit_transform(df[categories])

for var in col_nam:
    if df[var].dtype == 'float64':
        df[var] = df[var].astype(int)

df.info()

input = df.iloc[:, 0:6]
output = df["class"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=0)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42, n_estimators=10, criterion='entropy')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
cm = confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred)
print(classification_report(y_test, y_pred))
# """,



    5: """knn diabates
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

df = pd.read_csv(r"/home/student/Documents/ML_DATASET/diabetes.csv")
df.head()
df.size

input = df.iloc[:,1:7]
output = df["Outcome"]

df.info()

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=42)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.preprocessing import StandardScaler, RobustScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train)
print(X_test)

from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=21, p=2, metric='euclidean')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.dtype)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print("Accuracy ")
accuracy_score(y_test, y_pred)
""",
    6: """knn iris
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df.head()

df.info()

df.size
df["output"] = iris.target

input = df.iloc[:,0:4]
output = df["output"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=42)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.preprocessing import StandardScaler, RobustScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train)
print(X_test)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42, n_estimators=10, criterion='entropy')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.dtype)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print("Accuracy ")
accuracy_score(y_test, y_pred)

plt.scatter(y_pred, y_test)

x1 = X_train
y1 = y_train
x2 = X_test
y2 = y_test
plt.scatter(x1, y1, color='blue', label='Train')
plt.scatter(x2, y2, color='red', label='test')
plt.legend()
plt.show()

X_train.size
y_train.size""",
    7: """multinomial regression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"/home/student/Documents/ML_DATASET/50_Startups.csv")
df

df["State"].unique()
df["State"].replace("New York", 0, inplace=True)
df["State"].replace("California", 1, inplace=True)
df["State"].replace("Florida", 2, inplace=True)

input = df.iloc[:, 0:4]
output = df["Profit"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=0)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train, y_train)

print(X_train)
print(X_test)

y_pred = reg.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.shape)
print(X_train.shape)

plt.scatter(X_test, y_test, color='red')
plt.plot(X_train, reg.predict(X_train), color='blue')

from sklearn.metrics import r2_score
r2 = r2_score(y_test, reg.predict(X_test))
print(r2 * 100, "%")
""",
    8: """simple polynomal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"/home/student/Documents/ML_DATASET/Salary_Data.csv")
df

input = df.iloc[:, 0:1]
output = df["Salary"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=0)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train, y_train)

print(X_train)
print(X_test)

y_pred = reg.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.shape)
print(X_train.shape)

plt.scatter(X_test, y_test, color='red')
plt.plot(X_train, reg.predict(X_train), color='blue')

from sklearn.metrics import r2_score
r2 = r2_score(y_test, reg.predict(X_test))
print(r2 * 100, "%")""",
    9: """ polynomial regresiion
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"/home/student/Documents/ML_DATASET/Position_Salaries.csv")
df

input = df.iloc[:, 1:2]
output = df["Salary"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=0)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train, y_train)

print(X_train)
print(X_test)

y_pred = reg.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.shape)
print(X_train.shape)

plt.scatter(X_test, y_test, color='red')
plt.plot(X_train, reg.predict(X_train), color='blue')

from sklearn.metrics import r2_score
r2 = r2_score(y_test, reg.predict(X_test))
print(r2 * 100, "%")

from sklearn.preprocessing import PolynomialFeatures
X_grid = np.arange(min(X_train), max(X_train), 0.1)
X_grid = X_grid.reshape(len(X_grid), 1)
poly_reg = PolynomialFeatures(degree=4)
X_poly = poly_reg.fit_transform(X_train)
lin_reg2 = LinearRegression()
lin_reg2.fit(X_poly, y_train)

plt.scatter(X_train, y_train, color='red')
plt.plot(X_grid, lin_reg2.predict(poly_reg.fit_transform(X_grid)))
plt.show()

r2 = r2_score(y_test, reg.predict(X_test))
print(r2 * 100, "%")""",
    10: """logarithmic cornoa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"/home/student/Downloads/corona_tested_006.csv")
df = df.iloc[:, 2:12]

df.info()
df.isnull().sum()
df.isnull()

df["Sex"].size

cols = ["Cough_symptoms", "Fever", "Sore_throat", "Shortness_of_breath", "Headache"]
sc = df.isnull()
inx_tr = []
count = 0
for val in sc["Cough_symptoms"]:
    if val == True:
        inx_tr.append(count)
    count = count + 1

inx_tr

df.drop(columns="Age_60_above", inplace=True)
df["Sex"].replace("male", 1, inplace=True)
df["Sex"].replace("female", 0, inplace=True)

df.dropna(inplace=True)

for col in cols:
    df[col].replace(True, 1, inplace=True)
    df[col].replace(False, 0, inplace=True)

df.isnull().sum()
df["Sex"].unique()

df["Corona"].replace("positive", 1, inplace=True)
df["Corona"].replace("negative", 0, inplace=True)
df["Corona"].replace("other", 2, inplace=True)
df["Known_contact"].replace("Abroad", 1, inplace=True)
df["Known_contact"].replace("Contact with confirmed", 0, inplace=True)
df["Known_contact"].replace("Other", 2, inplace=True)

df["Known_contact"].unique()

input = df.iloc[:, 0:9]
df.info()
input = input.drop(columns="Corona")
output = df["Corona"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=20)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
sc = RobustScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.linear_model import LogisticRegression
reg = LogisticRegression()
reg.fit(X_train, y_train)

print(X_train)
print(X_test)

y_pred = reg.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.shape)
print(X_train.shape)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print("Accuracy ")
accuracy_score(y_test, y_pred) """,
    11:"""
#linear regression

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv(r"Salary_Data.csv") 
df
input = df.iloc[:,0:1] 
input
output = df["Salary"] 
output 
in_np=np.array(input) 
out_np=np.array(output) 
in_np
from sklearn.model_selection import train_test_split
X_train , X_test, y_train, y_test = train_test_split(in_np , out_np , test_size=0.20,random_state=0) 
# print(X_train.shape)
# print(X_test.shape) 
# print(y_test.shape) 
# y_train.shape 
X_test_n = X_test
from sklearn.linear_model import LinearRegression 
reg = LinearRegression()
reg.fit(X_train,y_train) 
print(X_train) 
print(X_test)
#predicting the test set result 
y_pred = reg.predict(X_test) 
y_test=np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1) 
y_pred.shape
print(y_pred.shape) 
print(X_train.shape) 
plt.scatter(X_test,y_test,color='red')
plt.plot(X_train,reg.predict(X_train),color='blue') 
plt.title('Simple Linear Regression') 
plt.xlabel('Years of Experience') 
plt.ylabel('Salary')
plt.show()
from sklearn.metrics import r2_score
r2 = r2_score(y_test,reg.predict(X_test)) 
print("R2 Score =",r2*100,"%")
""",
    12:"""
#svm car evaluation
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OrdinalEncoder, StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report 
# Load dataset
data = pd.read_csv(r"car_evaluation.csv", header=None) 
col_name = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class'] 
data.columns = col_name
data

# Replace categorical values in 'doors' and 'persons' 
data['doors'].replace('5more', '5', inplace=True)
data['persons'].replace('more', '5', inplace=True) 
data['doors'] = data['doors'].astype(int) 
data['persons'] = data['persons'].astype(int)
# Encoding categorical features
Categories = ['buying', 'maint', 'lug_boot', 'safety', 'class'] 
encoder = OrdinalEncoder()
data[Categories] = encoder.fit_transform(data[Categories]) 
data = data.astype(int) # Ensure all values are integers
# Prepare input and output 
input = data.iloc[:, 0:6] 
output = data['class']
# Convert to NumPy arrays 
in_np = np.array(input) 
out_np = np.array(output)
# Scatter plot
plt.scatter(np.array(data["buying"]), np.array(data["class"]), color='red') 
plt.xlabel("Buying")
plt.ylabel("Class")
plt.title("Scatter Plot of Buying vs Class") 
plt.show()
# Split dataset
x_train, x_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=0) 
# Scale the features
sc = StandardScaler()
x_train = sc.fit_transform(x_train) 
x_test = sc.transform(x_test)
# Train SVM model
classifier = SVC(kernel='poly', gamma='auto', C=70) 
classifier.fit(x_train, y_train)
# Predict results
y_pred = classifier.predict(x_test) 
# Evaluate model
cm = confusion_matrix(y_test, y_pred) 
accuracy = accuracy_score(y_test, y_pred) 
report = classification_report(y_test, y_pred) 
print(f"Confusion Matrix:\n{cm}") 
print(f"Accuracy: {accuracy:.7f}")
""",
    13:"""
#svm iris
import numpy as np 
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix 
import matplotlib.pyplot as plt
from sklearn.inspection import DecisionBoundaryDisplay 
iris = datasets.load_iris()
df = pd.DataFrame(iris.data, columns = iris.feature_names) 
df.head()
# input = np.array(df.iloc[:,0:4])
X = iris.data 
print(X)
X.shape
# output = np.array(df.iloc[:,4:5]) 
y = iris.target
print(y) 
y.shape
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size= 0.3,random_state = 70) 
print(y_test)
x_train.shape, x_test.shape, y_train.shape, y_test.shape 
sc = StandardScaler()
x_train = sc.fit_transform(x_train) 
x_test = sc.fit_transform(x_test) 
x_train.shape, x_test.shape
classifier = SVC(kernel = 'rbf', gamma = 'scale', C = 10) 
classifier.fit(x_train, y_train)
y_pred = classifier.predict(x_test)

accuracy = accuracy_score(y_test, y_pred) 
print(f"Accuracy is {accuracy: .7f}")
cm = confusion_matrix(y_test, y_pred) 
print(f"Confusion Matrix is \n{cm}")
# Train a new classifier with just the first two features 
classifier_2d = SVC(kernel='linear') 
classifier_2d.fit(x_train[:, :2], y_train)
# Then use your original plotting code 
h = 0.02
x_min, x_max = x_train[:, 0].min() - 1, x_train[:, 0].max() + 1
y_min, y_max = x_train[:, 1].min() - 1, x_train[:, 1].max() + 1 
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), 
np.arange(y_min, y_max, h))
z = classifier_2d.predict(np.c_[xx.ravel(), yy.ravel()]) 
z = z.reshape(xx.shape)
plt.contourf(xx, yy, z, alpha=0.7)
plt.scatter(x_train[:, 0], x_train[:, 1], c=y_train, edgecolors='k', marker='o', 
cmap=plt.cm.Paired)
plt.scatter(x_test[:, 0], x_test[:, 1], c=y_test, edgecolors='r', marker='X', 
cmap=plt.cm.Paired)
plt.title('SVM Decision Boundary (Iris Dataset) - 2D Only') 
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width') 
plt.colorbar()
plt.show()
""",
    14:""" logarithmic
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"/home/student/Documents/ML_DATASET/Social_Network_Ads.csv")
df

input = df.iloc[:, 0:2]
output = df["Purchased"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.10, random_state=0)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.linear_model import LogisticRegression
reg = LogisticRegression()
reg.fit(X_train, y_train)

print(X_train)
print(X_test)

y_pred = reg.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.shape)
print(X_train.shape)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print("Accuracy ")
accuracy_score(y_test, y_pred)""",
    15:""" ann
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

df = pd.read_csv(r"/home/student/Documents/ML_DATASET/Churn_Modelling.csv")
df.head()
df.size

input = df.iloc[:,0:2]
output = df["Purchased"]

in_np = np.array(input)
out_np = np.array(output)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(in_np, out_np, test_size=0.20, random_state=0)

print(X_train.shape)
print(X_test.shape)
print(y_test.shape)
y_train.shape
X_test_n = X_test

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
sc = RobustScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(criterion='entropy', random_state=42)
model.fit(X_train, y_train)

print(X_train)
print(X_test)

print(model.predict(sc.transform([[30, 87000]])))

y_pred = model.predict(X_test)
y_test = np.array(y_test)
out = np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1)

y_pred.shape
print(y_pred.dtype)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
accuracy_score(y_test, y_pred)

print(X_test[:, 0].size)
print(y_pred.size)
""",
    16:"""
#kmeans clustering mall
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
data=pd.read_csv(r"Mall_Customers.csv") 
data
data['Genre']=data['Genre'].replace({'Male':1,'Female':0}) 
#We take just the Annual Income and Spending score
df1=data[["CustomerID","Genre","Age","Annual Income (k$)","Spending Score (1-100)"]] 
X=df1[["Annual Income (k$)","Spending Score (1-100)"]]
#The input data 
X.head()
import seaborn as sns 
#Scatterplot of the input data 
plt.figure(figsize=(10,6))
sns.scatterplot(x = 'Annual Income (k$)',y = 'Spending Score (1-100)', data = X ,s = 60 ) 
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.title('Spending Score (1-100) vs Annual Income (k$)') 
plt.show()
#Importing KMeans from sklearn 
from sklearn.cluster import KMeans 
wcss=[]
for i in range(1,11):
    km=KMeans(n_clusters=i,init='k-means++',random_state=42) 
    km.fit(X)
    wcss.append(km.inertia_) 
#The elbow curve 
plt.figure(figsize=(12,6)) 
plt.plot(range(1,11),wcss)
plt.plot(range(1,11),wcss, linewidth=2, color="red", marker ="8") 
plt.xlabel("K Value")
plt.xticks(np.arange(1,11,1)) 
plt.ylabel("WCSS") 
plt.title('Elbow Method') 
plt.show()
#Taking 5 clusters 
km1=KMeans(n_clusters=5) 
#Fitting the input data 
km1.fit(X)
#predicting the labels of the input data 
y=km1.predict(X)
#adding the labels to a column named label 
df1["Cluster"] = y
#The new dataframe with the clustering done 
df1
# Set up the figure 
plt.figure(figsize=(10, 6)) 
# Calculate centroids
centroids = df1.groupby('Cluster')[['Annual Income (k$)', 'Spending Score (1-100)']].mean() 
# Plot clusters with both hue (color) and style (shape)
sns.scatterplot(
x='Annual Income (k$)', 
y='Spending Score (1-100)', 
hue='Cluster', 
style='Cluster',
palette=['green', 'orange', 'brown', 'dodgerblue', 'red'], 
data=df1,
s=80,
legend='full'
)
# Plot centroids with a distinct marker and label 
plt.scatter(
centroids['Annual Income (k$)'], 
centroids['Spending Score (1-100)'],
s=200,
c='black', 
marker='X', 
label='Centroid'
)
# Axis labels and title 
plt.xlabel('Annual Income (k$)') 
plt.ylabel('Spending Score (1-100)')
plt.title('Spending Score (1-100) vs Annual Income (k$)') 
# Display complete legend including centroids 
plt.legend(title='Cluster + Centroid', loc='best')
plt.show()
""",
    17:"""
#kmeans iris
import numpy as np 
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score 
iris = datasets.load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names) 
df['target'] = iris.target
df
X = df.iloc[:, :-1].values # All feature columns (sepal length, width, petal length, width)
Y = df['target'].values
# True target labels (iris species)# Calculate the accuracy
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=70) 
sc = StandardScaler()
x_train = sc.fit_transform(x_train) 
x_test = sc.transform(x_test)
kmeans = KMeans(n_clusters=50, random_state=70) # 3 clusters for Iris (3 species) 
y_kmeans = kmeans.fit_predict(x_train)
iris['Cluster'] = y_kmeans
mapped_labels = np.zeros_like(y_kmeans) 
for cluster in np.unique(y_kmeans):
    most_common_label = np.bincount(y_train[y_kmeans == cluster]).argmax() 
    mapped_labels[y_kmeans == cluster] = most_common_label
accuracy = accuracy_score(y_train, mapped_labels)
print(f'Accuracy of K-Means clustering for iris dataset: {accuracy * 100:.2f}%')
"""
}

def show_code(index):
    """
    Display the ML code snippet for the given index (1 to 10).
    
    Args:
        show_code(index) to display a code snippet by index (1 to 10).
        index (int): Index of the code snippet (1 to 10).
    
    Returns:
        str: The code snippet as a string, or an error message if index is invalid.
    """
    if index not in ML_CODES:
        return f"Error: Invalid index {index}. Please choose between 1 and 10."
    code = ML_CODES[index].strip()
    print(code)  # Display the code
    return code