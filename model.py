import numpy as np
import pandas as pd
import librosa
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

X_sentence, X_speaker, y_sentence, y_speaker = [], [], [], []

unlock_gate_stored_files = ['UnlockMiddleGate/ahmed_unlock_1.wav', 'UnlockMiddleGate/ahmed_unlock_2.wav', 'UnlockMiddleGate/ahmed_unlock_4.wav', 'UnlockMiddleGate/ahmed_unlock_5.wav',
                             'UnlockMiddleGate/nourhan_unlock_1.wav', 'UnlockMiddleGate/nourhan_unlock_2.wav', 'UnlockMiddleGate/nourhan_unlock_3.wav',
                               'UnlockMiddleGate/hazem_unlock_1.wav', 'UnlockMiddleGate/hazem_unlock_2.wav',
                                 'UnlockMiddleGate/raghda_unlock_2.wav', 'UnlockMiddleGate/raghda_unlock_3.wav',
                                   'UnlockMiddleGate/samer_unlock_1.wav', 'UnlockMiddleGate/samer_unlock_2.wav',
                                     'UnlockMiddleGate/mariem_unlock_1.wav', 'UnlockMiddleGate/mariem_unlock_2.wav',
                                       'UnlockMiddleGate/ali_unlock_1.wav', 'UnlockMiddleGate/ali_unlock_2.wav',
                                         'UnlockMiddleGate/nariman_unlock_1.wav', 'UnlockMiddleGate/nariman_unlock_2.wav']

open_door_stored_files = ['OpenTheDoor/ahmed_open_4.wav', 'OpenTheDoor/ahmed_open_5.wav', 'OpenTheDoor/ahmed_open_6.wav', 'OpenTheDoor/ahmed_open_7.wav',
                           'OpenTheDoor/nourhan_open_1.wav', 'OpenTheDoor/nourhan_open_2.wav', 'OpenTheDoor/nourhan_open_3.wav', 'OpenTheDoor/nourhan_open_5.wav', 'OpenTheDoor/nourhan_open_6.wav',
                             'OpenTheDoor/hazem_open_1.wav', 'OpenTheDoor/hazem_open_2.wav', 'OpenTheDoor/hazem_open_3.wav', 'OpenTheDoor/hazem_open_4.wav',
                               'OpenTheDoor/raghda_open_1.wav', 'OpenTheDoor/raghda_open_2.wav', 'OpenTheDoor/raghda_open_4.wav',
                                 'OpenTheDoor/samer_open_2.wav',
                                   'OpenTheDoor/mariem_open_1.wav', 'OpenTheDoor/mariem_open_2.wav', 'OpenTheDoor/mariem_open_3.wav',
                                     'OpenTheDoor/ali_open_1.wav', 'OpenTheDoor/ali_open_2.wav', 'OpenTheDoor/ali_open_3.wav',
                                       'OpenTheDoor/nariman_open_1.wav']

give_access_stored_files = ['GiveMeAccess/ahmed_give_1.wav', 'GiveMeAccess/ahmed_give_2.wav', 'GiveMeAccess/ahmed_give_3.wav', 'GiveMeAccess/ahmed_give_4.wav',
                             'GiveMeAccess/nourhan_give_1.wav', 'GiveMeAccess/nourhan_give_2.wav', 'GiveMeAccess/nourhan_give_3.wav',
                               'GiveMeAccess/hazem_give_1.wav', 'GiveMeAccess/hazem_give_2.wav', 'GiveMeAccess/hazem_give_3.wav',
                                 'GiveMeAccess/raghda_give_1.wav', 'GiveMeAccess/raghda_give_2.wav', 'GiveMeAccess/raghda_give_3.wav',
                                   'GiveMeAccess/samer_give_1.wav', 'GiveMeAccess/samer_give_2.wav', 'GiveMeAccess/samer_give_3.wav',
                                     'GiveMeAccess/mariem_give_1.wav', 'GiveMeAccess/mariem_give_2.wav', 'GiveMeAccess/mariem_give_3.wav',
                                       'GiveMeAccess/ali_give_1.wav', 'GiveMeAccess/ali_give_2.wav', 'GiveMeAccess/ali_give_3.wav',
                                         'GiveMeAccess/nariman_give_1.wav', 'GiveMeAccess/nariman_give_2.wav', 'GiveMeAccess/nariman_give_3.wav']

