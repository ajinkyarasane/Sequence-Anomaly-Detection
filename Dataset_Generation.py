import soundata
import pydub 
import os
import json
import re
import shutil
import pandas as pd
import random
from collections import defaultdict

f = json.load(open(r'/content/gdrive/MyDrive/dev_clips_info_FSD50K.json'))

Train_Sounds_Human = sorted(os.listdir(r'/content/gdrive/MyDrive/Final_Dataset_Train/Human_Sounds'))
Anomaly_Sounds_Ambi = sorted(os.listdir(r'/content/gdrive/MyDrive/Final_Dataset_Anomaly/Ambious_Sounds_Anomaly'))
Anomaly_Sounds_Nature = sorted(os.listdir(r'/content/gdrive/MyDrive/Final_Dataset_Anomaly/Nature_Sounds_Anomaly'))
Anomaly_Sounds_SoT = sorted(os.listdir(r'/content/gdrive/MyDrive/Final_Dataset_Anomaly/Sound_Of_Things_Anomaly'))

op_path = r'/content/gdrive/MyDrive/Human_Base/'

trainpath = r'/content/gdrive/MyDrive/Train/'
ambipath = r'/content/gdrive/MyDrive/Final_Dataset_Anomaly/Ambious_Sounds_Anomaly/'
naturepath = r'/content/gdrive/MyDrive/Final_Dataset_Anomaly/Nature_Sounds_Anomaly/'
sotpath = r'/content/gdrive/MyDrive/Final_Dataset_Anomaly/Sound_Of_Things_Anomaly/'

newdata = defaultdict(list)

def insert(wav1,wav2,freq):
  len1=len(wav1)
  len2=len(wav2)
  t1=random.randint(0,len1-len2*freq)
  t2=t1+len2*freq
  m2 = wav1.overlay(wav2,position=t1,gain_during_overlay=-6,times=freq)
  return m2,t1,t2

count = 0

for s in Train_Sounds_Human:
  wav_file1 = pydub.AudioSegment.from_file(file = trainpath+ s,format = "wav")
  key = str(s.split('.')[0])
  title = f[key]['title']
  title = title.split('.')[0]
  tags = f[key]['tags']
  license = f[key]['license']
  for clip2 in Anomaly_Sounds_Ambi:
    key_anom = str(clip2.split('.')[0])
    title_anom = f[key_anom]['title']
    title_anom = title_anom.split('.')[0]
    tags_anom = f[key_anom]['tags']
    license_anom = f[key_anom]['license']
    wav_file2 = pydub.AudioSegment.from_file(file = ambipath + clip2,format = "wav")
    newdata["Normal_Sound_Key"].append(key)
    newdata["Normal_Sound_Title"].append(title)
    newdata["Normal_Sound_Tags"].append(tags)
    newdata["Normal_Sound_License"].append(license)
    newdata["Anomaly_Sound_Key"].append(key_anom)
    newdata["Anomaly_Sound_Title"].append(title_anom)
    newdata["Anomaly_Sound_Tags"].append(tags_anom)
    newdata["Anomaly_Sound_License"].append(license_anom)
    mixed_clip,start_time,end_time = insert(wav_file1,wav_file2,1)
    new_title = re.sub('[^a-zA-Z0-9 \n\.]', '', title)
    new_title = new_title.replace(' ', '')
    new_title_anom = re.sub('[^a-zA-Z0-9 \n\.]', '', title_anom)
    new_title_anom = new_title_anom.replace(' ', '')
    new_title_dict = new_title + '_' + new_title_anom
    newdata["Name_Of_Mixed"].append(new_title_dict)
    newdata["Anomaly_startTime"].append(start_time)
    newdata["Anomaly_endTime"].append(end_time)
    count +=1 
    print(count,'Exporting to Drive')
    fil=mixed_clip.export( op_path + new_title_dict + ".wav", format="wav")
  
df = pd.DataFrame.from_dict(newdata)
df.to_csv('/content/gdrive/MyDrive/SoT_Base.csv',index = True, header = True)