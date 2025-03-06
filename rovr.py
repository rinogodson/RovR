import curses
import os

def main(stdscr):
  curses.curs_set(0)
  stdscr.clear()

  c_dir = os.getcwd()
  f_list = sorted(os.listdir(c_dir))

  f_index = 0

  history = []

  while True:
    stdscr.addstr(1, 1, f" 📂 {c_dir}", curses.A_BOLD)

    for i, item in enumerate(f_list):
      if i == f_index:
        stdscr.attron(curses.A_REVERSE)

      if os.path.isdir(os.path.join(c_dir, item)):
        icon = "📁"
      elif os.path.isfile(os.path.join(c_dir, item)):
        icon = "📄"
      else:
        icon = "🕸️"
      stdscr.addstr(i + 3, 2, f"{icon} {item}")
      if i == f_index:
        stdscr.attroff(curses.A_REVERSE)

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
