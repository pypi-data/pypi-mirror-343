#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path
from rich import print
from rich.table import Table
from rich.console import Console
from rich.text import Text
import questionary

# Setup
note_dir = Path.home() / ".Note"
note_dir.mkdir(exist_ok=True)
console = Console()

# --- Helper Functions ---

# Removed git functions

def is_hidden_relative(path: Path, base_dir: Path):
    """Checks if any component of a path relative to base_dir is hidden (starts with '.')."""
    try:
        relative_path = path.relative_to(base_dir)
        return any(part.startswith('.') for part in relative_path.parts if str(part) != '.')
    except ValueError:
        return False

def get_note_paths():
    """Recursively gets all non-hidden .md file paths relative to note_dir."""
    notes = []
    for path in note_dir.rglob("*.md"):
        if is_hidden_relative(path, note_dir):
             continue
        notes.append(path)
    return notes

def get_topic_paths():
    """Recursively gets all non-hidden directory paths relative to note_dir."""
    topics = []
    for path in note_dir.rglob("*"):
         if path == note_dir:
              continue
         if path.is_dir():
            if is_hidden_relative(path, note_dir):
                 continue
            topics.append(path)
    return topics

def get_creation_base_dirs():
    """Returns a list of (display_string, Path_object) tuples for valid directories to create within (root + all topics)."""
    base_dirs = [(".", note_dir)]
    base_dirs.extend([(str(p.relative_to(note_dir)), p) for p in get_topic_paths()])
    return base_dirs

def get_editor_command():
    """Determines the editor command to use."""
    return os.environ.get("EDITOR") or "nvim"

# --- Core Functionality ---

def list_notes():
    """Lists notes and topics, excluding hidden items."""
    table = Table(title="[bold blue]Your Notes and Topics[/bold blue]", show_lines=True, border_style="blue")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Path", style="green")

    items_listed = False

    topic_list = sorted(get_topic_paths())
    for path in topic_list:
         table.add_row("Topic", path.name, str(path.relative_to(note_dir)))
         items_listed = True # Correct indentation for this loop

    note_list = sorted(get_note_paths())
    for path in note_list:
        table.add_row("Note", path.stem, str(path.relative_to(note_dir)))
        items_listed = True # Correct indentation for this loop

    if not items_listed:
         print("[yellow]No notes or topics found (excluding hidden items).[/yellow]")
    else:
        console.print(table)

def create_note(in_topic=None):
    """Creates a new note and optionally opens it in the editor."""
    base_path = note_dir
    if in_topic:
        topic_path = note_dir / in_topic
        if not topic_path.is_dir():
            print(f"[red]Error: Topic '{in_topic}' not found.[/red]")
            return
        base_path = topic_path

    name = questionary.text("New note name (without .md):").ask()
    if not name:
        print("[yellow]Note creation cancelled.[/yellow]")
        return

    name = name.strip().replace(' ', '_').replace('/', '-').replace('\\', '-')

    if not name:
        print("[red]Invalid note name after cleanup.[/red]")
        return

    filepath = base_path / f"{name}.md"

    if filepath.exists():
        print(f"[yellow]Note already exists:[/yellow] {filepath}")
        if questionary.confirm("Do you want to open the existing note instead?").ask():
             open_note_path(filepath)
        return

    try:
        filepath.touch()
        print(f"[green]Created:[/green] {filepath}")
        # Removed git add here

    except Exception as e:
        console.print(Text("[red]Error creating note:[/red] ") + Text(e))
        return

    should_open = questionary.confirm("Do you want to open this note now?").ask()
    if should_open is True:
        open_note_path(filepath)
    elif should_open is None:
         print("[yellow]Opening note cancelled.[/yellow]")


