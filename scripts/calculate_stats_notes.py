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

def calculate_stats(id, p_id, text):
    return {"meeting_id": id,
            "participant_id": p_id,
            "words": word_len(text),
            "sentences": sent_len(text)}

if __name__ == "__main__":
    id_list = os.listdir("../downloads/signals/amicorpus")
    notes_dir = "../data/participant_notes/"

    rows = []

    for id in id_list:
        notes_sub_dir = os.path.join(notes_dir, id)
        if os.path.exists(notes_sub_dir):
            for p_notes in os.listdir(notes_sub_dir):
                notes = os.path.join(notes_sub_dir, p_notes)
                txt = get_text(notes)
                participant = p_notes.split(".")[1]
                stats = calculate_stats(id, participant, txt)
                rows.append(stats)
        else:
            txt = ""
            participant = None
            stats = calculate_stats(id, participant, txt)
            rows.append(stats)

    result = pd.DataFrame(rows)
    result.to_csv("../analysis/stats_notes.csv")