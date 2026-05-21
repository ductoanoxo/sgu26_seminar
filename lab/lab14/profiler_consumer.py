import pandas as pd
from memory_profiler import profile

@profile
def get_top_video(path):
    interactions = pd.read_csv(path)
    avg_ratio = interactions.mean(axis=0, skipna=True)
    return avg_ratio.idxmax()

get_top_video('interactions_10_000.csv')