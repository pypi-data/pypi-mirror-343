# PetHarbor

PetHarbor is a Python package designed for anonymizing datasets using either a pre-trained model or a hash-based approach. It provides two main classes for anonymization: `lite` and `advance`.

We introduce two anonymisation models to address the critical need for privacy protection in veterinary EHRs: PetHarbor Advanced and PetHarbor Lite. These models minimise the risk of re-identification in free-text clinical notes by identifying and pseudonymising sensitive information using custom-built private lists. The models differ by:

**PetHarbor-Advanced:** A state-of-the-art solution for clinical note anonymisation, leveraging an ensemble of two specialised large language models (LLMs). Each model is tailored to detect and process distinct types of identifiers within the text. Trained extensively on a diverse corpus of authentic veterinary EHR notes, these models are adept at parsing and understanding the unique language and structure of veterinary documentation. Due to its high performance and comprehensive approach, PetHarbor Advanced is our recommended solution for data sharing beyond controlled laboratory environments.

![model overview](img/model_diff.png)

**PetHarbor-Lite**: A lightweight alternative to accommodate organisations with limited computational resources. This solution employs a two-step pipeline: first, trusted partners use shared lookup hash list derived from the SAVSNET dataset to remove common identifiers. These hash lists utilise a one-way cryptographic hashing algorithm (SHA-256) with an additional protected salt. Therefore, this hash list can be made available and shared with approved research groups without the need for raw text to be transfered or viewed by end users. Second, a spaCy-based model identifies and anonymises any remaining sensitive information. This approach drastically reduces computational requirements while maintaining effective anonymisation.

## Installation

To install the required dependencies, run:

```bash
pip install petharbor
```

## Quick start
You can simply pass text to the initialise class (maybe slow first down as we download the model):

```
from petharbor.advance import Anonymiser

petharbor = Anonymiser()
petharbor.anonymise("cookie presented to jackson's on 25th May 2025 before travel to hungary. Issued passport (GB52354324)")

# <<NAME>> presented to <<ORG>> on <<TIME>> before travel to <<LOCATION>>. Issued passport (<<MISC>>)

````

n.b This is only advised for testing, see below for how to pass an entire dataset through which will be significantly faster

# Models

## PetHarbor-Advanced Anonymization
The `advance` anonymization class uses a pre-trained model to anonymize text data. Here is an example of how to use it:

## 🛠️ PetHarbor-Advanced Arguments

This script supports the following command-line arguments for dataset loading, model configuration, preprocessing, and output control:

| Argument       | Type              | Default                                                                 | Description                                                                                       |
|----------------|-------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `dataset`      | `str`             | `None`                                                                  | **Required.** Path to the dataset file (e.g., `.csv`, `.arrow`).                                 |
| `split`        | `str`             | `"train"`                                                               | The split of the dataset to use. Typical options include `"train"`, `"test"`, or `"eval"`.       |
| `model`        | `str`             | `"SAVSNET/PetHarbor"`                                                   | Path to the pre-trained model or model identifier from Hugging Face.                             |
| `tokenizer`    | `str`             | `None`                                                                  | Path to the tokenizer. If not specified, defaults to the tokenizer associated with the model.    |
| `text_column`  | `str`             | `"text"`                                                                | Column name in the dataset that contains the text input data.                                    |
| `cache`        | `bool`            | `True`                                                                  | Whether to enable caching of processed datasets to speed up subsequent runs.                     |
| `cache_path`   | `str`             | `"petharbor_cache/"`                                                    | Directory path to store cache files.                                                             |
| `logs`         | `Optional[str]`   | `None`                                                                  | Optional path to save logs generated during processing.                                          |
| `device`       | `str`             | `"cuda"` if available, otherwise `"cpu"`                                | Device to run the model on. Automatically detects GPU if available.                              |
| `tag_map`      | `Dict[str, str]`  | `{ "PER": "<<NAME>>", "LOC": "<<LOCATION>>", "TIME": "<<TIME>>", "ORG": "<<ORG>>", "MISC": "<<MISC>>" }` | A dictionary mapping entity tags to replacement strings. Useful for masking/anonymizing entities. |
| `output_dir`   | `str`             | `None`                                                                  | Directory to save the processed outputs, such as transformed datasets or predictions.            |


### Methods

`annonymise()`: Anonymizes the text data in the dataset.


```python
# example_run.py

