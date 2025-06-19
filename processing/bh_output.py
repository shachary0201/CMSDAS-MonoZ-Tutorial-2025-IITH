import gzip
import pickle

#with gzip.open("histograms-default.pkl.gz", "rb") as f:
#with gzip.open("histograms.pkl.gz", "rb") as f:
with gzip.open("histograms-reformed.pkl.gz", "rb") as f:
    bh_output = pickle.load(f)

print(type(bh_output))

if isinstance(bh_output, dict):
    print("Keys in bh_output:", list(bh_output.keys()))

for key in list(bh_output.keys())[:3]:
    print(f"\nContents of '{key}':")
    print(bh_output[key])
