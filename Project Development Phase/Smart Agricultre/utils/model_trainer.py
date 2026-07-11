import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

from sklearn.metrics import accuracy_score


class CropModelTrainer:

    def __init__(self, dataset_path):

        self.dataset_path = dataset_path

        self.df = None

        self.X = None
        self.y = None

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

        self.scaler = StandardScaler()

        self.models = {}

    # ------------------------
    # Load Dataset
    # ------------------------

    def load_dataset(self):

        self.df = pd.read_csv(self.dataset_path)

        print("Dataset Loaded Successfully")
        print(self.df.head())

    # ------------------------
    # Prepare Data
    # ------------------------

    def prepare_data(self):

        self.X = self.df.drop("label", axis=1)

        self.y = self.df["label"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(

            self.X,
            self.y,
            test_size=0.20,
            random_state=42

        )

        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

    # ------------------------
    # Train Models
    # ------------------------

    def train_models(self):

        self.models = {

            "KNN": KNeighborsClassifier(),

            "Logistic Regression": LogisticRegression(max_iter=500),

            "Decision Tree": DecisionTreeClassifier(random_state=42),

            "Random Forest": RandomForestClassifier(random_state=42)

        }

        best_accuracy = 0
        best_model = None
        best_name = ""

        print("\nModel Accuracy\n")

        for name, model in self.models.items():

            model.fit(self.X_train, self.y_train)

            prediction = model.predict(self.X_test)

            accuracy = accuracy_score(
                self.y_test,
                prediction
            )

            print(f"{name} : {accuracy*100:.2f}%")

            if accuracy > best_accuracy:

                best_accuracy = accuracy

                best_model = model

                best_name = name

        print("\nBest Model :", best_name)
        print("Accuracy :", round(best_accuracy*100,2), "%")

        os.makedirs("model", exist_ok=True)

        joblib.dump(best_model, "model/crop_model.pkl")

        joblib.dump(self.scaler, "model/scaler.pkl")

        print("\nModel Saved Successfully")

    # ------------------------
    # KMeans Clustering
    # ------------------------

    def perform_kmeans(self):

        kmeans = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )

        clusters = kmeans.fit_predict(self.X)

        self.df["Cluster"] = clusters

        print("\nK-Means Clustering Completed")


if __name__ == "__main__":

    trainer = CropModelTrainer(
        "dataset/Crop_recommendation.csv"
    )

    trainer.load_dataset()

    trainer.prepare_data()

    trainer.train_models()

    trainer.perform_kmeans()