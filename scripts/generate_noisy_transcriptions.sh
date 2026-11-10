#!/usr/bin/env bash

BASE_INPUT_DIR="../downloads/signals/amicorpus/"
BASE_OUTPUT_DIR="../whisper_transcriptions/noisy/"

for meeting_dir in "$BASE_INPUT_DIR"/*; do
  meeting_id="${meeting_dir##*/}"
  for file in "$meeting_dir"/audio/*; do
    OUTPUT_DIR="$BASE_OUTPUT_DIR/$meeting_id/transcripts"
    printf "Transcribing %s \n" "$file"
    whisper "$file" \
      --model tiny.en \
      --output_format txt \
      --output_dir "$OUTPUT_DIR" \
      --verbose False
  done
done
