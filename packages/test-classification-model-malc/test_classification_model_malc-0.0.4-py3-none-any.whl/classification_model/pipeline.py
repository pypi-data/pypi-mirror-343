from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import AddMissingIndicator, CategoricalImputer, MeanMedianImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from classification_model.config.core import config
from classification_model.processing import features as pp

survive_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        # impute categorical variables with string missing
        (
            "categorical_imputation",
            CategoricalImputer(
                imputation_method="missing",
                variables=config.model_config.categorical_vars,
            ),
        ),
        # add missing indicator
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_vars),
        ),
        # impute numerical variables with the mean
        (
            "median_imputation",
            MeanMedianImputer(
                imputation_method="median",
                variables=config.model_config.numerical_vars,
            ),
        ),
        (
            "extract_letter",
            pp.ExtractLetterTransformer(
                variables=config.model_config.cabin_var,
            ),
        ),
        (
            "cast_object",
            pp.CastToObject(
                variables=config.model_config.categorical_vars,
            ),
        ),
        # == CATEGORICAL ENCODING
        (
            "rare_label_encoder",
            RareLabelEncoder(
                tol=0.05, n_categories=1, variables=config.model_config.categorical_vars,
            ),
        ),
        # encode categorical variables using the target mean
        (
            "categorical_encoder",
            OneHotEncoder(
                drop_last=True,
                variables=config.model_config.categorical_vars,
            ),
        ),
        ("scaler", StandardScaler()),
        (
            "LogisticRegression",
            LogisticRegression(
                C=config.model_config.c,
                random_state=config.model_config.random_state,
            ),
        ),
    ]
)
