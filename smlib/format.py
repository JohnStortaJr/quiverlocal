#!/usr/bin/python3

class color:
   BLACK = "\033[0;30m"    # If the terminal background is black, then the text will be unreadable
   RED = "\033[0;31m"
   GREEN = "\033[0;32m"
   YELLOW = "\033[0;33m"
   BLUE = "\033[0;34m"
   MAGENTA = "\033[0;35m"
   CYAN = "\033[0;36m"
   WHITE = "\033[0;37m"

   # These are the same colors as above, but the text is also BOLD and more readable
   BBLACK = "\033[1;30m"   # Unlike above, this text is more of a dark gray and still reable
   BRED = "\033[1;31m"
   BGREEN = "\033[1;32m"
   BYELLOW = "\033[1;33m"
   BBLUE = "\033[1;34m"
   BMAGENTA = "\033[1;35m"
   BCYAN = "\033[1;36m"

   # White on light gray makes this almost unreadable
   BWHITE = "\033[1;37m"

   END = "\033[0m"


class style:
   BOLD = "\033[1m"
   FAINT = "\033[2m"
   ITALIC = "\033[3m"
   UNDERLINE = "\033[4m"
   BLINK = "\033[5m"

   # This give black text on a white background
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
   WHITE = "\u001b[47m"    # This makes white text on a white background which completely obscures the text

   # These are the same background colors as above, but the text is BOLD
   BBLACK = "\u001b[40;1m"
   BRED = "\u001b[41;1m"
   BGREEN = "\u001b[42;1m"
   BYELLOW = "\u001b[43;1m"
   BBLUE = "\u001b[44;1m"
   BMAGENTA = "\u001b[45;1m"
   BCYAN = "\u001b[46;1m"
   BWHITE = "\u001b[47;1m"    # This text would be barely readable

   END = "\u001b[0m"