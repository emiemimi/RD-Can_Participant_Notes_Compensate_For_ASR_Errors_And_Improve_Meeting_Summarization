import os
import nltk
import pandas as pd


def get_text(path):
    with open(path, "r") as f:
        return f.read()

def word_len(txt):
    return len(nltk.word_tokenize(txt))

def sent_len(txt):
    return len(nltk.sent_tokenize(txt))

def calculate_stats(id, text):
    return {"meeting_id": id,
            "words": word_len(text),
            "sentences": sent_len(text)}

if __name__ == "__main__":
    id_list = os.listdir("../downloads/signals/amicorpus")
    summaries_dir = "../data/gold_summaries/"

    rows = []

    for id in id_list:
        summary = os.path.join(summaries_dir, id + ".txt")
        txt = get_text(summary)
        stats = calculate_stats(id, txt)
        rows.append(stats)

    result = pd.DataFrame(rows)
    result.to_csv("../analysis/stats_summaries.csv")