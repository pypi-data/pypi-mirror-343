# Automatic Narratives

Automatic Narratives is a Python module for predicting **agency** or **communion** codes from natural language text using transformer-based embeddings (RoBERTa) and ridge regression.

## Features

- Uses `microsoft/roberta-base` to generate contextual embeddings
- Predicts codes for either **agency** or **communion** using pretrained ridge regression models
- Fully compatible with scikit-learn pipelines

---

## Installation

Clone the repository and install dependencies:

```python
import pandas as pd
from automatic_narratives import AutomaticNarratives

# Example texts
texts = pd.Series([
    "She took charge of the situation and led the team with confidence.",
    "He cared deeply for others and always made time to listen."
])

# Choose device: "cpu" or "cuda" (if available)
device = "cpu"

# Initialize predictor for agency
agency_predictor = AutomaticNarratives(rating_domain="agency", device=device)

# Predict agency scores
agency_scores = agency_predictor.predict(texts)
```
