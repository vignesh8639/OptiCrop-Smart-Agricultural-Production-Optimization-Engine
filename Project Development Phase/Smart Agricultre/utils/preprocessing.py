import pandas as pd


class DataPreprocessor:
    """
    Handles dataset loading and preprocessing.
    """

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.data = None

    def load_dataset(self):
        """
        Load dataset from CSV file.
        """
        self.data = pd.read_csv(self.dataset_path)
        return self.data

    def display_first_rows(self):
        """
        Display first five rows.
        """
        return self.data.head()

    def dataset_info(self):
        """
        Display dataset information.
        """
        return self.data.info()

    def check_null_values(self):
        """
        Check missing values.
        """
        return self.data.isnull().sum()

    def remove_duplicates(self):
        """
        Remove duplicate rows.
        """
        before = len(self.data)

        self.data = self.data.drop_duplicates()

        after = len(self.data)

        print(f"Duplicates Removed: {before - after}")

        return self.data

    def split_features_target(self):
        """
        Split dataset into X and y.
        """

        X = self.data[
            [
                "N",
                "P",
                "K",
                "temperature",
                "humidity",
                "ph",
                "rainfall"
            ]
        ]

        y = self.data["label"]

        return X, y


if __name__ == "__main__":

    processor = DataPreprocessor(
        "dataset/Crop_recommendation.csv"
    )

    processor.load_dataset()

    print("\nFirst Five Rows\n")
    print(processor.display_first_rows())

    print("\nNull Values\n")
    print(processor.check_null_values())

    print("\nRemoving Duplicates...\n")
    processor.remove_duplicates()

    X, y = processor.split_features_target()

    print("\nFeatures Shape:", X.shape)
    print("Target Shape:", y.shape)