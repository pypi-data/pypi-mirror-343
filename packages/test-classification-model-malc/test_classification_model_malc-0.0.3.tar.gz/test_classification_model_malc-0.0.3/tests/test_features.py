from classification_model.config.core import config
from classification_model.processing.features import ExtractLetterTransformer


def test_extract_letter_transformer(sample_input_data):
    # Given
    transformer = ExtractLetterTransformer(
        variables=config.model_config.cabin_var,
    )
    assert sample_input_data[0][config.model_config.cabin_var[0]].iat[5] == "G6"

    # When
    subject = transformer.fit_transform(sample_input_data[0])

    # Then
    assert subject[config.model_config.cabin_var[0]].iat[5] == "G"
