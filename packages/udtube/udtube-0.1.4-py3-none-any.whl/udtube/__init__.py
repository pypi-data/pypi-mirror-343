"""UDTube: a neural morphological analyzer.

This module just silences some uninformative warnings.
"""

import os
import warnings

# Silences tokenizers warning about forking.
os.environ["TOKENIZERS_PARALLELISM"] = "false"

warnings.filterwarnings(
    "ignore", ".*does not have many workers which may be a bottleneck.*"
)
warnings.filterwarnings(
    "ignore", ".*Couldn't infer the batch indices fetched from.*"
)
