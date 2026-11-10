"""
downloads the clean transcriptions from a Hugging Face dataset,
filters it: keep only the meeting ids we have audio for
for each transcription: removes speaker tags, segments into sentences and writes it to its own file
"""

from datasets import load_dataset, concatenate_datasets
import os
import re
import nltk


def get_data_as_df():
    """load the dataset from HuggingFace, concatenate the splits into one dataset, and return id and transcript coloums in a pandas dataframe"""
    alldata = load_dataset("TalTechNLP/AMIsum", revision="refs/convert/parquet")
    concat_splits = concatenate_datasets([alldata["train"], alldata["validation"], alldata["test"]])
    return concat_splits.to_pandas()[["id", "transcript"]]

def filter_df_by_ids(df, lst):
    return df[df["id"].isin(lst)].reset_index(drop=True)

def remove_speaker_tags(text):
    return re.sub(r"<[A-Z]{2}>\s", "", text)

def segment_into_sentences(text):
    return nltk.sent_tokenize(text)

def print_to_file(id, lines, path):
    file = os.path.join(path, id + ".txt")
    with open(file, "w") as f:
        for line in lines:
            f.write(line + "\n")


if __name__ == "__main__":

    output_dir = "../downloads/clean_transcriptions"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    df_all = get_data_as_df()
    id_list = os.listdir("../downloads/signals/amicorpus")
    df = filter_df_by_ids(df_all, id_list)

    for id, transcription in df.itertuples(index=False, name=None):
        clean = remove_speaker_tags(transcription)
        clean_sentences = segment_into_sentences(clean)
        print_to_file(id, clean_sentences, output_dir)