def create_topic():
    """Creates a new topic (folder) within a selected directory."""
    base_dir_choices_data = get_creation_base_dirs()
    choices = [display for display, path in base_dir_choices_data]
    choices.insert(0, "Back")

    selected_display = questionary.select("Choose where to create the new topic:", choices=choices).ask()

    if selected_display is None or selected_display == "Back":
        print("[yellow]Topic creation cancelled.[/yellow]")
        return

    selected_base_path = next((path for display, path in base_dir_choices_data if display == selected_display), None)

    if not selected_base_path:
         print("[red]Error: Could not determine selected path.[/red]")
         return

    folder = questionary.text(f"New topic name (in {selected_display}):").ask()
    if not folder:
        print("[yellow]Topic creation cancelled.[/yellow]")
        return

    folder = folder.strip().replace(' ', '_').replace('/', '-').replace('\\', '-')

    if not folder:
         print("[red]Invalid topic name after cleanup.[/red]")
         return

    topic_path = selected_base_path / folder

    if topic_path.exists():
        print(f"[yellow]Topic already exists:[/yellow] {topic_path}[/yellow]")
        return

    try:
        topic_path.mkdir()
        print(f"[green]Created topic:[/green] {topic_path}")
        # Removed git add here
    except Exception as e:
        console.print(Text("[red]Error creating topic:[/red] ") + Text(e))


def create_note_in_topic():
    """Guides the user to create a note within an existing topic (any level)."""
    topic_paths = get_topic_paths()
    if not topic_paths:
        print("[yellow]No topics found to create notes in. Create one first.[/yellow]")
        return

    choices = sorted([str(p.relative_to(note_dir)) for p in topic_paths])
    choices.insert(0, "Back")

    selected_rel_path_str = questionary.select("Choose topic to create note in:", choices=choices).ask()

    if selected_rel_path_str is None or selected_rel_path_str == "Back":
        print("[yellow]Note creation in topic cancelled.[/yellow]")
        return

    create_note(in_topic=selected_rel_path_str)


def open_note_path(note_path: Path):
    """Opens a specific note file in the editor."""
    if not note_path.is_file():
         print(f"[red]Error: Not a valid note file: {note_path}[/red]")
         return

    editor = get_editor_command()
    print(f"[dim]Opening {note_path.relative_to(note_dir)} in {editor}...[/dim]")
    try:
        subprocess.run([editor, str(note_path)], cwd=note_dir)
    except FileNotFoundError:
        print(f"[red]Error: Editor '{editor}' not found.[/red]")
        print("Please ensure your editor (like nvim) is installed and in your PATH,")
        print("or set the EDITOR environment variable.")
    except Exception as e:
        console.print(Text("[red]An error occurred while trying to open the note:[/red] ") + Text(e))


def open_note_interactive():
    """Prompts user to select a note and opens it."""
    all_notes_paths = get_note_paths()
    if not all_notes_paths:
        print("[yellow]No notes found (excluding hidden items).[/yellow]")
        return

    choices = sorted([str(p.relative_to(note_dir)) for p in all_notes_paths])
    choices.insert(0, "Back")

    selected_rel_path = questionary.select("Choose a note to open:", choices=choices).ask()

    if selected_rel_path is None or selected_rel_path == "Back":
        print("[yellow]Opening note cancelled.[/yellow]")
        return

    note_to_open = note_dir / selected_rel_path
    open_note_path(note_to_open)


def delete_item():
    """Deletes a selected note or topic."""
    all_items = []
    all_items.extend([(str(p.relative_to(note_dir)), "Note") for p in get_note_paths()])
    all_items.extend([(str(p.relative_to(note_dir)), "Topic") for p in get_topic_paths()])

    if not all_items:
        print("[yellow]No notes or topics found to delete (excluding hidden items).[/yellow]")
        return

    all_items.sort(key=lambda item: item[0])

    choices = [f"[{item_type}] {item_path}" for item_path, item_type in all_items]
    choices.insert(0, "Back")

    selected_choice = questionary.select("Select item to delete:", choices=choices).ask()

    if selected_choice is None or selected_choice == "Back":
        print("[yellow]Deletion cancelled.[/yellow]")
        return

    parts = selected_choice.split("] ", 1)
    if len(parts) != 2:
         print("[red]Error parsing selected item.[/red]")
         return

    item_type_bracket = parts[0]
    selected_rel_path = parts[1]

    item_type = item_type_bracket.strip("[")

    selected_path = note_dir / selected_rel_path

    confirm_message = f"Are you sure you want to DELETE {item_type} '{selected_rel_path}'?"
    if item_type == "Topic":
        confirm_message += " [This will delete EVERYTHING inside it!]"
        print("[bold red]WARNING: Deleting a topic is permanent and removes all contents.[/bold red]")

    if not questionary.confirm(confirm_message).ask():
        print("[yellow]Deletion cancelled.[/yellow]")
        return

    try:
        if selected_path.is_file():
            selected_path.unlink()
            print(f"[green]Deleted Note:[/green] {selected_rel_path}")
        elif selected_path.is_dir():
            shutil.rmtree(selected_path)
            print(f"[green]Deleted Topic:[/green] {selected_rel_path}")
        else:
            print(f"[red]Error: Item not found or not a file/directory: {selected_rel_path}[/red]")
            return

        # Removed git add here

    except OSError as e:
        print(f"[red]Error deleting {item_type.lower()} '{selected_rel_path}': {e}[/red]")
    except Exception as e:
        console.print(Text("[red]An unexpected error occurred during deletion:[/red] ") + Text(e))

