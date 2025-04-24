import numpy as np
from sklearn.metrics import accuracy_score

from classification_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    expected_no_predictions = 262

    # When
    result = make_prediction(input_data=sample_input_data[0])

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[5], np.int64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions
    _predictions = list(predictions)
    y_true = sample_input_data[1]
    accuracy = accuracy_score(_predictions, y_true)
    assert accuracy > 0.6
