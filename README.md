# MKV Subtitle Extraction, Translation, and Merging Tool

This repository contains a set of Python scripts designed to automate the process of extracting subtitles from MKV files, translating them using Ollama, and merging the translated subtitles back into the MKV files.

## Features

* **Subtitle Extraction:** Extracts specified subtitle tracks from MKV files using `mkvextract`.
* **Subtitle Translation:** Translates the extracted subtitles to Romanian using Ollama's API.
* **Subtitle Merging:** Merges the translated subtitles back into the MKV files using `mkvmerge`.
* **Batch Processing:** Processes multiple MKV and SRT files in a directory.
* **Asynchronous Translation:** Uses `aiohttp` and `asyncio` for efficient, concurrent translation.
* **GPU/CPU Support:** Automatically detects and utilizes GPU if available.

## Prerequisites

* **Python 3.7+:** Ensure Python is installed on your system.
* **mkvtoolnix:** Install `mkvtoolnix` for `mkvextract` and `mkvmerge` utilities. Make sure it's in your system's PATH.
* **Ollama:** Install Ollama and pull the desired model (e.g., `gemma3:12b`). Run Ollama server.
* **Dependencies:** Install required Python packages using `pip install package-name`.

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  Install the required Python packages:

3.  Ensure `mkvtoolnix` is installed and in your system's PATH.
4.  Run Ollama server and pull your model:

    ```bash
    ollama pull gemma3:12b
    ollama run gemma3:12b
    ```

## Usage

1.  **Extract Subtitles:**

    * Place your MKV files in the same directory as `extract.py`.
    * Run `extract.py` and change the track number on the script to extract the correct track.

    ```bash
    python extract.py
    ```

    * Extracted SRT files will be saved in the `extracted_srts` folder.

2.  **Translate Subtitles:**

    * Place the SRT files you want to translate in the same directory as `translate.py`.
    * Run `translate.py`.

    ```bash
    python translate.py
    ```

    * Translated SRT files will be created in the same directory, with `_ro.srt` appended to the original filename.

3.  **Merge Subtitles:**

    * Place the original MKV files and the translated SRT files in the same directory as `subtitle.py`.
    * Run `subtitle.py`.

    ```bash
    python subtitle.py
    ```

    * New MKV files with the translated subtitles will be created, with `(RO).mkv` appended to the original filename.

## File Descriptions

* `extract.py`: Extracts subtitle tracks from MKV files.
* `translate.py`: Translates SRT files using Ollama.
* `subtitle.py`: Merges translated SRT files back into MKV files.

## Customization

* **Track ID:** Modify the `track_id_to_extract` variable in `extract.py` to specify the desired subtitle track.
* **Ollama Model:** Change the `model` variable in `translate.py` to use a different Ollama model.
* **Batch Size:** Adjust the `batch_size` variable in `translate.py` to control the number of subtitles processed in each batch.
* **Charset:** Modify the `charset` variable in `subtitle.py` to change the character encoding of the merged subtitles.

## Troubleshooting

* **`mkvextract` or `mkvmerge` not found:** Ensure `mkvtoolnix` is installed and in your system's PATH.
* **Ollama connection errors:** Verify that Ollama is running and accessible at `http://localhost:11434`.
* **Translation errors:** Check the Ollama model and prompts for accuracy.
* **Encoding issues:** Make sure the charset is set correctly in `subtitle.py`.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug fixes, feature requests, or improvements.

## License

This project is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for details.
