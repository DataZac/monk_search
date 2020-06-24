import pandas as pd

import pdb

import load_data

from tabulate import tabulate

from pprint import pprint

import collections

def filter_topics(df, topics):
    df_aux = pd.DataFrame()
    for topic in topics:
        df_aux = df_aux.append(df.loc[df.topics.str.contains(topic)])
    return df_aux


def filter_tags(df, tags):
    df_aux = pd.DataFrame()
    for i, row in df.iterrows():
        for tag in tags:
            if tag in row["tags"]:
                df_aux = df_aux.append(row)
                break
    return df_aux


def filter_content(df, content):
    df_aux = pd.DataFrame()
    for i, row in df.iterrows():
        found = False
        for entry in row.content:
            for record in content:
                if record in entry:
                    # print('hit')
                    found = True
                    break
        if found == True:
            df_aux = df_aux.append(row)

    return df_aux


def filter_notes(df, notes):
    df_aux = pd.DataFrame()
    for i, row in df.iterrows():
        found = False
        for entry in row.notes:
            for note in notes:
                if note in entry:
                    # print('hit')
                    found = True
                    break

        if found == True:
            df_aux = df_aux.append(row)

    return df_aux


def search(df, **kwargs):
    if not kwargs:
        print('Please provid any combination of search kvarg(s): topics, tags, content and/or notes')

    for k,v in kwargs.items():
        print("Searching for:",k,v)

    # topics filtered first, and than passed to other searches > topic AND ( X OR Y .. Or W)
    if "topics" in kwargs.keys():
        if len(kwargs['topics']) > 0:
            df_topics = filter_topics(df,kwargs['topics'])
        else:
            df_topics = df

    topics_seach = False
    tags_seach = False
    content_seach = False
    notes_seach = False

    if "tags" in kwargs.keys():
        if len(kwargs['tags']) > 0:
            tags_seach = True
            df_tags = filter_tags(df_topics,kwargs['tags'])
        else: df_tags = pd.DataFrame({"topics": [],"tags":[], "content":[], "notes":[]})

    if "content" in kwargs.keys():
        if len(kwargs['content']) > 0:
            content_seach = True
            df_content = filter_content(df_topics,kwargs['content'])
        else: df_content = pd.DataFrame({"topics": [],"tags":[], "content":[], "notes":[]})

    if "notes" in kwargs.keys():
        if len(kwargs['notes']) > 0:
            notes_seach = True
            df_notes = filter_notes(df_topics,kwargs['notes'])
        else: df_notes = pd.DataFrame({"topics": [],"tags":[], "content":[], "notes":[]})

    # check if searched for detailed categories
    other_than_topic = False
    for search_field in [df_tags, df_content, df_notes]:
        if search_field.shape[0] > 0 :
            other_than_topic = True

    print(df.shape[0], df_topics.shape[0])
    print("other than topic", other_than_topic)
    # return joined seach df's ( each filtered by detailed cats)
    if other_than_topic:
        x = df_tags.append(df_content).append(df_notes)
        return x.loc[~x.index.duplicated(keep="first")][["topics","tags", "content", "notes"]]


    # case no search match (search frame == base frame) -> retrn no result
    # catch case when frame was already with no result
    elif (df.shape[0] == df_topics.shape[0]) and (True in [topics_seach, tags_seach, notes_seach, content_seach]):
        print("here")
        return pd.DataFrame({"topics": ["no result"],"tags":["no result"], "content":["no result"], "notes":["no result"]})

    # successfull search
    else:
        return df_topics[["topics","tags", "content", "notes"]]


if __name__ == '__main__':
    PATTERN = [".txt"]
    SEARCH_ROOT = "./"

    pd.set_option('display.max_columns', 5)  # or 1000
    pd.set_option('display.max_rows', 100)  # or 1000
    pd.set_option('display.max_colwidth', 50)  # or 199
    pd.set_option('display.width', 200)  # or 199

    df = load_data.get_data(load_data.get_valid_files(SEARCH_ROOT, PATTERN))
    d1 = search(df, topics=[], tags=[""], content=[], notes=[])