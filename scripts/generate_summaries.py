import os
import ollama
import json
from nltk import sent_tokenize


MODEL = "llama3.1:8b-instruct-q4_K_M"
# average sentences in gold summaries is 7.86, ranging from 3 to 13
SYSTEM_PROMPT = ("User will provide a meeting transcription, maybe also meetings notes."
                 "Answer only with an abstract summary based on the provided input."
                 "The summary must not be shorter than 3 sentences, nor longer than 13 sentences.")

CLEAN_DIR = "../data/clean_transcriptions"
NOISY_DIR = "../data/whisper_transcriptions/noisy"
NOTES_DIR = "../data/participant_notes"
OUTPUT_DIR = "../data/generated_summaries"

ID_LIST = os.listdir("../downloads/signals/amicorpus")


def get_text(path):
    with open(path, "r") as f:
        return f.read()

def write_file(path, txt):
    with open(path, "w") as f:
        f.write("\n".join(txt))

def call_llm(transcription, notes=None):
    schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"}
        },
        "required": ["summary"],
        "additionalProperties": False
    }
    if notes:
        input_content = (f"TRANSCRIPT:\n{transcription}\n\n"
                         f"MEETING NOTES:\n{notes}")
    else:
        input_content = f"TRANSCRIPT:\n{transcription}"
    response = ollama.chat(
        model = MODEL,
        messages = [
            {"role": "system","content": SYSTEM_PROMPT},
            {"role": "user","content": f"{input_content}"}
        ],
        format = schema
    )
    summary = json.loads(response.message.content)["summary"]
    return sent_tokenize(summary)

def make_summary(file_name, path, transcript_path, notes_path=None):
    print("Working on", file_name)
    transcript = get_text(transcript_path)
    if notes_path is not None:
        note = get_text(notes_path)
        if len(note) >= 1:
            summary = call_llm(transcript, note)
            write_file(path, summary)
    else:
        summary = call_llm(transcript)
        write_file(path, summary)


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    """test = 1"""
    for id in ID_LIST:
        """
        if test <= 0:
            break
        test -= 1
        """
        notes_sub_dir = os.path.join(NOTES_DIR, id)
        has_notes = os.path.exists(notes_sub_dir)

        summary_id = f"{id}_clean.txt"
        output_path = os.path.join(OUTPUT_DIR, summary_id)
        clean_transcript_path = os.path.join(CLEAN_DIR, id + ".txt")
        if not os.path.exists(output_path):
            make_summary(summary_id, output_path, clean_transcript_path)

        if has_notes:
            for p_notes in os.listdir(notes_sub_dir):
                note_id = p_notes.split(".")[1]
                summary_id = f"{id}_clean_{note_id}.txt"
                output_path = os.path.join(OUTPUT_DIR, summary_id)
                if not os.path.exists(output_path):
                    notes_path = os.path.join(notes_sub_dir, p_notes)
                    make_summary(summary_id, output_path, clean_transcript_path, notes_path)

        noisy_sub_dir = os.path.join(NOISY_DIR, id, "transcripts")
        noisy_transcripts = os.listdir(noisy_sub_dir)
        for noisy in noisy_transcripts:
            noisy_id = noisy.split(".")[-2].split("-")[-1]
            summary_id = f"{id}_noisy{noisy_id}.txt"
            output_path = os.path.join(OUTPUT_DIR, summary_id)
            noisy_transcript_path = os.path.join(noisy_sub_dir, noisy)
            if not os.path.exists(output_path):
                make_summary(summary_id, output_path, noisy_transcript_path)

            if has_notes:
                for p_notes in os.listdir(notes_sub_dir):
                    note_id = p_notes.split(".")[1]
                    summary_id = f"{id}_noisy{noisy_id}_{note_id}.txt"
                    output_path = os.path.join(OUTPUT_DIR, summary_id)
                    if not os.path.exists(output_path):
                        notes_path = os.path.join(notes_sub_dir, p_notes)
                        make_summary(summary_id, output_path, noisy_transcript_path, notes_path)