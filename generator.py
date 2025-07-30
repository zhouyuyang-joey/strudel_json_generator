import argparse
import os
import json
import sys

def create_strudel_json(root_path, github_user, github_repo, github_branch):

    if not os.path.isdir(root_path):
        print(f"Error: The specified path '{root_path}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    audio_extensions = {'.wav', '.mp3', '.flac', '.aiff'}

    base_url = f"https://raw.githubusercontent.com/{github_user}/{github_repo}/{github_branch}/"
    strudel_data = {"_base": base_url}
    
    found_audio_files = False

    try:
        for entry in os.scandir(root_path):
            if entry.is_dir():
                folder_name = entry.name
                folder_path = entry.path
                
                audio_files = []

                for file_entry in os.scandir(folder_path):
                    if file_entry.is_file() and os.path.splitext(file_entry.name)[1].lower() in audio_extensions:
                        correct_path = f"{folder_name}/{file_entry.name}"
                        audio_files.append(correct_path)
                
                if not audio_files:
                    continue
                
                found_audio_files = True
                
                if len(audio_files) == 1:
                    strudel_data[folder_name] = audio_files[0]

                else:
                    strudel_data[folder_name] = sorted(audio_files)

    except OSError as e:
        print(f"Error scanning directory {root_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if not found_audio_files:
        print("Warning: No audio files found in the subdirectories of the specified path.")
        
    output_filename = 'strudel.json'
    try:
        with open(output_filename, 'w', encoding='utf-8') as json_file:
            json.dump(strudel_data, json_file, indent=4, ensure_ascii=False)
        print(f"Successfully generated '{output_filename}' in the current directory.")

    except IOError as e:
        print(f"Error writing to file {output_filename}: {e}", file=sys.stderr)
        sys.exit(1)


def main():

    parser = argparse.ArgumentParser(
        description="Generate a json file from a local directory structure for GitHub sample loading.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-p', '--path',
        required=True,
        help="Path to the local root directory to scan."
    )
    parser.add_argument(
        '-u', '--username',
        required=True,
        help="Your GitHub username (the one in your GitHub page URL)."
    )
    parser.add_argument(
        '-r', '--repo',
        required=True,
        help="Your GitHub repository name."
    )
    parser.add_argument(
        '-b', '--branch',
        default='main',
        help="Your GitHub repository branch name (You do not need to specify this if you have not made any changes)."
    )
    
    args = parser.parse_args()
    
    create_strudel_json(args.path, args.username, args.repo, args.branch)


if __name__ == '__main__':
    main()