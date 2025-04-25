#!/usr/bin/env python3
import os
import subprocess
import shutil
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.patch_stdout import patch_stdout


def get_terminal_size():
    try:
        return os.get_terminal_size()
    except:
        return (80, 24)  # Default size if terminal detection fails


def get_history_path():
    histfile = os.getenv("HISTFILE")
    if not histfile:
        histfile = os.path.expanduser("~/.bash_history")
    if not os.path.exists(histfile):
        zsh_hist = os.path.expanduser("~/.zsh_history")
        if os.path.exists(zsh_hist):
            histfile = zsh_hist
    return histfile


def backup_history(history_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{history_file}.bak_{timestamp}"
    shutil.copy2(history_file, backup_path)
    return backup_path


def load_history():
    history_file = get_history_path()
    if not os.path.exists(history_file):
        return [], history_file, False

    with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
        history = [line.strip() for line in f.readlines() if line.strip()]

    seen = set()
    unique_history = []
    for cmd in reversed(history):
        if cmd not in seen:
            seen.add(cmd)
            unique_history.append(cmd)

    return list(reversed(unique_history)), history_file, False


def save_history(history, history_file):
    with open(history_file, "w", encoding="utf-8") as f:
        f.write("\n".join(history) + "\n")


async def confirm_deletion():
    session = PromptSession()
    with patch_stdout():
        answer = await session.prompt_async("Delete this entry? (y/n) ")
        return answer.lower().startswith("y")


async def main():
    history, history_file, modified = load_history()
    undo_stack = []
    backup_created = False
    _, term_rows = get_terminal_size()
    visible_lines = term_rows - 5  # Reserve space for header/footer

    if not history:
        print("No history found in:", history_file)
        return

    bindings = KeyBindings()
    current_selection = len(history) - 1
    scroll_offset = max(0, current_selection - visible_lines + 1)

    def display_history():
        print("\033c", end="")
        status = "[MODIFIED]" if modified else ""
        print(
            f"Bash History {status} (↑/↓: navigate, Enter: execute, Delete: remove, Ctrl+Z: undo, Ctrl+C: quit)"
        )
        print(f"Editing: {history_file}")
        if backup_created:
            print(f"Backup created: {history_file}.bak_*")
        print()

        start_idx = scroll_offset
        end_idx = min(len(history), start_idx + visible_lines)

        for i in range(start_idx, end_idx):
            prefix = "> " if i == current_selection else "  "
            line_num = f"{i+1}:".ljust(5)
            print(f"{prefix}{line_num}{history[i]}")

        # Footer with navigation info
        print("\n" + "-" * 50)
        if scroll_offset > 0:
            print("↑↑↑ More items above ↑↑↑")
        if end_idx < len(history):
            print("↓↓↓ More items below ↓↓↓")

    def update_scroll_position():
        nonlocal scroll_offset
        if current_selection < scroll_offset:
            scroll_offset = current_selection
        elif current_selection >= scroll_offset + visible_lines:
            scroll_offset = max(0, current_selection - visible_lines + 1)

    @bindings.add("delete")
    async def _(event):
        nonlocal history, modified, undo_stack, backup_created, current_selection
        if not history:
            return

        # Show confirmation prompt
        event.app.exit(result=False)
        should_delete = await confirm_deletion()

        if not should_delete:
            display_history()
            return

        if not backup_created:
            backup_history(history_file)
            backup_created = True

        undo_stack.append((current_selection, history[current_selection]))
        del history[current_selection]

        if current_selection >= len(history) and len(history) > 0:
            current_selection = len(history) - 1

        modified = True
        save_history(history, history_file)
        update_scroll_position()
        display_history()

    @bindings.add("c-z")
    def _(event):
        nonlocal history, modified, undo_stack, current_selection
        if undo_stack:
            pos, cmd = undo_stack.pop()
            history.insert(pos, cmd)
            current_selection = pos
            modified = bool(undo_stack)
            save_history(history, history_file)
            update_scroll_position()
            display_history()

    @bindings.add("up")
    def _(event):
        nonlocal current_selection
        if current_selection > 0:
            current_selection -= 1
            update_scroll_position()
            display_history()

    @bindings.add("down")
    def _(event):
        nonlocal current_selection
        if current_selection < len(history) - 1:
            current_selection += 1
            update_scroll_position()
            display_history()

    @bindings.add("pageup")
    def _(event):
        nonlocal current_selection, scroll_offset
        current_selection = max(0, current_selection - visible_lines)
        scroll_offset = max(0, scroll_offset - visible_lines)
        display_history()

    @bindings.add("pagedown")
    def _(event):
        nonlocal current_selection, scroll_offset
        current_selection = min(len(history) - 1, current_selection + visible_lines)
        scroll_offset = min(len(history) - visible_lines, scroll_offset + visible_lines)
        display_history()

    @bindings.add("enter")
    def _(event):
        if history:
            selected_command = history[current_selection]
            print(f"\nExecuting: {selected_command}\n")
            try:
                subprocess.run(selected_command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
        event.app.exit()

    @bindings.add("c-c")
    def _(event):
        print("\nExiting...")
        event.app.exit()

    display_history()
    session = PromptSession(key_bindings=bindings)

    with patch_stdout():
        await session.prompt_async()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
