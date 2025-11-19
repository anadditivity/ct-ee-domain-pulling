import os
import hashlib

# Directory containing your PEM files
input_dir = "./certificates"
duplicates_file = "python-duplicate-certificates.txt"

hash_map = {}
duplicates = []

for filename in os.listdir(input_dir):
    if filename.endswith(".pem"):
        filepath = os.path.join(input_dir, filename)
        
        # Compute SHA-256 hash
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Group by hash
        if file_hash not in hash_map:
            hash_map[file_hash] = [filename]
        else:
            hash_map[file_hash].append(filename)

# Collect duplicates (all but the first in each group)
for files in hash_map.values():
    if len(files) > 1:
        duplicates.extend(files[1:])  # keep first, mark others as duplicates

# Save duplicates list to file
with open(duplicates_file, "w") as f:
    for dup in duplicates:
        f.write(dup + "\n")

print(f"Found {len(duplicates)} duplicate certificates.")
print(f"Duplicate list saved to: {duplicates_file}")
