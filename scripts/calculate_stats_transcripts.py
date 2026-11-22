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

def calculate_stats(id, t_id, text):
    return {"meeting_id": id,
            "transcript_id": t_id,
            "words": word_len(text),
            "sentences": sent_len(text)}

if __name__ == "__main__":
    id_list = os.listdir("../downloads/signals/amicorpus")
    clean_dir = "../data/clean_transcriptions/"
    noisy_dir = "../data/whisper_transcriptions/noisy/"
    notes_dir = "../data/participant_notes"

    rows = []

    for id in id_list:
        clean = os.path.join(clean_dir, id + ".txt")
        noisy_sub_dir = os.path.join(noisy_dir, id, "transcripts")
        noisy_transcripts = os.listdir(noisy_sub_dir)
        all_paths = [clean] + [os.path.join(noisy_sub_dir, noisy) for noisy in noisy_transcripts]

        notes_sub_dir = os.path.join(notes_dir, id)
        if os.path.exists(notes_sub_dir):
            nb_speakers = len(os.listdir(notes_sub_dir))
        else:
            nb_speakers = None

        for transcript in all_paths:
            txt = get_text(transcript)
            transcript_id = transcript.split(".")[-2].split("-")[-1]
            if len(transcript_id) > 2:
                transcript_id = "clean"
            stats = calculate_stats(id, transcript_id, txt)
            stats["nb_speakers"] = nb_speakers
            rows.append(stats)

    result = pd.DataFrame(rows)
    result.to_csv("../analysis/stats_transcripts.csv")