from petharbor.advance import Annonymiser

if __name__ == "__main__":
    # Initialize the Annonymiser with your configuration
    advance = Annonymiser(
        dataset="testing/data/out/predictions.csv",  # Path to input dataset
        split="train",                               # Optional: dataset split for arrow(default is "train")
        model="SAVSNET/PetHarbor",                   # Optional: path or name of the model
        text_column="text",                          # Column containing text to process
        cache=True,                                  # Use cache
        cache_path="petharbor_cache/",               # Where to store cache files
        logs="logs/",                                # Path to store logs
        device="cuda",                               # Device to run on: "cuda" or "cpu"
        tag_map={                                     # Entity replacement map
            "PER": "<<NAME>>",
            "LOC": "<<LOCATION>>",
            "TIME": "<<TIME>>",
            "ORG": "<<ORG>>",
            "MISC": "<<MISC>>"
        },
        output_dir="output.csv"  # Where to save anonymised data
    )

    # Run the anonymisation process
    advance.annonymise()

```
## Lite Anonymization
The `lite` anonymization class uses a hash-based approach to anonymize text data. Here is an example of how to use it:


### Arguments
`dataset_path` : (str) The path to the dataset file. Can be a Arrow Dataset (uses the test split) or a .csv file

`hash_table` : (str)  The path to the hash table file.

`salt` : (str), [optional] An optional salt value for hashing (default is None).

`cache` : (bool), [optional] Whether to use caching for the dataset processing (default is True).

`use_spacy` : (bool), [optional] Whether to use spaCy for additional text processing (default is False).

`spacy_model` : (str), [optional]  The spaCy model to use for text processing (default is "en_core_web_sm").

`text_column` : (str), [optional] The name of the text column in the dataset (default is "text").

`output_dir` : (str), [optional]  The directory where the output files will be saved (default is "testing/out/").

### Methods
`annonymise()`: Anonymizes the dataset by hashing the text data and optionally using spaCy for additional processing.
    


### Usage

```python
from petharbor.lite import Annonymiser

lite = Annonymiser(
        dataset="testing/data/test.csv",
        hash_table="petharbor/data/pet_names_hashed.txt",
        salt="savsnet",
        text_column="text",
        cache=True,
        use_spacy=False,
        output_dir="testing/data/out/lite.csv",
    )
lite.annonymise()
```


## Configuration

### Device Configuration

The device (CPU or CUDA) can be configured by passing the `device` parameter to the anonymization classes. If not specified, the package will automatically configure the device.

### Caching

Both methods support caching to avoid re-anonymising records that have already been processed. This makes subsequent runs significantly faster, especially when working with large datasets.

There are two caching options available:

#### **(Recommended)**: `cache={consult ID column}`

If your dataset includes a unique identifier for each consultation (e.g., a consult ID), you can pass this column name to enable ID-based caching. This method logs which records have already been anonymised.

- A folder will be created to store the cache (default: `petharbor_cache/`). You can customize this path using `cache_path={path/to/cache}`.
- The cache stores a list of processed consult IDs.
- On subsequent runs, the model reads this list and skips records whose IDs are already logged.
- **Note**: The cache is stored locally. If you want to re-anonymise a record, you must manually remove its ID from the log.

```cache=True``` : We apply a 'annonymised' flag to the dataset, if a record is marked '1' in this field we skip it, and add it back to the complete dataset at the end.


```cache=False```: No caching. Full dataset processed each time. No consult_ids or 'annonymised' flag is used.

## Logging

Logging is set up using the `logging` module. Logs will provide information about the progress and status of the anonymization process.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.
