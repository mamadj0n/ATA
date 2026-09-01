# ATA (AI Terminal Assistant)

> [!NOTE]
> **Persian Documentation **
> 
> برای مطالعه راهنمای فارسی این پروژه، فایل [README_FA.md](./README_FA.md) را مشاهده کنید.

**ATA** is a lightweight, zero-dependency local CLI tool that converts natural language commands into executable Linux terminal operations using local Large Language Models (LLMs) via Ollama.

It acts as a bridge between your shell and local AI, eliminating the need to memorize complex bash syntax—while keeping your terminal secure and completely offline.

---

## Key Features

* **Zero External Dependencies:** Built entirely with Python's standard library (`urllib`, `subprocess`, `readline`). No `pip install` required.
* **Privacy First & Offline:** Powered locally by Ollama using `qwen2.5-coder:1.5b`. No API keys, tracking, or cloud latency.
* **Interactive Execution:** Preview generated commands before running them. Accept, decline, or edit suggestions on the fly.
* **Safety Built-In:** Automatic sanitization of markdown/inline backticks and pattern-matching against destructive system commands (e.g., `rm -rf /`).

---

## Prerequisites

1. **Ollama:** Make sure Ollama is installed and running on your system.
```bash
curl -fsSL https://ollama.com/install.sh | sh

```


2. **Local Model:** Pull the recommended coding model:
```bash
ollama pull qwen2.5-coder:1.5b

```



---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/mamadj0n/ATA.git
cd ATA

```


2. **Make the script executable:**
```bash
chmod +x main.py

```


3. **Install globally (as `ata` command):**
```bash
sudo cp main.py /usr/local/bin/ata

```



---

## Usage

Simply run `ata` followed by your request in plain English or Persian:

```bash
ata "whats my cpu"

```

### Options Prompt

After generating a command, ATA will prompt you:

```text
💡 Suggested Command:
  lscpu

Options: [y] Execute | [n] Cancel | [e] Edit
What to do? (y/N/e):

```

* **`y` (Yes / Default):** Executes the command directly in your shell.
* **`n` (No):** Cancels the execution safely.
* **`e` (Edit):** Load the generated command into the interactive prompt to tweak arguments before execution.

---

## Examples

**Find large files in your home directory:**

```bash
ata "find files larger than 100MB in home directory"

```

**Check active network connections:**

```bash
ata "show listening ports and associated processes"

```

---

## Customization

To change the default model, pass the `-m` or `--model` flag:

```bash
ata "compress images in current directory" -m llama3.2:1b

```

Alternatively, you can edit `DEFAULT_MODEL` inside `/usr/local/bin/ata` to set your preferred default local model.

---

## Security & Safety

* ATA includes an execution interceptor that displays a warning if a command matches hazardous patterns (e.g., `rm -rf /`, `mkfs`, raw device writes).
* No command is ever executed without explicit user confirmation (`y` / `e`).
