import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

df = pd.read_csv("gender_classification.csv")

df["gender"] = df["gender"].astype("category")
df["gender"] = df["gender"].cat.codes         # Male : 1, Female : 0

x = df.iloc[:,:-1]
y = df.iloc[:,-1]

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=42)

model = GaussianNB()

model.fit(x_train,y_train)

pickle.dump(model,open("model.pkl","wb"))