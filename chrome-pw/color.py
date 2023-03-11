from ctypes import WINFUNCTYPE
import sys
import os

def _windows_enable_ANSI(std_id):
    """Enable Windows 10 cmd.exe ANSI VT Virtual Terminal Processing."""
    from ctypes import byref, POINTER, windll, WINFUNCTYPE
    from ctypes.wintypes import BOOL, DWORD, HANDLE

    GetStdHandle = WINFUNCTYPE(
        HANDLE,
        DWORD)(('GetStdHandle', windll.kernel32))

    GetFileType = WINFUNCTYPE(
        DWORD,
        HANDLE)(('GetFileType', windll.kernel32))

    GetConsoleMode = WINFUNCTYPE(
        BOOL,
        HANDLE,
        POINTER(DWORD))(('GetConsoleMode', windll.kernel32))

    SetConsoleMode = WINFUNCTYPE(
        BOOL,
        HANDLE,
        DWORD)(('SetConsoleMode', windll.kernel32))

    if std_id == 1:       # stdout
        h = GetStdHandle(-11)
    elif std_id == 2:     # stderr
        h = GetStdHandle(-12)
    else:
        return False

    if h is None or h == HANDLE(-1):
        return False

    #FILE_TYPE_CHAR = 0x0002
    #ft = GetFileType(h)
    #if (ft & 3) != FILE_TYPE_CHAR:
    #    return False

    mode = DWORD()
    GetConsoleMode(h, byref(mode))

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0007
    if (mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING) == 0:
        SetConsoleMode(h, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    return True


class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    # cancel SGR codes if we don't write to a terminal
    #if not __import__("sys").stdout.isatty():
    #    for _ in dir():
    #        if isinstance(_, str) and _[0] != "_":
    #            locals()[_] = ""
    #else:
    #    # set Windows console in VT mode
    #    if __import__("platform").system() == "Windows":
    #        kernel32 = __import__("ctypes").windll.kernel32
    #        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    #        del kernel32


_windows_enable_ANSI(1)
sys.stdout.write("Current Python version: %s\n" % (sys.version,))
for key, value in os.environ.items():
    print(f'{Colors.GREEN}{key}{Colors.END}={Colors.BLUE}{value}{Colors.END}')

