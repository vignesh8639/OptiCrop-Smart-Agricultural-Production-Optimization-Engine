import os
import joblib
import numpy as np


class CropPredictor:
    """
    Loads the trained model and scaler,
    validates user input,
    and predicts the best crop.
    """

    def __init__(self):

        model_path = "model/crop_model.pkl"
        scaler_path = "model/scaler.pkl"

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                "Model not found! Run model_trainer.py first."
            )

        if not os.path.exists(scaler_path):
            raise FileNotFoundError(
                "Scaler not found! Run model_trainer.py first."
            )

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    # ---------------------------------
    # Validate User Input
    # ---------------------------------

    def validate_input(
        self,
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall
    ):

        values = [
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        ]

        for value in values:

            if value is None:
                raise ValueError("Input cannot be empty.")

        return True

    # ---------------------------------
    # Predict Crop
    # ---------------------------------

    def predict_crop(
        self,
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall
    ):

        self.validate_input(
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        )

        sample = np.array([
            [
                N,
                P,
                K,
                temperature,
                humidity,
                ph,
                rainfall
            ]
        ])

        sample = self.scaler.transform(sample)

        prediction = self.model.predict(sample)

        return prediction[0]


# ---------------------------------------
# Testing
# ---------------------------------------

if __name__ == "__main__":

    predictor = CropPredictor()

    crop = predictor.predict_crop(

        N=90,
        P=42,
        K=43,
        temperature=20.8,
        humidity=82,
        ph=6.5,
        rainfall=202

    )

    print("\nRecommended Crop :", crop)