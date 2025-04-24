"""Selects the appropriate pretrained encoder from Hugging Face.

This module also includes two types of special-casing:

* Some models have non-standard names for parameters we provide.
* Some models require us to set certain options.
* We warn the user if they select a pre-trained encoder we haven't tested yet.

Users are encouraged to file pull requests to fill this out.
"""

import logging

import transformers

# The keys here are assumed to be prefixes of full name and should include
# the organization name, a forward slash, and the shared prefix of the model.

# Please keep in lexicographic order.
# The key is the model prefix; the value is a dictionary of remappings for the
# provided parameters. If the value is empty, this indicates models with this
# prefix are believed to work with UDTube.
SUPPORTED_ENCODERS = {
    "DeepPavlov/rubert": {"dropout": "hidden_dropout_prob"},
    "FacebookAI/roberta": {"dropout": "hidden_dropout_prob"},
    "FacebookAI/xlm-roberta": {"dropout": "hidden_dropout_prob"},
    "dccuchile/bert-base-spanish": {"dropout": "hidden_dropout_prob"},
    "distilbert/distilbert": {},
    "flaubert/flaubert": {},
    "google-t5/t5": {"hidden_dropout_prob": "dropout_rate"},
    "google-bert/bert": {"dropout": "hidden_dropout_prob"},
    "nlpaueb/bert-base-greek": {"dropout": "hidden_dropout_prob"},
}


def load(model_name: str, **kwargs) -> transformers.AutoModel:
    """Loads the encoder and applies any special casing.

    Args:
        model_name (str): the Hugging Face model name.
        **kwargs: kwargs to be passed to the encoder constructor after any
            remapping.

    Returns:
        A Hugging Face encoder.
    """
    model_found = False
    for prefix, remappings in SUPPORTED_ENCODERS.items():
        if model_name.startswith(prefix):
            for from_, to_ in remappings.items():
                kwargs[to_] = kwargs[from_]
                del kwargs[from_]
            model_found = True
            break
    if not model_found:
        logging.warning(
            "Model %s has not been tested with UDTube; it may require special "
            "casing in %s",
            model_name,
            __file__,
        )
    return transformers.AutoModel.from_pretrained(
        model_name, output_hidden_states=True, **kwargs
    )
