import pandas as pd

import os

import pdb

import monk


def get_valid_files(root, patterns):
    valid_files = []
    this_path = os.walk(root)
    for pattern in patterns:
        for path, subdirs, files in this_path:
            for name in files:
                if pattern in os.path.join(path, name):
                    valid_files.append(os.path.join(path, name))

    return valid_files


def lines_parser(lines):
    lines = [line.replace('\n','') for line in lines if line != "\n"]
    return lines


def record_extractor(lines,topic, df):
    new_row = {"topics": topic,"tags": None, "content": [], "notes": []}
    for line in lines:
        # print("start",line)
        if line.startswith("--"):
            # print('if')
            if new_row["tags"] != None:
                df = df.append(new_row, ignore_index=True)
                new_row = {"topics":topic, "tags": None, "content": [], "notes": []}

            new_row["tags"] = line[2:]

        elif line.startswith("-") and not line.startswith("--"):
            # print('elif')
            new_row["content"] += [line]
        else:
            # print('else')
            try:
                new_row["notes"] += [line]
            except:
                "No proper line"

        # print(new_row)
    return df


def get_data(paths):
    df = pd.DataFrame({"topics": [],"tags":[], "content":[], "notes":[]})
    print(paths)
    for doc in paths:
        with open(doc) as f:
            try:
                lines = f.readlines()
            except:
                print('couldnt load file')
                pass


        lines = lines_parser(lines)
        topic_name = os.path.basename(doc)[:-4]
        df = record_extractor(lines, topic_name,df)

    return df

if __name__ == '__main__':
    DATA ="./data"
    TXT = os.listdir(DATA)
    pd.options.display.max_colwidth = 1400
    PATTERN = [".txt"]
    SEARCH_ROOT = "./data"
    print(get_valid_files(DATA, PATTERN))
    df = get_data(get_valid_files(DATA, PATTERN))









#

#

#



#

# #topic=["baking"], notes=["bake"],  content=["Until"]

# #searcher.search_topic(df, topic=["baking"])

# #monk.search(topic=["baking"])

# #monk.search(df, notes=["bake"])
