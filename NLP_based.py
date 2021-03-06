# -*- coding: utf-8 -*-
"""Copy of 1DCNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t6D6Sr2hbvYw-SQn8qeMQJkHYboxTOfT
"""

# This is the NLP approach
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import librosa
import panns_inference
from panns_inference import AudioTagging, SoundEventDetection, labels
import torch
import torch.nn as nn
import torch.optim as optim
import torch.cuda.amp as amp
from sklearn.metrics import accuracy_score
import os

transent= SentenceTransformer('all-MiniLM-L6-v2')
emb=transent.encode(labels)

from google.colab import drive

drive.mount("/content/gdrive", force_remount=True)
#

"""

*   Ambi pann - 1329
*   Human pann - 2115
*   Music pann - 970
*   Nature pann - 1625
*   SoT pann - 10152
*   Animal pann - 1654



"""

#below commented code is to bring data to your disk
#you can change paths according to your wish however they must be consistent through out the code
# ! cp /content/gdrive/MyDrive/Train_data.csv .
# ! cp /content/gdrive/MyDrive/vocabulary.csv .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/Ambi_pann.zip .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/Human_pann.zip .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/Music_pann.zip .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/Nature_pann.zip .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/SoT_pann-001.zip .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/SoT_pann-002.zip .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/SoT_pann-003.zip .
# ! cp /content/gdrive/MyDrive/New-FSD50K-Dataset/Animal_pann.zip .

# ! unzip Ambi_pann.zip
# ! unzip Animal_pann.zip
# ! unzip Human_pann.zip
# ! unzip Music_pann.zip
# ! unzip Nature_pann.zip
# ! unzip SoT_pann-001.zip -d /content/content/gdrive/MyDrive/New-FSD50K-Dataset
# ! unzip SoT_pann-002.zip -d /content/content/gdrive/MyDrive/New-FSD50K-Dataset
# ! unzip SoT_pann-003.zip -d /content/content/gdrive/MyDrive/New-FSD50K-Dataset

df=pd.read_csv("/content/Train_data.csv")

df=df.iloc[:,1:]

import os
Ambi_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Ambi_pann"))
Animal_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Animal_pann"))
Human_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Human_pann"))
Music_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Music_pann"))
Nature_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Nature_pann"))
SoT_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/SoT_pann"))
x_vec=[]
X_path="/content/content/gdrive/MyDrive/New-FSD50K-Dataset/"
for j,i in df.Fname.iteritems():
  k=i+".npy"
  if k in Ambi_Npy:
    x_vec.append(i)
  if k in Animal_Npy:
    x_vec.append(i)
  if k in Human_Npy:
    x_vec.append(i)
  if k in Music_Npy:
    x_vec.append(i)
  if k in Nature_Npy:
    x_vec.append(i)
  if k in SoT_Npy:
    x_vec.append(i)

del Ambi_Npy
del Animal_Npy
del Human_Npy
del Music_Npy
del Nature_Npy
del SoT_Npy

vocab=pd.read_csv("/content/vocabulary.csv",header=None)

vocab.columns=["ind","tags","ids"]

vocab["tags"]=vocab["tags"].str.lower()

hot=[]
for i,k in df.Anomaly_Sound_Audioset_Tags.iteritems():
  ones=[0 for z in range(200)]
  for j in k.lower().split(","):
    row_nos=vocab["tags"][vocab["tags"]==j].index
    for t in row_nos:
      ones[t]=1  
  hot.append(ones)

True_Natural = ['Wind','Thunderstorm','Thunder','Water','Rain','Raindrop','Stream','Ocean','Waves_and_surf','Gurgling','Fire']

True_Ambigous = ['Hiss','Chirp_and_tweet','Buzz','Rattle','Crackle','Knock','Tap','Squeak','Tick','Crack','Whoosh_and_swoosh_and_swish','Thump_and_thud','Crushing','Crumpling_and_crinkling','Tearing',
'Screech']

True_Hs  = ['Human_voice','Speech','Male_speech_and_man_speaking','Female_speech_and_woman_speaking','Child_speech_and_kid_speaking','Conversation','Speech_synthesizer', \
    'Shout','Yell','Screaming','Whispering','Laughter','Giggle','Chuckle_and_chortle','Crying_and_sobbing','Sigh','Singing','Male_singing','Female_singing','Respiratory_sounds', \
    'Breathing','Gasp','Cough','Sneeze','Run','Walk_and_footsteps','Chewing_and_mastication','Burping_and_eructation','Fart','Hands','Finger_snapping','Clapping','Human_group_actions','Cheering', \
    'Applause','Chatter','Crowd']

