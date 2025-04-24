from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classification_model.config.core import config


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    validated_data = input_data[config.model_config.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultiplePassengerDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()
    return validated_data, errors


class PassengerDataInputSchema(BaseModel):
    pclass: Optional[str]
    name: Optional[str]
    sex: Optional[str]
    age: Optional[float]
    sibsp: Optional[str]
    parch: Optional[str]
    ticket: Optional[str]
    fare: Optional[float]
    cabin: Optional[str]
    embarked: Optional[str]
    boat: Optional[str]
    body: Optional[str]
    homedest: Optional[str]  # renamed
    title: Optional[str]


class MultiplePassengerDataInputs(BaseModel):
    inputs: List[PassengerDataInputSchema]
