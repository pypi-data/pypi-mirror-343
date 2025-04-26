# xtnote - Simple CLI Note Manager

`xtnote` is a command-line tool for managing your notes and topics directly from your terminal. It stores notes as plain Markdown files in a dedicated directory (`~/.Note`) and provides an interactive menu for common note-taking tasks.

## Features

* **Interactive Menu:** Navigate common actions using arrow keys.
* **Note Creation:** Create new Markdown notes (`.md`) in the root of your notes directory or within topics.
* **Topic (Folder) Creation:** Organize your notes by creating topics. Supports nested topics.
* **Nested Structure:** Create notes and topics inside existing topics to build a hierarchical structure.
* **List Items:** View a structured list of all your notes and topics.
* **Open Items:** Select a note to open it in your preferred command-line editor (like `nvim`, `vim`, `nano`, etc.). You can also open the entire `~/.Note` directory in your editor.
* **Delete Items:** Safely delete notes or topics (with confirmation).
* **Configurable Editor:** Uses the `EDITOR` environment variable, falling back to `nvim` if not set.

## Installation

You can install `xtnote` using pip:

```bash
pip install xtnote

