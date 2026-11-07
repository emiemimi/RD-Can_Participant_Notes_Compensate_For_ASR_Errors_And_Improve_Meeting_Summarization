from datasets import load_dataset, concatenate_datasets
import pandas

# load the dataset from HuggingFace, concatenate the splits into one dataset
alldata = load_dataset("TalTechNLP/AMIsum", "full", revision="refs/convert/parquet")
concat_splits = concatenate_datasets([alldata["train"], alldata["validation"], alldata["test"]])

# transform it into a pandas dataframe, keeping only the id and trasncript columns
df = concat_splits.to_pandas()[["id", "transcript"]]

# TODO: keep only IDs that start with ES, IS and TS -> regex?

# TODO: for each, print transcription to file named with ID
