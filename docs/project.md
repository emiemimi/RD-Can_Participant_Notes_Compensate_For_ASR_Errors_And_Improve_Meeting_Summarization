# Research question
Can participant notes compensate for ASR errors and improve meeting summarization?

# Data:
- gold: AMI_abstractive_summaries
- clean: AMI_transcriptions
- noisy: ASR transcriptions of AMI audios*
- notes: AMI_participant_summaries

# Tools:
- ASR: whisper tiny**
- summarisation tool: LLM to be defined***, with a fixed prompt

# Tasks:
- generate transcriptions, and evaluate the WER of noisy vs clean, ie. analyse the noisiness
- parse AMI_abstractive_summaries and AMI_participants_notes to keep text only
- generate summaries on:
  - clean only (as a baseline?)
  - clean + notes (for extra comparison only?)
  - noisy only
  - noisy + notes
- evaluate with different ROUGE scores*** and BERTScore
- analyse errors:
  - do they correlate with ASR errors
  - are there hallucinations
  - etc. ?
- if time allows it: 
  - (small) manual human evaluation ****
  - evaluate with the 2021 Fabbri et al's toolkit
  - evaluate with the 2025 Kirstein et al's LLM-based MESA 

# Future work:
  - expand to more meeting real data (non scenario-based)
  - expand to different domains: recorded lectures and student notes
  - expand to other languages
  - expand to different speech types (aphasia dataset, dyslexia, etc.)
  - expand to different note types
  - query-based / Q&A evaluation methods
  - RoSE atomic content unit evaluation method, sentence-level semantic similarity, maximal marginal relevance

***

\* I still need to chose what signals to use: array1 or array2 ?

** I do not know yet if I should use the flag "condition_on_previous_text False" or not

*** The model(s) will be chosen according to its size (the smaller the better to run), its cost, and its maximum input length

**** I haven't yet decided which ROUGE metrics to use: ROUGE-1, ROUGE-2, ROUGE-SU4, etc.

***** I need to find guidelines on how one should evaluate a summary