True_SoT = ['Cowbell','Bell','Church_bell','Bicycle_bell','Chime','Wind_chime','Vehicle','Boat_and_Water_vehicle','Motor_vehicle_(road)','Car','Vehicle_horn_and_car_horn_and_honking', \
    'Car_passing_by','Race_car_and_auto_racing','Truck','Bus','Motorcycle','Traffic_noise_and_roadway_noise','Rail_transport','Train','Subway_and_metro_and_underground', \
    'Aircraft','Fixed-wing_aircraft_and_airplane','Bicycle','Skateboard','Engine','Engine_starting','Idling','Accelerating_and_revving_and_vroom','Domestic_sounds_and_home_sounds', \
    'Door','Doorbell','Sliding_door','Slam','Cupboard_open_or_close','Drawer_open_or_close','Dishes_and_pots_and_pans','Cutlery_and_silverware','Frying_(food)','Microwave_oven', \
    'Water_tap_and_faucet','Sink_(filling_or_washing)','Bathtub_(filling_or_washing)','Toilet_flush','Zipper_(clothing)','Keys_jangling','Coin_(dropping)','Packing_tape_and_duct_tape','Scissors', \
    'Typing','Typewriter','Computer_keyboard','Writing','Alarm','Telephone','Ringtone','Siren','Mechanisms','Ratchet_and_pawl','Clock','Tick-tock','Mechanical_fan','Printer', \
    'Camera','Tools','Hammer','Sawing','Power_tool','Drill','Explosion','Gunshot_and_gunfire','Fireworks','Boom','Wood','Glass','Chink_and_clink','Shatter','Liquid','Splash_and_splatter', \
    'Drip','Pour','Trickle_and_dribble','Fill_(with_liquid)','Boiling']

True_A = ['Animal','Domestic_animals_and_pets','Dog','Bark','Growling','Cat','Purr','Meow','Livestock_and_farm_animals_and_working_animals','Fowl','Chicken_and_rooster', \
    'Wild_animals','Bird','Bird_vocalization_and_bird_call_and_bird_song','Crow','Gull_and_seagull','Insect','Cricket', 'Frog']

True_M = ['Music','Musical_instrument','Plucked_string_instrument','Guitar','Electric_guitar','Bass_guitar','Acoustic_guitar','Strum','Keyboard_(musical)','Piano', \
'Organ','Percussion','Drum_kit','Drum','Snare_drum','Bass_drum','Tabla','Cymbal','Hi-hat','Crash_cymbal','Tambourine','Rattle_(instrument)','Gong','Mallet_percussion', \
'Marimba_and_xylophone','Glockenspiel','Brass_instrument','Trumpet','Bowed_string_instrument','Wind_instrument_and_woodwind_instrument','Harp','Harmonica','Accordion',
 'Scratching_(performance_technique)']

for i in range(len(True_Natural)):
  True_Natural[i] = True_Natural[i].lower()
for i in range(len(True_Ambigous)):
  True_Ambigous[i] = True_Ambigous[i].lower()
for i in range(len(True_SoT)):
  True_SoT[i] = True_SoT[i].lower()
for i in range(len(True_Hs)):
  True_Hs[i] = True_Hs[i].lower()
for i in range(len(True_A)):
  True_A[i] = True_A[i].lower()
for i in range(len(True_M)):
  True_M[i] = True_M[i].lower()
  #

category=[]
for i,k in df.Anomaly_Sound_Audioset_Tags.iteritems():
  local=[0 for z in range(6)]
  # print(i,k)
  # print(ast.literal_eval(k))
  for j in k.lower().split(","):
    if j in True_Natural:
      local[0]=1
    if j in True_Ambigous:
      local[1]=1
    if j in True_Hs:
      local[2]=1
    if j in True_A:
      local[3]=1
    if j in True_SoT:
      local[4]=1
    if j in True_M:
      local[5]=1
  category.append(local)

df["y_category"]=category
#change this acc to category of classes, actual classes or parent classes
df["y_hot"]=hot

df=df.drop(df.index[[3069,3070]])
df=df.drop(df.index[df['Fname'] == "110reusschrikt_CrackingKnuckles"])

df2=df[df["Fname"].isin(x_vec)]

#sample the dataset
df2=df2.sample(n=2500)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df2.iloc[:,:-2], df2.iloc[:,-2:], test_size=0.2, random_state=1,shuffle=True)

