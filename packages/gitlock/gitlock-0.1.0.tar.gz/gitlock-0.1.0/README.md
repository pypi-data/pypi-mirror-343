# GitLock

**GitLock** is a simple tool that allows you to password-protect the contents of your public Git repositories by encrypting files.  
Keep your repos public — but lock the important stuff!

---

## Features
- 🔒 Encrypt all files in a repo (except `.git`, `README.md`, and others you choose)
- 🔓 Decrypt files easily with a password
- 🗂️ Store a `.gitlock` metadata file to track encrypted files
- 🛡️ Optional file exclusion patterns (e.g., skip `.md` files)

---

## Installation

### 1. Clone GitLock

```bash
git clone https://github.com/yourusername/gitlock.git
cd gitlock
```

### 2. Set up a Python virtual environment (recommended)

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install required dependencies

```bash
pip install cryptography
```

---

## Usage

### Encrypt a repository

```bash
python3 gitlock.py encrypt --path ./myrepo --password yourSecretPassword
```

- `--path` = the folder you want to encrypt
- `--password` = password you want to use for encryption

### Decrypt a repository

```bash
python3 gitlock.py decrypt --path ./myrepo --password yourSecretPassword
```

---

## Example

Suppose your repo looks like this:

```
myrepo/
  ├── secret.txt
  ├── README.md
```

To encrypt:

```bash
python3 gitlock.py encrypt --path ./myrepo --password myPassword123
```

- `secret.txt` will be encrypted.
- `README.md` will stay unencrypted.

To decrypt:

```bash
python3 gitlock.py decrypt --path ./myrepo --password myPassword123
```

---

## Notes

- The `.gitlock` file must stay in the repo — it tells GitLock which files to decrypt.
- Files like `.git`, `.gitlock`, and `README.md` are automatically skipped.
- You can exclude additional files when encrypting:

```bash
python3 gitlock.py encrypt --path ./myrepo --password yourSecretPassword --exclude "*.md" "*.png"
```

---

## Troubleshooting

- If you see `ModuleNotFoundError: No module named 'cryptography'`, install it:

```bash
pip install cryptography
```

- Always activate your environment before using GitLock:

```bash
source myenv/bin/activate
```

---

## Coming Soon

- `pip install gitlock`
- Usage like:

```bash
gitlock encrypt --path ./myrepo --password yourSecretPassword
```
instead of needing to clone manually!

Stay tuned! 🚀
