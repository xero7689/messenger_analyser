import os
import json
import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

from utils import *

font_path = '/Users/leepeter/myFonts/Noto_Sans_TC/NotoSansTC-Regular.otf'
prop = font_manager.FontProperties(fname=font_path)

root_path = './messages/inbox/dizhishuangbi_lxlgbqmybg'
directory = os.listdir(root_path)


class MessageTherad:
    def __init__(self):
        self.participants = {}
        for fn in os.listdir(root_path):
            if not fn.endswith('json'):
                continue
            with open(os.path.join(root_path, fn), 'r') as f:
                data = json.load(f)

                # Initialize Participants
                for participant in data['participants']:
                    participant = convert_fb_str(participant['name'])
                    if participant not in self.participants:
                        self.participants[participant] = {
                            'messages': [],
                            'timestamps': []
                        }
                
                # Initialize Timeseries
                for message in data['messages']:
                    if 'content' not in message:
                        continue
                    sender = convert_fb_str(message['sender_name'])
                    self.participants[sender]['messages'].append(convert_fb_str(message['content']))
                    self.participants[sender]['timestamps'].append(message['timestamp_ms'])
        
        frame = {}
        for participant, _ in self.participants.items():
            time_index = pd.to_datetime(self.participants[participant]['timestamps'], unit='ms')
            time_series = pd.Series(self.participants[participant]['messages'], 
                                    index = time_index)
            self.participants[participant]['series'] = time_series
            frame[participant] = time_series
        self.frame = pd.DataFrame(frame)

    def participant_total_message(self):
        for participant in self.participants.keys():
            print("[{}] {}".format(participant, len(self.participants[participant]['series'])))

    def plot_participant_activity(self):
        fig, ax = plt.subplots()
        ax.set_facecolor(ColorScheme.gruvbox.fg)
        for participant in self.participants.keys():
            cs = self.participants[participant]['series'].copy()
            cs[:] = 1
            cs = cs.resample('W').sum()
            ax.plot_date(cs.index, 
                         cs.values, 
                         '-', color=random_color(),
                         label=participant)
        plt.legend(prop=prop)
        plt.show()

if __name__ == '__main__':
    thread = MessageTherad()

    # Use jieba
    import jieba
    import jieba.posseg as pseg
    jieba.load_userdict('./dict.txt')
    jieba.enable_parallel(4)
    jieba.initialize()
    jieba.enable_paddle()

    """
    # WordCloud
    from wordcloud import WordCloud
    wordcloud = WordCloud(font_path=font_path)
    wordcloud = WordCloud(font_path=font_path).generate(words)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    history
    """

    #thread.participant_total_message()
    #thread.plot_participant_activity()