# class dataload(torch.utils.data.Dataset):
#   def __init__(self,train_ids,y_labs):
#     self.Ambi_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Ambi_pann"))
#     self.Animal_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Animal_pann"))
#     self.Human_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Human_pann"))
#     self.Music_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Music_pann"))
#     self.Nature_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Nature_pann"))
#     self.SoT_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/SoT_pann"))
#     self.x_vec=train_ids
#     self.length=len(self.x_vec)
#     self.y_vec=y_labs
#     self.x_dat=[]

    
#   def __len__(self):
#     return self.length

#   def __getitem__(self,i):
#     X_path="/content/content/gdrive/MyDrive/New-FSD50K-Dataset/"
#     fname=self.x_vec[i]
#     k=fname+".npy"
#     # print(i)
#     x=None
#     if k in self.Ambi_Npy:
#       x=np.load(X_path+"Ambi_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Animal_Npy:
#       x=np.load(X_path+"Animal_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Human_Npy:
#       x=np.load(X_path+"Human_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Music_Npy:
#       x=np.load(X_path+"Music_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Nature_Npy:
#       x=np.load(X_path+"Nature_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.SoT_Npy:
#       x=np.load(X_path+"/SoT_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     pd=6955-x.shape[0]
#     t=np.zeros((pd,527))
#     x=np.concatenate((x,t),axis=0)
#     na=x.argsort()[:,-1]
#     na2=np.sort(x)[:,-1]
#     inp=[]
#     for i in range(na.shape[0]):
#       inp.append(labels[na[i]])
#     # print(self.y_vec[i])
#     return np.array(inp),self.y_vec[i]
#     #

class get_data():
  def __init__(self,train_ids,y_dat,y_hot):
    self.Ambi_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Ambi_pann"))
    self.Animal_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Animal_pann"))
    self.Human_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Human_pann"))
    self.Music_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Music_pann"))
    self.Nature_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Nature_pann"))
    self.SoT_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/SoT_pann"))
    self.x_vec=train_ids
    X_path="/content/content/gdrive/MyDrive/New-FSD50K-Dataset/"
    self.length=len(self.x_vec)
    self.x_dat=[]
    self.y_hot=[]
    self.y_dat=[]
    for i in range(self.length):
      fname=self.x_vec[i]
      k=fname+".npy"
      print(i)
      if k in self.Ambi_Npy:
        x=np.load(X_path+"Ambi_pann/"+k)
        self.y_dat.append(y_dat[i])
        self.y_hot.append(y_hot[i])
        na=x.argsort()[:,-1:]
        na2=np.sort(x)[:,-1:]
        inp=[]
        for u in range(na.shape[0]):
          temp=np.zeros(384)
          for p in range(na.shape[1]):
            # print(emb[na[i][j]]*na2[i][j])
            temp+=emb[na[u][p]]*na2[u][p]
            # print(temp.shape)
          inp.append(temp)
        self.x_dat.append(inp)
      elif k in self.Animal_Npy:
        x=np.load(X_path+"Animal_pann/"+k)
        self.y_dat.append(y_dat[i])
        self.y_hot.append(y_hot[i])
        na=x.argsort()[:,-1:]
        na2=np.sort(x)[:,-1:]
        inp=[]
        for u in range(na.shape[0]):
          temp=np.zeros(384)
          for p in range(na.shape[1]):
            # print(emb[na[i][j]]*na2[i][j])
            temp+=emb[na[u][p]]*na2[u][p]
            # print(temp.shape)
          inp.append(temp)
        self.x_dat.append(inp)
      elif k in self.Human_Npy:
        x=np.load(X_path+"Human_pann/"+k)
        self.y_dat.append(y_dat[i])
        self.y_hot.append(y_hot[i])
        na=x.argsort()[:,-1:]
        na2=np.sort(x)[:,-1:]
        inp=[]
        for u in range(na.shape[0]):
          temp=np.zeros(384)
          for p in range(na.shape[1]):
            # print(emb[na[i][j]]*na2[i][j])
            temp+=emb[na[u][p]]*na2[u][p]
            # print(temp.shape)
          inp.append(temp)
        self.x_dat.append(inp)
      elif k in self.Music_Npy:
        x=np.load(X_path+"Music_pann/"+k)
        self.y_dat.append(y_dat[i])
        self.y_hot.append(y_hot[i])
        na=x.argsort()[:,-1:]
        na2=np.sort(x)[:,-1:]
        inp=[]
        for u in range(na.shape[0]):
          temp=np.zeros(384)
          for p in range(na.shape[1]):
            # print(emb[na[i][j]]*na2[i][j])
            temp+=emb[na[u][p]]*na2[u][p]
            # print(temp.shape)
          inp.append(temp)
        self.x_dat.append(inp)
      elif k in self.Nature_Npy:
        x=np.load(X_path+"Nature_pann/"+k)
        self.y_dat.append(y_dat[i])
        self.y_hot.append(y_hot[i])
        na=x.argsort()[:,-1:]
        na2=np.sort(x)[:,-1:]
        inp=[]
        for u in range(na.shape[0]):
          temp=np.zeros(384)
          for p in range(na.shape[1]):
            # print(emb[na[i][j]]*na2[i][j])
            temp+=emb[na[u][p]]*na2[u][p]
            # print(temp.shape)
          inp.append(temp)
        self.x_dat.append(inp)
      elif k in self.SoT_Npy:
        x=np.load(X_path+"SoT_pann/"+k)
        self.y_dat.append(y_dat[i])
        self.y_hot.append(y_hot[i])
        na=x.argsort()[:,-1:]
        na2=np.sort(x)[:,-1:]
        inp=[]
        for u in range(na.shape[0]):
          temp=np.zeros(384)
          for p in range(na.shape[1]):
            # print(emb[na[i][j]]*na2[i][j])
            temp+=emb[na[u][p]]*na2[u][p]
            # print(temp.shape)
          inp.append(temp)
        self.x_dat.append(inp)

