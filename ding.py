import os
import json
import random

import pandas as pd
import numpy as np

import matplotlib
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt

path = '/Users/leepeter/myFonts/Noto_Sans_TC/NotoSansTC-Regular.otf'
prop = font_manager.FontProperties(fname=path)
print(prop.get_name())
matplotlib.rcParams['font.family'] = prop.get_name()


def random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def convert_fb_str(s):
    return s.encode('latin1').decode('utf8')

root_path = './messages/inbox/dizhishuangbi_lxlgbqmybg'
directory = os.listdir(root_path)

value = []
index = []

SENDER = '丁凱元'
#DIRTY_WORD_SET = ['廢物', '嫩', '低能兒', '阿嬤', '白癡', '想幹', '想揉']
#DIRTY_WORD_SET = ['好照', '涵薏']
DIRTY_WORD_SET = ['廢物', '低能', '阿嬤', '我媽', '我弟']

# Init dataframe
dataset = {}
for dirty_word in DIRTY_WORD_SET:
    dataset[dirty_word] = []

for fn in directory:
    if not fn.endswith('.json'):
        continue
    with open(os.path.join(root_path, fn), 'r') as f:
        data = json.load(f)
        for msg in data['messages']:
            if convert_fb_str(msg['sender_name'])==SENDER:
                value.append(1)
                index.append(msg['timestamp_ms'])

                if 'content' not in msg:
                    continue

                for dirty_word in DIRTY_WORD_SET:
                    if dirty_word in convert_fb_str(msg['content']):
                        #dataset[dirty_word].append((msg['timestamp_ms'], convert_fb_str(msg['content'])))
                        dataset[dirty_word].append((msg['timestamp_ms'], 1))
df_dataset = []
for dirty_word, data in dataset.items():
    tmp_df = pd.DataFrame(dataset[dirty_word], columns=['ms', dirty_word])
    tmp_df = tmp_df.set_index(tmp_df['ms'])
    del tmp_df['ms']
    tmp_df = tmp_df.set_index(pd.to_datetime(tmp_df.index, unit='ms'))
    tmp_df = tmp_df.resample('M').sum()
    df_dataset.append(tmp_df)


fig, ax = plt.subplots()

for i in range(len(df_dataset)):
    ax.plot_date(df_dataset[i].index, df_dataset[i].values, '-', color=random_color(),
                 label=df_dataset[i].columns[0])

plt.legend(prop=prop)
plt.show()

#plt.legend()
#plt.show()

#index = pd.to_datetime(index, unit='ms')
#sindex = pd.to_datetime(spi, unit='ms')

#ts = pd.Series(value, index=index)
#ts = ts.resample('1D').sum()

#ax = df.plot.bar()
#sts.plot()
#plt.show()

#plt.plot(ts.resample('1D').sum(), kind='bar')
#plt.show()