# Removed git_commit
# Removed git_push
# Removed git_pull
# Removed manage_remote

def open_note_directory():
    """Opens the main note directory in the editor by changing directory first."""
    editor = get_editor_command()
    print(f"[dim]Changing directory to {note_dir} and opening in {editor}...[/dim]")
    try:
        subprocess.run([editor, "."], cwd=note_dir)
    except FileNotFoundError:
        print(f"[red]Error: Editor '{editor}' not found.[/red]")
        print("Please ensure your editor is installed and in your PATH,")
        print("or set the EDITOR environment variable.")
    except Exception as e:
        console.print(Text("[red]An error occurred while trying to open the directory:[/red> ") + Text(e))


# --- Sub-Menus ---

def creation_menu():
    """Menu for note and topic creation options."""
    print("\n[bold cyan]--- Creation Menu ---[/bold cyan]")
    action = questionary.select(
        "What do you want to create?",
        choices=[
            "Create New Note (in root)",
            "Create New Topic (Choose parent)",
            "Create Note in Topic (Choose topic)",
            "Back to Main Menu",
        ],
        qmark="✨"
    ).ask()

    if action == "Create New Note (in root)":
        create_note()
    elif action == "Create New Topic (Choose parent)":
        create_topic()
    elif action == "Create Note in Topic (Choose topic)":
        create_note_in_topic()
    elif action == "Back to Main Menu":
        print("[dim]Returning to main menu...[/dim]")
        return
    else:
         if action is None:
              print("[yellow]Operation cancelled. Returning to main menu.[/yellow]")
              return

# Removed git_menu

# --- Main Menu ---

def main_menu():
    """Displays the main menu and handles user choices."""
    print("\n[bold cyan]Welcome to dotNote![/bold cyan] [dim](~/.Note)[/dim]")
    action = questionary.select(
        "What do you want to do?",
        choices=[
            "Open a Note",
            "Open Note Directory in Editor",
            "List Notes & Topics",
            "Create...",
            "Delete Note or Topic",
            # Removed "Git..." option
            "Exit",
        ],
        qmark="👉"
    ).ask()

    if action == "Open a Note":
        open_note_interactive()
    elif action == "Open Note Directory in Editor":
        open_note_directory()
    elif action == "List Notes & Topics":
        list_notes()
    elif action == "Create...":
        creation_menu()
    elif action == "Delete Note or Topic":
        delete_item()
    # Removed elif for "Git..."
    elif action == "Exit":
        print("[bold yellow]Exiting dotNote. Happy note-taking![/bold yellow]")
        sys.exit()
    else:
         if action is None:
              print("[yellow]Operation cancelled. Exiting.[/yellow]")
              sys.exit()


# --- Script Entry Point ---

if __name__ == "__main__":
    try:
        import rich
        import questionary
        from rich.text import Text
    except ImportError:
        print("[red]Error: Missing required libraries.[/red]")
        print("Please install them using: [bold green]pip install rich questionary[/bold green]")
        sys.exit(1)

    # Removed Git executable check

    editor_command = get_editor_command()
    if not shutil.which(editor_command):
        print(f"[yellow]Warning: Editor '{editor_command}' not found.[/yellow]")
        print("Opening notes or the directory might not work unless you have an editor set up.")

    while True:
        try:
            main_menu()
        except EOFError:
            print("\n[bold yellow]Exiting due to EOF.[/bold yellow]")
            sys.exit()
        except KeyboardInterrupt:
            print("\n[bold yellow]Operation interrupted.[/bold yellow]")
        except Exception as e:
            console.print(Text("[red]An unexpected error occurred:[/red> ") + Text(e))
            import traceback
            traceback.print_exc()
            if not questionary.confirm("Continue?").ask():
                 sys.exit()