ahmed_voice = ['Speakers/ahmed_1.wav', 'Speakers/ahmed_2.wav', 'Speakers/ahmed_3.wav', 'Speakers/ahmed_4.wav', 'Speakers/ahmed_5.wav', 'Speakers/ahmed_6.wav', 'Speakers/ahmed_7.wav', 'Speakers/ahmed_8.wav', 'Speakers/ahmed_9.wav', 'Speakers/ahmed_10.wav']
nourhan_voice = ['Speakers/nourhan_1.wav', 'Speakers/nourhan_2.wav', 'Speakers/nourhan_3.wav', 'Speakers/nourhan_4.wav', 'Speakers/nourhan_5.wav', 'Speakers/nourhan_6.wav', 'Speakers/nourhan_7.wav', 'Speakers/nourhan_8.wav', 'Speakers/nourhan_9.wav', 'Speakers/nourhan_10.wav']
hazem_voice = ['Speakers/hazem_1.wav', 'Speakers/hazem_2.wav', 'Speakers/hazem_3.wav', 'Speakers/hazem_4.wav', 'Speakers/hazem_5.wav', 'Speakers/hazem_6.wav', 'Speakers/hazem_7.wav', 'Speakers/hazem_8.wav', 'Speakers/hazem_9.wav', 'Speakers/hazem_10.wav']
raghda_voice = ['Speakers/raghda_1.wav', 'Speakers/raghda_2.wav', 'Speakers/raghda_3.wav', 'Speakers/raghda_4.wav', 'Speakers/raghda_5.wav', 'Speakers/raghda_6.wav', 'Speakers/raghda_7.wav', 'Speakers/raghda_8.wav', 'Speakers/raghda_9.wav', 'Speakers/raghda_10.wav']

unlock_sentence = ['Sentences/unlock_1.wav', 'Sentences/unlock_2.wav', 'Sentences/unlock_3.wav', 'Sentences/unlock_4.wav', 'Sentences/unlock_5.wav', 'Sentences/unlock_6.wav', 'Sentences/unlock_7.wav']
open_sentence = ['Sentences/open_3.wav', 'Sentences/open_6.wav', 'Sentences/open_7.wav', 'Sentences/open_10.wav', 'Sentences/open_11.wav', 'Sentences/open_12.wav', 'Sentences/open_13.wav', 'Sentences/open_14.wav']
give_sentence = ['Sentences/give_1.wav', 'Sentences/give_2.wav', 'Sentences/give_3.wav', 'Sentences/give_4.wav', 'Sentences/give_5.wav', 'Sentences/give_6.wav', 'Sentences/give_9.wav', 'Sentences/give_10.wav']

other_sentences = ['Others/empty_1.wav', 'Others/empty_2.wav' ,'Others/empty_3.wav', 'Others/empty_4.wav', 'Others/empty_5.wav',
                   'Others/ahmed_allow_1.wav', 'Others/ahmed_allow_2.wav', 'Others/ahmed_allow_3.wav', 'Others/ahmed_permit_1.wav', 'Others/ahmed_permit_2.wav', 'Others/ahmed_permit_3.wav', 'Others/ahmed_turnon_1.wav', 'Others/ahmed_turnon_2.wav', 'Others/ahmed_turnon_3.wav',
                    'Others/nourhan_allow_1.wav', 'Others/nourhan_allow_2.wav', 'Others/nourhan_allow_3.wav', 'Others/nourhan_permit_1.wav', 'Others/nourhan_permit_2.wav', 'Others/nourhan_permit_3.wav', 'Others/nourhan_turnon_1.wav', 'Others/nourhan_turnon_2.wav', 'Others/nourhan_turnon_3.wav',
                     'Others/hazem_allow_1.wav', 'Others/hazem_allow_2.wav', 'Others/hazem_allow_3.wav', 'Others/hazem_permit_1.wav', 'Others/hazem_permit_2.wav', 'Others/hazem_permit_3.wav', 'Others/hazem_turnon_1.wav', 'Others/hazem_turnon_2.wav', 'Others/hazem_turnon_3.wav',
                     'Others/raghda_allow_1.wav', 'Others/raghda_allow_2.wav', 'Others/raghda_allow_3.wav', 'Others/raghda_permit_1.wav', 'Others/raghda_permit_2.wav', 'Others/raghda_permit_3.wav', 'Others/raghda_turnon_1.wav', 'Others/raghda_turnon_2.wav', 'Others/raghda_turnon_3.wav']

