import subprocess
import os

def extract_and_rename_srt(track_id, output_folder="extracted_srts"):
    """
    Extracts a specified track from all MKV files in the current folder and renames them to SRT files.

    Args:
        track_id (int): The track ID to extract.
        output_folder (str): The folder where extracted SRT files will be saved.
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    mkv_files = [f for f in os.listdir() if f.lower().endswith(".mkv")]

    if not mkv_files:
        print("No MKV files found in the current folder.")
        return

    for mkv_file in mkv_files:
        filename_without_ext = os.path.splitext(mkv_file)[0]
        temp_track_file = os.path.join(output_folder, f"{filename_without_ext}_track_{track_id}.track")
        srt_file = os.path.join(output_folder, f"{filename_without_ext}.srt")

        command = [
            "mkvextract",
            "tracks",
            mkv_file,
            f"{track_id}:{temp_track_file}",
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Successfully extracted track {track_id} from {mkv_file} to {temp_track_file}")

            # Rename to SRT if extraction was successful
            os.rename(temp_track_file, srt_file)
            print(f"Renamed {temp_track_file} to {srt_file}")

        except subprocess.CalledProcessError as e:
            print(f"Error extracting track from {mkv_file}: {e}")
            print(e.stderr)
            # Remove temp file if it was created, but extraction failed.
            if os.path.exists(temp_track_file):
                os.remove(temp_track_file)
        except FileNotFoundError:
            print("Error: mkvextract not found. Make sure mkvtoolnix is installed and in your PATH.")
            return

# Example usage:
track_id_to_extract = 2  # Replace with the desired track ID
extract_and_rename_srt(track_id_to_extract)
