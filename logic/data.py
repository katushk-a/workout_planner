import pandas as pd

df = pd.read_csv('logic/data/megaGymDataset_cleaned.csv')

def get_info():
    levels = df['Level'].unique().tolist()
    equipments = df['Equipment'].unique().tolist()
    purposes = ['lose_weight', 'gain_muscle', 'increase_stamina', 'maintain_shape', 'powerlifting','flexibility']
    info = {
        'levels': levels,
        'equipments': equipments,
        'purposes': purposes
    }
    return info