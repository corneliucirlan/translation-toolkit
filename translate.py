import asyncio
import aiohttp
import os
import re
import torch

class Subtitle:
    def __init__(self, id, timestamps, original, translated):
        self.id = id
        self.timestamps = timestamps
        self.original = original
        self.translated = translated

    def __str__(self):
        return f"id: {self.id}\ntimestamps: {self.timestamps}\noriginal: {self.original}\ntranslated: {self.translated}"

def parse_srt(srt_file_path):
    """Parses an SRT file and returns a list of Subtitle objects."""
    subtitles = []
    with open(srt_file_path, 'r', encoding='utf-8') as f:
        srt_content = f.read()

    subtitle_blocks = re.split(r'\n\s*\n', srt_content.strip())

    for block in subtitle_blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                id = int(lines[0].strip())
                timestamps = lines[1].strip()
                original = '\n'.join(lines[2:]).strip()
                subtitles.append(Subtitle(id, timestamps, original, ""))
            except ValueError:
                print(f"Warning: Invalid subtitle block: {block}")
        else:
            print(f"Warning: Incomplete subtitle block: {block}")
    return subtitles

async def generate_ollama(session, model, prompt):
    """Generates a response from Ollama asynchronously."""
    url = "http://localhost:11434/api/generate"  # Ollama API endpoint
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    try:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["response"]
            else:
                return f"Error: {response.status}"
    except aiohttp.ClientError as e:
        return f"Error: {e}"

async def process_commands(model, commands):
    """Processes a list of commands asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [generate_ollama(session, model, command) for command in commands]
        results = await asyncio.gather(*tasks)
        return results

async def translate_subtitles(subtitle_array, output_srt_file, model, batch_size):
    with open(output_srt_file, "w", encoding="utf-8") as outfile:
        array_length = len(subtitle_array)
        for batch_index in range(0, array_length, batch_size):
            batch = subtitle_array[batch_index:batch_index + batch_size]
            print(f"Processing batch starting at index {batch_index} of {array_length}:")
            prompts = [f"Give me only the Romanian translation: '{subtitle.original}'" for subtitle in batch]

            results = await process_commands(model, prompts)
            for i, result in enumerate(results):
                subtitle_array[batch_index + i].translated = result

                outfile.write(f"{subtitle_array[batch_index + i].id}\n")
                outfile.write(f"{subtitle_array[batch_index + i].timestamps}\n")
                outfile.write(f"{subtitle_array[batch_index + i].translated}\n")
                outfile.write("\n")

                print(f"{subtitle_array[batch_index + i].id}")
                print(f"{subtitle_array[batch_index + i].timestamps}")
                print(f"{subtitle_array[batch_index + i].translated}")
                print("\n")

async def process_srt_file(input_srt_file, model, batch_size):
    """Processes a single SRT file."""
    output_srt_file = os.path.splitext(input_srt_file)[0] + "_ro.srt"
    if not os.path.exists(input_srt_file):
        print(f"Error: Input file '{input_srt_file}' not found.")
        return

    print(f"Processing SRT file: {input_srt_file}")
    subtitles = parse_srt(input_srt_file)
    await translate_subtitles(subtitles, output_srt_file, model, batch_size)
    print(f"Finished processing SRT file: {input_srt_file}. Output saved to {output_srt_file}")

async def main():
    model = "gemma3:12b"
    batch_size = 10

    srt_files = [f for f in os.listdir() if f.endswith(".srt")]

    if not srt_files:
        print("No SRT files found in the current directory.")
        return

    for file in srt_files:
        await process_srt_file(file, model, batch_size)

if __name__ == "__main__":
    if torch.cuda.is_available():
        print("GPU is available. Utilizing GPU.")
    else:
        print("GPU is not available. Using CPU.")
    asyncio.run(main())
