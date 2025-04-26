import joblib
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
import numpy as np
import os
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import torch
from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm


class RoBERTaTransformerMixin(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        transformer_model: AutoModel,
        transformer_tokenizer: AutoTokenizer,
        device: str,
    ) -> None:
        """
        ---- Description ----
        Initializes a transformer mixin that uses a pretrained transformer model
        (e.g., RoBERTa) to convert text input into dense vector embeddings.

        ---- Parameters ----
        transformer_model : AutoModel
            A pretrained transformer model from the Hugging Face library.
        transformer_tokenizer : AutoTokenizer
            The corresponding tokenizer for the transformer model.
        device : str
            The device to run the model on ("cpu" or "cuda").

        ---- Returns ----
        None

        ---- Raises ----
        None
        """

        self.transformer_model = transformer_model
        self.transformer_tokenizer = transformer_tokenizer
        self.device = device

    def fit(self, X: pd.Series, y: np.array = None):
        """
        ---- Description ----
        Dummy fit method for compatibility with scikit-learn pipelines.

        ---- Parameters ----
        X : pd.Series
            Input text data.
        y : np.array, optional
            Target values (not used).

        ---- Returns ----
        self

        ---- Raises ----
        None
        """

        return self

    def transform(self, X: pd.Series, y: np.array = None) -> np.array:
        """
        ---- Description ----
        Transforms a series of text inputs into dense vector representations
        using the pretrained transformer model.

        ---- Parameters ----
        X : pd.Series
            A pandas Series containing text data.
        y : np.array, optional
            Target values (not used).

        ---- Returns ----
        np.array
            A NumPy array of shape (n_samples, embedding_dim) containing the mean-pooled
            embeddings for each input text.

        ---- Raises ----
        None
        """

        logger.info("#### Beginning to extract embeddings... ####")

        embeddings = []
        for text in tqdm(X.tolist()):
            tokenized_text = self.transformer_tokenizer(
                text=text,
                padding=False,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.device)

            with torch.no_grad():
                output_embeddings = (
                    self.transformer_model(**tokenized_text)
                    .last_hidden_state.detach()
                    .cpu()
                )

            _, rows, columns = output_embeddings.size()
            embeddings.append(
                output_embeddings.numpy().reshape(rows, columns).mean(axis=0)
            )

            del tokenized_text

        embeddings = np.array(embeddings).reshape(len(X), embeddings[0].shape[0])
        return embeddings


class AutomaticNarratives:
    def __init__(self, rating_domain: str, device: str) -> None:
        """
        ---- Description ----
        Initializes an AutomaticNarratives instance that sets up a pipeline
        for predicting psychological ratings (agency or communion) from text.

        ---- Parameters ----
        rating_domain : str
            The rating category to predict. Must be either "agency" or "communion".
        device : str
            The device for running the transformer model ("cpu" or "cuda").

        ---- Returns ----
        None

        ---- Raises ----
        ValueError
            If input parameters are not valid.
        """

        if type(rating_domain) != str:
            raise ValueError(
                f"rating_domain must be a str, current type is {type(rating_domain)}."
            )
        if rating_domain not in ["agency", "communion"]:
            raise ValueError(
                f"rating_domain must either be agency or communion, current value is {rating_domain}."
            )
        if type(device) != str:
            raise ValueError(f"device must be a str, current type is {type(device)}.")
        if device != "cpu" and not device.startswith("cuda"):
            raise ValueError(
                f"device must either specify cpu or cuda (incl. specific cuda-device) - current value is  {device}."
            )

        self.rating_domain = rating_domain
        self.device = device
        self._initialize_pipeline()

    def _initialize_pipeline(self) -> None:
        """
        ---- Description ----
        Initializes the internal prediction pipeline. This includes loading the
        transformer model, tokenizer, and a pretrained ridge regression model for
        predicting the specified rating domain.

        ---- Parameters ----
        None

        ---- Returns ----
        None

        ---- Raises ----
        None
        """

        transformer_model = AutoModel.from_pretrained("microsoft/deberta-v3-base")
        transformer_model.eval()
        transformer_model.to(self.device)
        transformer_tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/deberta-v3-base", use_fast=False
        )
        roberta_transformer_mixin = RoBERTaTransformerMixin(
            transformer_model, transformer_tokenizer, self.device
        )

        this_dir = os.path.dirname(os.path.abspath(__file__))
        ridge_model = joblib.load(
            f"{this_dir}/resources/{self.rating_domain}_rr.joblib"
        )

        self.pipeline = Pipeline(
            steps=[("RTM", roberta_transformer_mixin), ("RR", ridge_model)]
        )
        logger.info(
            f"#### Pipeline was successfully initialized to infer {self.rating_domain} codes. ####"
        )

    def predict(self, X: pd.Series) -> np.array:
        """
        ---- Description ----
        Predicts ratings (agency or communion) from a series of input texts.

        ---- Parameters ----
        X : pd.Series
            A pandas Series of text entries to be evaluated.

        ---- Returns ----
        np.array
            An array of predicted rating values.

        ---- Raises ----
        ValueError
            If input is not a pandas Series of string data.
        """

        if type(X) != type(pd.Series()):
            raise ValueError(
                f"X must be a Pandas Series object, current type is f{type(X)}."
            )
        if X.dtype != object:
            raise ValueError(
                f"X's dtype must be object (str), current dtype is {X.dtype}."
            )

        predictions = self.pipeline.predict(X)
        return predictions
