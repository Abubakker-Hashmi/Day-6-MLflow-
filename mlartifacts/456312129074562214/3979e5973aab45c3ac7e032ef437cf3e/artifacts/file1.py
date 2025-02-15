import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
mlflow.set_tracking_uri("http://127.0.0.1:5000")
#Mention Here your new experiments

mlflow.set_experiment("Day-6-MLflow")
#add new experiments in mlflow server




# Load Wine dataset
wine = load_wine()
X = wine.data
y = wine.target

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

# Define the params for RF model
max_depth = 12
n_estimators = 10

with mlflow.start_run():
    rf=RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators,random_state=42)
    rf.fit(X_train, y_train)
    y_pred=rf.predict(X_test)
    accuracy=accuracy_score(y_test, y_pred)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("random_state", 42)

    #create confusion matrix
    cm=confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap='Blues')
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()

    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("src/file1.py")
    
    # tags
    mlflow.set_tag({"model": "RandomForestClassifier","Author":"Hashim","Project":"Drinks"})
    #log the model
    mlflow.sklearn.log_model(rf, "RandomForestClassifier")

    print("Accuracy: ", accuracy)