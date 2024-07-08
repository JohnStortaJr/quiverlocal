#!/usr/bin/python3

class color:
   BLACK = "\033[0;30m"
   RED = "\033[0;31m"
   GREEN = "\033[0;32m"
   YELLOW = "\033[0;33m"
   BLUE = "\033[0;34m"
   MAGENTA = "\033[0;35m"
   CYAN = "\033[0;36m"
   WHITE = "\033[0;37m"

   LBLACK = "\033[1;30m"
   LRED = "\033[1;31m"
   LGREEN = "\033[1;32m"
   LYELLOW = "\033[1;33m"
   LBLUE = "\033[1;34m"
   LMAGENTA = "\033[1;35m"
   LCYAN = "\033[1;36m"
   LWHITE = "\033[1;37m"

   END = "\033[0m"


class style:
   BOLD = "\033[1m"
   FAINT = "\033[2m"
   ITALIC = "\033[3m"
   UNDERLINE = "\033[4m"
   BLINK = "\033[5m"
   NEGATIVE = "\033[7m"
   CROSSED = "\033[9m"

   END = "\033[0m"

class background:
   BLACK = "\u001b[40m"
   RED = "\u001b[41m"
   GREEN = "\u001b[42m"
   YELLOW = "\u001b[43m"
   BLUE = "\u001b[44m"
   MAGENTA = "\u001b[45m"
   CYAN = "\u001b[46m"
   WHITE = "\u001b[47m"
   
   BBLACK = "\u001b[40;1m"
   BRED = "\u001b[41;1m"
   BGREEN = "\u001b[42;1m"
   BYELLOW = "\u001b[43;1m"
   BBLUE = "\u001b[44;1m"
   BMAGENTA = "\u001b[45;1m"
   BCYAN = "\u001b[46;1m"
   BWHITE = "\u001b[47;1m"

   END = "\u001b[0m"