file_arrays = [unlock_gate_stored_files, open_door_stored_files, give_access_stored_files]
speaker_arrays = [ahmed_voice, nourhan_voice, hazem_voice, raghda_voice]
sentences_arrays = [unlock_sentence, open_sentence, give_sentence]

def label_encode(labels):
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    return labels_encoded

def extract_features(file_path):
    y, sr = librosa.load(file_path)
        
    sentence_spectrogram = np.abs(librosa.stft(y))
    sentence_features = np.mean(librosa.feature.mfcc(y=y, sr=sr, S=librosa.amplitude_to_db(sentence_spectrogram), n_mfcc=40), axis=1)

    speaker_features = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
    
    return sentence_features, speaker_features

def load_others_data(file_array):
    for filename in file_array:
                
      other_sentence_features , _ = extract_features(filename)
                    
      X_sentence.append(other_sentence_features)
      y_sentence.append('other')

def load_sentence_data(file_arrays):
    for file_array in (file_arrays):
        for filename in file_array:
            sentence_said = filename.split('/')[1].split('_')[0]
                
            sentence_features , _ = extract_features(filename)
                    
            X_sentence.append(sentence_features)
            y_sentence.append(sentence_said)

def load_speaker_data(file_arrays):
    for file_array in (file_arrays):
        for filename in file_array:
            speaker_name = filename.split('/')[1].split('_')[0]
                
            _ , speaker_features = extract_features(filename)

            X_speaker.append(speaker_features)
            y_speaker.append(speaker_name)
    
def load_data(file_arrays):
    for file_array in (file_arrays):
        for filename in file_array:
            speaker_name, sentence_said, _ = filename.split('/')[1].split('_')
                
            sentence_features, speaker_features = extract_features(filename)
                    
            X_sentence.append(sentence_features)
            X_speaker.append(speaker_features)
            y_sentence.append(sentence_said)
            y_speaker.append(speaker_name)

    # sentence_features_df = pd.DataFrame(X_sentence, columns=[f'coefficient_{i}' for i in range(1, 41)])
    # sentence_features_df['Sentence'] = y_sentence
    # speaker_features_df = pd.DataFrame(X_speaker, columns=[f'coefficient_{i}' for i in range(1, 14)])
    # speaker_features_df['Speaker'] = y_speaker
    # print(sentence_features_df)
    # print(speaker_features_df)

    return X_sentence, X_speaker, y_sentence, y_speaker

def load_model():
    X_sentence, X_speaker, y_sentence, y_speaker = load_data(file_arrays)
    load_speaker_data(speaker_arrays)
    load_sentence_data(sentences_arrays)
    load_others_data(other_sentences)

    y_sentence_encoded = label_encode(y_sentence)
    y_speaker_encoded = label_encode(y_speaker)

    model_sentence = svm.SVC(kernel='linear', random_state=20, probability=True)
    model_sentence.fit(X_sentence, y_sentence_encoded)
    
    class_weights_speaker = {0: 10.0, 2: 10.0, 5: 10.0, 6: 10.0}

    model_speaker = svm.SVC(kernel='linear', random_state=20, probability=True, class_weight=class_weights_speaker)
    model_speaker.fit(X_speaker, y_speaker_encoded)

    return model_sentence, model_speaker