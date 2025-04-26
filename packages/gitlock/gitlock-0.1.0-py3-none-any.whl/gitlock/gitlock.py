import os
import argparse
import json
import fnmatch
from gitlock.encryption_utils import encrypt_file, decrypt_file

def main():
    parser = argparse.ArgumentParser(description="GitLock: Password-protect your public repos.")
    parser.add_argument('command', choices=['encrypt', 'decrypt'], help='encrypt or decrypt files')
    parser.add_argument('--path', required=True, help='Path to the folder')
    parser.add_argument('--password', required=True, help='Password to encrypt/decrypt')
    parser.add_argument('--exclude', nargs='*', default=[], help='List of filename patterns to exclude')
    args = parser.parse_args()

    if args.command == 'encrypt':
        encrypted_files = []
        for root, dirs, files in os.walk(args.path):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                skip = False
                for pattern in args.exclude:
                    if fnmatch.fnmatch(file, pattern):
                        skip = True
                        break
                if skip or file.lower() in ['readme.md', '.gitlock']:
                    continue
                file_path = os.path.join(root, file)

                print(f"Encrypting {file_path}...")  # <-- ADD this so you can see!

                encrypt_file(file_path, args.password)
                encrypted_files.append(file_path)
        
        # Save .gitlock metadata
        metadata_path = os.path.join(args.path, '.gitlock')
        with open(metadata_path, 'w') as f:
            json.dump(encrypted_files, f)
        print(f"Saved encrypted file list to {metadata_path}")

    elif args.command == 'decrypt':
        metadata_path = os.path.join(args.path, '.gitlock')
        with open(metadata_path, 'r') as f:
            encrypted_files = json.load(f)

        for file_path in encrypted_files:
            print(f"Decrypting {file_path}...")  # <-- ADD this so you can see!
            decrypt_file(file_path, args.password)

if __name__ == "__main__":
    main()
