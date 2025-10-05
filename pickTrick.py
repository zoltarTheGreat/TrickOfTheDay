import yaml
import os

# Load tricks
with open("tricks.yaml", "r") as f:
    tricks = yaml.safe_load(f)

# Load last used index
last_index_file = ".last_trick_index"
if os.path.exists(last_index_file):
    with open(last_index_file, "r") as f:
        last_index = int(f.read().strip())
else:
    last_index = -1

# Compute next trick index
next_index = (last_index + 1) % len(tricks)
trick = tricks[next_index]

# Update README.md
video_id = trick["video"].split("v=")[-1]  # extract YouTube video ID
thumbnail = f"https://img.youtube.com/vi/{video_id}/0.jpg"

with open("README.md", "w") as f:
    f.write(f"# Trick of the Day\n\n")
    f.write(f"## {trick['name']}\n\n")
    f.write(f"{trick['description']}\n\n")
    f.write(f"**Invented by:** {trick.get('invented_by', 'Unknown')}\n\n")
    f.write(f"**Year:** {trick.get('year', 'Unknown')}\n\n")
    f.write(f"[![Watch the trick]({thumbnail})]({trick['video']})\n")

# Save last index
with open(last_index_file, "w") as f:
    f.write(str(next_index))
