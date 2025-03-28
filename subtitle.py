import os
import subprocess

# Get the current working directory (the folder where your script is located)
folder_path = os.path.dirname(os.path.abspath(__file__))

# Charset to be used
charset = "UTF-8"  # Change this to the desired charset

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.lower().endswith((".mp4", ".mkv")):  # Checking for both .mp4 and .mkv extensions
        video_path = os.path.join(folder_path, file_name)

        # Check if a corresponding SRT file exists
        srt_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + ".srt")
        if os.path.exists(srt_path):
            output_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + " (RO).mkv")

            # Construct the mkvmerge command
            mkvmerge_command = [
                "mkvmerge",
                "-o", output_path,
                video_path,
                "--language", "0:ro", srt_path,
                "--sub-charset", "0:" + charset
            ]

            # Run the mkvmerge command
            subprocess.run(mkvmerge_command)
            print(f"Merged {file_name} with {os.path.basename(srt_path)} to {os.path.basename(output_path)}")
        else:
            print(f"No corresponding SRT file found for {file_name}")
