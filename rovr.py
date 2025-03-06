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

  while True:
    height, width = stdscr.getmaxyx()
    stdscr.border(0)
    stdscr.addstr(0, 2, " RovR 🛰 ", curses.A_BOLD)

    stdscr.addstr(1, 2, f" 📂 {c_dir}", curses.A_BOLD)

    for i, item in enumerate(f_list):
      full_path = os.path.join(c_dir, item)
      is_dir = os.path.isdir(full_path)

      color = curses.color_pair(1) if is_dir else curses.color_pair(2)

      display_text = f"{' 📁' if is_dir else ' 📄'}{item}"
      padded_text = ">"+display_text.ljust(width - 6)

      if i == f_index:
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
    stdscr.clear()
    stdscr.refresh()

curses.wrapper(main)
