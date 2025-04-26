import typing as t

import pandas as pd

from classification_model import __version__ as _version
from classification_model.config.core import config
from classification_model.processing.data_manager import get_preprocessed_dataset, load_pipeline
from classification_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_survive_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    relevant_data = get_preprocessed_dataset(data)
    validated_data, errors = validate_inputs(input_data=relevant_data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _survive_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": predictions,
            "version": _version,
            "errors": errors,
        }

    return results
