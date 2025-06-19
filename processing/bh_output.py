import gzip
import pickle

#with gzip.open("histograms-default.pkl.gz", "rb") as f:
#with gzip.open("histograms.pkl.gz", "rb") as f:
with gzip.open("histograms-reformed.pkl.gz", "rb") as f:
    bh_output = pickle.load(f)

# Print the type of bh_output
print(type(bh_output))

# Print the keys if it is a dict
if isinstance(bh_output, dict):
    print("Keys in bh_output:", list(bh_output.keys()))

# Optionally print one histogram or summary
for key in list(bh_output.keys())[:3]:
    print(f"\nContents of '{key}':")
    print(bh_output[key])
