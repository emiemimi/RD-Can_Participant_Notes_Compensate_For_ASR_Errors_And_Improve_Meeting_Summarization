from nltk.corpus.reader import XMLCorpusReader


# TODO: use sys argv to get paths and filenames
#  i want to run this script from a shell file, or manually
INPUT_DATA = ""
INPUT_FILE_IDS = []
OUTPUT_DATA = ""


reader = XMLCorpusReader(INPUT_DATA, INPUT_FILE_IDS)

for file in FILE_IDS:
    root = reader.xml(FILE_IDS[file]).getroot()
    tokens = []
    for element in root.iter("w"):
        token = "".join(element.itertext()).strip()
        if not token:
            continue
        if element.get("punc") == "true" and tokens: # add punctuation to the previous word, if any
            tokens[-1] += token
        else:
            tokens.append(token)

    text = " ".join(tokens)
    # TODO:
    #  manage ouput file name according to input file name
    #  manage file paths
    #  test
    with open("file_name.txt", "w", encoding="utf-8") as file:
        file.write(text)