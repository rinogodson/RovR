import curses
import os

def main(stdscr):

  curses.start_color()
  curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

  curses.curs_set(0)
  stdscr.clear()
  
  #variables:
  c_dir = os.getcwd()
  f_list = sorted(os.listdir(c_dir))
  f_index = 0
  history = []
  height, width = stdscr.getmaxyx()
  max_visible_items = height - 6
  scroll_offset = max(0, f_index - max_visible_items + 1)

  while True:

    if f_index < scroll_offset:
      scroll_offset = f_index
    elif f_index >= scroll_offset + max_visible_items:
      scroll_offset = f_index - max_visible_items + 1

    stdscr.border(0)
    stdscr.addstr(0, 2, " RovR 🛰 ", curses.A_BOLD)

    stdscr.addstr(1, 2, f"💾{c_dir}", curses.A_BOLD)

    for i, item in enumerate(f_list[scroll_offset:scroll_offset + max_visible_items]):
      full_path = os.path.join(c_dir, item)
      is_dir = os.path.isdir(full_path)

      actual_index = i + scroll_offset

      color = curses.color_pair(1) if is_dir else curses.color_pair(2)

      display_text = f"{' 📁' if is_dir else ' 📄'}{item}"
      padded_text = ">"+display_text.ljust(width - 6)

      if actual_index == f_index:
          stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
          stdscr.addstr(i + 3, 2, padded_text)
          stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
      else:
          stdscr.addstr(i + 3, 2, display_text, color)

    key = stdscr.getch()

    if key == curses.KEY_UP and f_index > 0:
      f_index -= 1 
    elif key == curses.KEY_DOWN and f_index < len(f_list) - 1:
      f_index += 1  
    elif key in (ord('q'), 27):
      break    

    elif key == curses.KEY_RIGHT:
      selected_item = f_list[f_index]
      new_path = os.path.join(c_dir, selected_item)

      if(os.path.isdir(new_path)):
        try:
          history.append(c_dir)
          c_dir = new_path
          f_list = sorted(os.listdir(c_dir))
          if not f_list:
            f_list = ["(Empty Folder.)"]
          f_index = 0
        except PermissionError:
            stdscr.addstr(len(f_list) + 4, 2, "🚫 Access Denied", curses.color_pair(1))

    elif key == curses.KEY_LEFT:
      if history:
        c_dir = history.pop()
        f_list = sorted(os.listdir(c_dir))
        f_index = 0
      else:
        parent_dir = os.path.dirname(c_dir)
        if parent_dir != c_dir:  # Prevent infinite loop at root
            c_dir = parent_dir
        c_dir = parent_dir
        f_list = sorted(os.listdir(c_dir))
        f_index = 0
    stdscr.clear()
    stdscr.refresh()

curses.wrapper(main)
