import os
from nltk.corpus.reader import XMLCorpusReader
import nltk.data


def filter_files(file_list, id_list):
    return [file for file in file_list if file.split(".")[0] in id_list]

def extract_lines(xml_file_root, tag):
    summary = xml_file_root.find(tag)
    return [sent.text for sent in summary.findall("sentence")]

def print_to_file(id, lines, path):
    file = os.path.join(path, id + ".txt")
    with open(file, "w") as f:
        for line in lines:
            f.write(line + "\n")


if __name__ == "__main__":

    input_dir = "../downloads/ami_public_manual_1.6.2/abstractive"
    output_dir = "../data/gold_summaries"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    id_list = os.listdir("../downloads/signals/amicorpus")
    files = filter_files(os.listdir(input_dir), id_list)
    nltk.data.path.append(input_dir)
    reader = XMLCorpusReader(input_dir, files)

    n = len(files)
    for i in range(n):
        print(f"Processing {i+1}/{n} files")
        sentences = extract_lines(reader.xml(files[i]), "abstract")
        id = files[i].split(".")[0]
        print_to_file(id, sentences, output_dir)