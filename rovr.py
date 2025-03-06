import curses
import os

dotFiles = False

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

    curses.curs_set(0)
  
    # Variables:
    c_dir = os.getcwd()
    f_list = filterList(sorted(os.listdir(c_dir)), c_dir)
    f_index = 0
    history = []
    search_query = ""
    height, width = stdscr.getmaxyx()
    max_visible_items = height - 6
    scroll_offset = max(0, f_index - max_visible_items + 1)

    while True:
        stdscr.clear()

        # Handle scrolling
        if f_index < scroll_offset:
            scroll_offset = f_index
        elif f_index >= scroll_offset + max_visible_items:
            scroll_offset = f_index - max_visible_items + 1

        stdscr.border(0)
        stdscr.addstr(0, 2, " RovR 🛰 ", curses.A_BOLD)
        stdscr.addstr(1, 2, f"💾 {c_dir}", curses.A_BOLD)

        # Apply search filter
        if search_query:
            filtered_list = [item for item in f_list if search_query.lower() in item.lower()]
        else:
            filtered_list = f_list

        # If search has no matches
        if not filtered_list:
            filtered_list = ["(No Results Found)"]
            f_index = 0

        # Display files and folders
        for i, item in enumerate(filtered_list[scroll_offset:scroll_offset + max_visible_items]):
            full_path = os.path.join(c_dir, item)
            is_dir = os.path.isdir(full_path)
            actual_index = i + scroll_offset
            color = curses.color_pair(1) if is_dir else curses.color_pair(2)
            display_text = f"{' 📁' if is_dir else ' 📄'} {item}"
            padded_text = ">" + display_text.ljust(width - 6)

            if actual_index == f_index:
                stdscr.attron(curses.color_pair(3))
                stdscr.attron(curses.A_BOLD)
                stdscr.addstr(i + 3, 2, padded_text)
                stdscr.attroff(curses.color_pair(3))
                stdscr.attron(curses.A_BOLD)
            else:
                stdscr.addstr(i + 3, 2, display_text, color)

        # Show search bar
        stdscr.addstr(height - 2, 2, f" 🔍 Search: {search_query}", curses.A_BOLD)

        key = stdscr.getch()

        if key == curses.KEY_UP and f_index > 0:
            f_index -= 1
        elif key == curses.KEY_DOWN and f_index < len(filtered_list) - 1:
            f_index += 1
        elif key in (ord('q'), 27):  # Quit on 'q' or ESC
            break

        # Open folder on RIGHT arrow
        elif key == curses.KEY_RIGHT:
            selected_item = filtered_list[f_index]
            new_path = os.path.join(c_dir, selected_item)

            if os.path.isdir(new_path):
                try:
                    history.append(c_dir)
                    c_dir = new_path
                    f_list = filterList(sorted(os.listdir(c_dir)), c_dir)
                    f_index = 0
                    search_query = ""  # Reset search when changing directories
                except PermissionError:
                    stdscr.addstr(len(f_list) + 4, 2, "🚫 Access Denied", curses.color_pair(1))

        # Go back on LEFT arrow
        elif key == curses.KEY_LEFT:
            parent_dir = os.path.dirname(c_dir)
            dir_name = os.path.basename(c_dir)
            if parent_dir != c_dir:
                c_dir = parent_dir
            f_list = filterList(sorted(os.listdir(c_dir)), c_dir)
            f_index = f_list.index(dir_name) if dir_name in f_list else 0
            search_query = ""  # Reset search when going back
            history.append(dir_name)

        # Search functionality
        elif key == 27:  # Esc clears search
            search_query = ""
        elif key in (curses.KEY_BACKSPACE, 127):  # Backspace deletes last char
            search_query = search_query[:-1]
        elif 32 <= key <= 126:  # Typable characters (A-Z, a-z, 0-9, etc.)
            search_query += chr(key)

        stdscr.refresh()

def filterList(arr, c):
    if not arr:
        return []
    if not dotFiles:
        return sort_folders_first(list(filter(lambda item: not item.startswith("."), arr)), c)
    else:
        return sort_folders_first(arr, c)

def sort_folders_first(file_list, current_path):
    return sorted(file_list, key=lambda item: (not os.path.isdir(os.path.join(current_path, item)), item.lower()))

curses.wrapper(main)