train_data=get_data(X_train["Fname"].tolist(),y_train["y_category"].to_list(),y_train["y_hot"].to_list())
test_data=get_data(X_test["Fname"].tolist(),y_test["y_category"].to_list(),y_test["y_hot"].to_list())

# class dataload(torch.utils.data.Dataset):
#   def __init__(self,train_ids,y_labs):
#     self.Ambi_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Ambi_pann"))
#     self.Animal_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Animal_pann"))
#     self.Human_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Human_pann"))
#     self.Music_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Music_pann"))
#     self.Nature_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/Nature_pann"))
#     self.SoT_Npy=sorted(os.listdir("/content/content/gdrive/MyDrive/New-FSD50K-Dataset/SoT_pann"))
#     self.x_vec=train_ids
#     self.length=len(self.x_vec)
#     self.y_vec=y_labs
#     self.x_dat=[]

    
#   def __len__(self):
#     return self.length

#   def __getitem__(self,i):
#     X_path="/content/content/gdrive/MyDrive/New-FSD50K-Dataset/"
#     fname=self.x_vec[i]
#     k=fname+".npy"
#     # print(i)
#     x=None
#     if k in self.Ambi_Npy:
#       x=np.load(X_path+"Ambi_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Animal_Npy:
#       x=np.load(X_path+"Animal_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Human_Npy:
#       x=np.load(X_path+"Human_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Music_Npy:
#       x=np.load(X_path+"Music_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.Nature_Npy:
#       x=np.load(X_path+"Nature_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     if k in self.SoT_Npy:
#       x=np.load(X_path+"/SoT_pann/"+k)
#       # return x,self.y_vec[i]
#       # self.x_dat.append(x)
#     pd=6955-x.shape[0]
#     t=np.zeros((pd,527))
#     x=np.concatenate((x,t),axis=0)
#     na=x.argsort()[:,-1:]
#     na2=np.sort(x)[:,-1:]
#     inp=[]
#     for u in range(na.shape[0]):
#       temp=np.zeros(384)
#       for p in range(na.shape[1]):
#         # print(emb[na[i][j]]*na2[i][j])
#         temp+=emb[na[u][p]]*na2[u][p]
#         # print(temp.shape)
#       inp.append(temp)
#       # print(np.array(inp))
#     # print(self.y_vec[i])
#     return np.array(inp),self.y_vec[i]
#     #

class dataload(torch.utils.data.Dataset):
  def __init__(self,x_dat,y_labs):
    self.x_dat=x_dat
    self.y_vec=y_labs
    self.length=len(y_labs)
    print(self.length)
    # print(x_dat)

    
  def __len__(self):
    return self.length

  def __getitem__(self,i):
    x=np.array(self.x_dat[i])
    pd=6955-x.shape[0]
    t=np.zeros((pd,384))
    x=np.concatenate((x,t),axis=0)
    return x,self.y_vec[i]

