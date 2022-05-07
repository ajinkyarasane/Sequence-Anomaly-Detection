
import os
import json
import pandas as pd
import numpy as np
import shutil

#---------------------------------------------
# SPLITTING THE MUSIC FILES INTO PARENT CLASSES
#----------------------------------------------

Check = pd.read_csv(r'/mnt/d/Google_downloads/FSD50K.metadata/collection/collection_dev.csv')
Check.dropna(inplace = True)

f = json.load(open(r'/mnt/d/Google_downloads/FSD50K.metadata/dev_clips_info_FSD50K.json'))
Sounds = sorted(os.listdir(r'/mnt/d/Google_downloads/FSD50K.dev_audio/15+'))
Anomaly = sorted(os.listdir(r'/mnt/d/Google_downloads/FSD50K.dev_audio/4-'))

Animal = []
Human_Sounds = []
Music = []
Sound_of_Things = []
Natural_Sounds = []
Ambi_Sounds = []

Animal_Anomaly = []
Human_Sounds_Anomaly = []
Music_Anomaly = []
Sound_of_Things_Anomaly = []
Natural_Sounds_Anomaly = []
Ambi_Sounds_Anomaly = []

Sounds_key = []
Anomalies_key = []

# True Labels belonging to the parent classes according to the Audioset Ontology is obtained from True_labels.py

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


Dic ={}
for(id,name) in zip(Check['fname'],Check['labels']):
    Dic[id] = name

#----------------------------------------------
# Splitting the Anomalies according to their "Parent" classes
#----------------------------------------------


for A in Anomaly:
    Anomalies_key.append(str((A.split('.')[0])))

for key in Anomalies_key:
    base_tags = []
    final = []
    if (int(key) in Dic.keys()):
        base_tags.append(Dic[int(key)])
    else:
        continue
    final = base_tags[0].split(',')
    if any(i in final for i in True_SoT):
        Sound_of_Things_Anomaly.append(key)
    if any(i in final for i in True_Hs):
        Human_Sounds.append(key)
    if any(i in final for i in True_A):
        Animal_Anomaly.append(key)
    if any(i in final for i in True_M):
        Music_Anomaly.append(key)
    if any(i in final for i in True_Natural):
        Natural_Sounds_Anomaly.append(key)
    if any(i in final for i in True_Ambigous):
        Ambi_Sounds_Anomaly.append(key)


source_sound = r'/mnt/d/Google_downloads/FSD50K.dev_audio/4-/'
dest_animal_Anomaly = r'/mnt/d/Final_Dataset_Anomaly/Animal_Sounds_Anomaly/'
dest_music_Anomaly = r'/mnt/d/Final_Dataset_Anomaly/Music_Sounds_Anomaly/'
dest_human_Anomaly = r'/mnt/d/Final_Dataset_Anomaly/Human_Sounds_Anomaly/'
dest_nature_Anomaly = r'/mnt/d/Final_Dataset_Anomaly/Nature_Sounds_Anomaly/'
dest_sot_Anomaly = r'/mnt/d/Final_Dataset_Anomaly/Sound_Of_Things_Anomaly/'
dest_ambi_Anomaly = r'/mnt/d/Final_Dataset_Anomaly/Ambious_Sounds_Anomaly/'


for key in Animal_Anomaly:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_animal_Anomaly)

for key in Music_Anomaly:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_music_Anomaly)

for key in Natural_Sounds_Anomaly:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_nature_Anomaly)

for key in Ambi_Sounds_Anomaly:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_ambi_Anomaly)

for key in Sound_of_Things_Anomaly:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_sot_Anomaly)

for key in Human_Sounds_Anomaly:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_human_Anomaly)


#----------------------------------------------
# Splitting the Base Sound Clips according to their "Parent" classes
#----------------------------------------------

for S in Sounds:
    Sounds_key.append(str((S.split('.')[0])))

for key in Sounds_key:
    base_tags = []
    final = []
    if (int(key) in Dic.keys()):
        base_tags.append(Dic[int(key)])
    else:
        continue
    final = base_tags[0].split(',')
    if any(i in final for i in True_SoT):
        Sound_of_Things.append(key)
    if any(i in final for i in True_Hs):
        Human_Sounds.append(key)
    if any(i in final for i in True_A):
        Animal.append(key)
    if any(i in final for i in True_M):
        Music.append(key)
    if any(i in final for i in True_Natural):
        Natural_Sounds.append(key)
    if any(i in final for i in True_Ambigous):
        Ambi_Sounds.append(key)

# print(len(Animal))
source_sound = r'/mnt/d/Google_downloads/FSD50K.dev_audio/15+/'
dest_animal = r'/mnt/d/Final_Dataset_Train/Animal_Sounds/'
dest_music = r'/mnt/d/Final_Dataset_Train/Music_Sounds/'
dest_human = r'/mnt/d/Final_Dataset_Train/Human_Sounds/'
dest_nature = r'/mnt/d/Final_Dataset_Train/Nature_Sounds/'
dest_sot = r'/mnt/d/Final_Dataset_Train/Sound_Of_Things/'
dest_ambi = r'/mnt/d/Final_Dataset_Train/Ambious_Sounds/'

# for key in Animal:
#     content = str(key) + ".wav"
#     shutil.copy(source_sound + content, dest_animal)

for key in Music:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_music)

for key in Natural_Sounds:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_nature)

for key in Ambi_Sounds:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_ambi)

for key in Sound_of_Things:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_sot)

for key in Human_Sounds:
    content = str(key) + ".wav"
    shutil.copy(source_sound + content, dest_human)








































# anomaly_key = []
# for a in Anomaly:
#     anomaly_key.append(str(a.split('.')[0]))


# all_tags = []
# for key in anomaly_key:
#   all_tags.append(f[key]['tags'])

# mix = []
# discard = []
# for s in Sounds:
#   key = str(s.split('.')[0])
#   base_tags = f[key]['tags']
#   for tag in all_tags:
#     if any(item in base_tags for item in tag):
#       discard.append(tag)
#     else:
#       mix.append(tag)
#   break

# print(len(mix))