import pandas as pd
import textwrap
import pdb

class PrettyShower:

    def __init__(self):
        self.a = 3


    def show(self, df):

        for i, row in df.iterrows():

            topic_length = 45
            tag_length = 45
            topic =  self.get_fixed_width_string(row['topics'], topic_length)
            tag =  self.get_fixed_width_string(row['tags'], tag_length)

            preferredWidth = 240
            prefix_length = topic_length + tag_length
            four_spaces = " "*4
            prefix = topic + four_spaces + tag + four_spaces
            subsequent_indent = ' '*len(prefix)

            wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth,
                                   subsequent_indent=subsequent_indent)
            message = ""
            for part in row['content']:
                message += " "
                message += part
            #pdb.set_trace()
            print(wrapper.fill(message))

    def get_fixed_width_string(self, text, length):
        text =  (' ...' + text[-length+4:]) if len(text) > length-4 else text
        formatter = "{0:<" + str(length) +"}"
        return formatter.format(text)



if __name__ == '__main__':
    df = pd.DataFrame({"topics": ["./data\docker_test_xs2.txt"],"tags":["383838"],"content":["hu"]})
    print(df.head(2))
    Prtyshwr = PrettyShower()
    Prtyshwr.show(df)