class Lstm_classification(nn.Module):
  def __init__(self):
    self.hidden_dim=384
    self.output_classes=6
    super(Lstm_classification,self).__init__()
    self.lstm=nn.LSTM(input_size=self.hidden_dim,num_layers=2 ,hidden_size=self.hidden_dim,batch_first=True)
    self.fc1 = nn.Sequential(nn.Linear(self.hidden_dim, 50),nn.ReLU(),nn.Linear(50,self.output_classes))
    

  def forward(self,x):
    out, (hidden, cell)=self.lstm(x)
    # if torch.any(torch.isnan(out)).item():
    #     import pdb; pdb.set_trace()
    # print(out[:,-1,:].shape)
    out= self.fc1(out[:,-1,:])
    # if torch.any(torch.isnan(out)).item():
    #     import pdb; pdb.set_trace()
    return out

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
a=[]
b=[]
c=[]
d=[]
e=[]
f=[]
g=[]
def calculate_metrics(pred, target, threshold=0.5):
  pred = np.array(pred > threshold, dtype=int)
  # print(pred,target)
  print('Accuracy : ', accuracy_score(y_true=target, y_pred=pred))
  print('micro/precision', precision_score(y_true=target, y_pred=pred, average='micro'))
  print('micro/recall', recall_score(y_true=target, y_pred=pred, average='micro'))
  print('micro/f1', f1_score(y_true=target, y_pred=pred, average='micro'))
  print('macro/precision', precision_score(y_true=target, y_pred=pred, average='macro'))
  print('macro/recall', recall_score(y_true=target, y_pred=pred, average='macro'))
  print('macro/f1', f1_score(y_true=target, y_pred=pred, average='macro'))
  a.append(accuracy_score(y_true=target, y_pred=pred))
  b.append( precision_score(y_true=target, y_pred=pred, average='micro'))
  c.append( recall_score(y_true=target, y_pred=pred, average='micro'))
  d.append(f1_score(y_true=target, y_pred=pred, average='micro'))
  e.append(precision_score(y_true=target, y_pred=pred, average='macro'))
  f.append( recall_score(y_true=target, y_pred=pred, average='macro'))
  g.append(f1_score(y_true=target, y_pred=pred, average='macro'))

import os
# train_dataset=dataload(X_train["Fname"].tolist(),np.array(y_train["y_category"].to_list()))
# print(len(X_train["Fname"].tolist()))
# train_loader = torch.utils.data.DataLoader(train_data, batch_size=16,shuffle=True)
# val_dataset=dataload(X_test["Fname"].tolist(),np.array(y_test["y_category"].to_list()))
# val_loader = torch.utils.data.DataLoader(val_data, batch_size=16,shuffle=False)
train_dataset=dataload(train_data.x_dat,np.array(train_data.y_dat))
val_dataset=dataload(test_data.x_dat,np.array(test_data.y_dat))

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32,shuffle=True)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=1,shuffle=False)

torch.cuda.empty_cache()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model=Lstm_classification().to(device)
epochs=50
# model.load_state_dict(dict_param['model_state_dict'])
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=2,verbose=True)
# scaler=amp.GradScaler()
# optimizer.load_state_dict(dict_param['potimizer_state_dict'])
# for g in optimizer.param_groups:
#   g['lr'] = 0.003
criterion = torch.nn.BCEWithLogitsLoss()
sig=nn.Sigmoid()

def val_score():
  model.eval()
  with torch.no_grad():
    model_result = []
    targets=[]
    for i, (data,target) in enumerate(val_loader):
      # data = data.float().reshape(data.shape[0],1,data.shape[1],data.shape[2]).to(device)
      # target = target.float().to(device)
      # print(target.shape)
      output = model(data.float().to(device))
      output=sig(output)
      model_result.extend(output.cpu().numpy())
      targets.extend(target.cpu().numpy())
    result = calculate_metrics(np.array(model_result), np.array(targets))


for ep in range(epochs):
  model.train()
  avg_loss=0
  for i, (data,target) in enumerate(train_loader):
    target = target.float().to(device)

    optimizer.zero_grad()
    print(torch.any(torch.isnan(data)))
    print(torch.any(torch.isnan(data.float())))
    output = model(data.float().to(device))
    loss = criterion(output, target)
    print(avg_loss, loss)
    loss.backward()
    optimizer.step()
    avg_loss += loss.detach()
  print("============EPOCH : ",ep,"=======================")
  print("average loss epoch: ", avg_loss)
  print("average loss epoch: ", avg_loss/len(train_dataset))
  val_score()
  print("==============================================")
  scheduler.step(avg_loss)

