import pandas as pd
import imp
import os

import pdb

import monk


def get_valid_files(root, patterns, vrb=False):
    valid_files = []
    # can only be interated once
    this_path = os.walk(root)
    for path, subdirs, files in this_path:
        for name in files:
            for pattern in patterns:
                if pattern in os.path.join(path, name):
                    valid_files.append(os.path.join(path, name))

    if vrb:
        print("Info: loading from files: ", valid_files)

    return valid_files


def lines_parser(lines):
    lines = [line.replace('\n','') for line in lines if line != "\n"]
    return lines


def record_extractor(lines,doc, df, vrb=False):

    #topic = os.path.basename(doc)[:-4]
    topic = doc[-max(len(doc), 40):]

    if vrb:
        print(lines, topic)

    new_row = {"topics": topic,"tags": None, "content": []}
    for i, line in enumerate(lines):

        # append at last line
        if (i == len(lines)-1) and (new_row["tags"] != None):
            df = df.append(new_row, ignore_index=True)

        elif line.startswith("--"):
            if new_row["tags"] != None:
                df = df.append(new_row, ignore_index=True)
                new_row = {"topics":topic, "tags": None, "content": []}

            new_row["tags"] = line[2:]

        elif line.startswith("-") and not line.startswith("--"):
            new_row["content"] += [line]
        else:
            try:
                pass
            except:
                print("No proper line")

    return df


def get_data(paths, vrb=False):
    df = pd.DataFrame({"topics": [],"tags":[], "content":[]})
    for doc in paths:
        with open(doc) as f:
            try:
                lines = f.readlines()
            except:
                print('couldnt load file')
                pass


        lines = lines_parser(lines)
        df = record_extractor(lines, doc,df, vrb=vrb)

    return df

if __name__ == '__main__':
    DATA ="./data"
    TXT = os.listdir(DATA)

    pd.set_option('display.max_columns', 100)  # or 1000
    pd.set_option('display.max_rows', 100)  # or 1000
    pd.set_option('display.max_colwidth', 2000)  # or 199
    pd.set_option('display.width', 2000)  # or 199

    PATTERN = ["xs1", "xs2"]
    df = get_data(get_valid_files(DATA, PATTERN, vrb=True), vrb=True)








