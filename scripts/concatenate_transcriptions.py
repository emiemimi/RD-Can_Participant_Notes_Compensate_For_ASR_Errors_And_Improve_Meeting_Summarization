"""
for each meeting id (ex: "ES2022a") this script fetches all its part transcriptions and combines them into one file
all output files are stored in the directory "full_transcriptions"
"""

import os

def combine_transcriptions(id, transcripts_dir, output_dir):
    print("Combining transcriptions for", id)
    output_file = os.path.join(output_dir, id + ".txt")
    with open(output_file, "w") as f:
        for file_name in sorted(os.listdir(transcripts_dir)):
            print("\tAdding transcription", file_name)
            f.writelines(fetch_transcript_lines(transcripts_dir, file_name))

def fetch_transcript_lines(dir, name):
    file = os.path.join(dir, name)
    with open(file, "r") as f:
        return f.readlines()

if __name__ == "__main__":

    path = "../whisper_transcriptions/noisy/"
    meeting_ids = os.listdir(path)

    transcriptions_dir = os.path.join(path, "full_transcriptions")
    if not os.path.exists(transcriptions_dir):
        os.mkdir(transcriptions_dir)

    for meeting in meeting_ids:
        subdir = os.path.join(path, meeting, "transcripts")
        combine_transcriptions(meeting, subdir, transcriptions_dir)