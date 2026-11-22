import os

import pandas as pd
import werpy


def get_text(path):
    with open(path, "r") as f:
        return f.read()


if __name__ == "__main__":
    id_list = os.listdir("../downloads/signals/amicorpus")
    clean_dir = "../data/clean_transcriptions/"
    noisy_dir = "../data/whisper_transcriptions/noisy/"

    lst = []

    for id in id_list:
        clean = os.path.join(clean_dir, id + ".txt")
        noisy_sub_dir = os.path.join(noisy_dir, id, "transcripts")
        noisy_transcripts = os.listdir(noisy_sub_dir)
        for transcript in noisy_transcripts:
            noisy = os.path.join(noisy_sub_dir, transcript)
            full_id = id + transcript.split("-")[-1].split(".")[0] # ex: "ES2002a.Array1-01.txt" -> "ES2002a01"

            # normalize(text): Unicode Normalization Form C,
            # remove ASCII and Unicode punctuation,
            # remove duplicated spaces, leading/trailing blanks
            # and convert all words to lowercase.
            ref = werpy.normalize(get_text(clean))
            hyp = werpy.normalize(get_text(noisy))

            # pandas DataFrame breakdown of the calculated results including the WER, Levenshtein Distance
            # and all the insertion, deletion and substitution errors.
            summary = werpy.summary(ref, hyp)
            summary.index = pd.Index([full_id])
            lst.append(summary)

    result = pd.concat(lst)
    result.to_csv("../analysis/wer_clean_vs_whisper.csv")
