import os
import sys
import platform
import time
import datetime as dt
from pathlib import Path
from IPython.display import display, HTML, Markdown

__author__ = "Romuald POTEAU"
__maintainer__ = "Romuald POTEAU"
__email__ = "romuald.poteau@univ-tlse3.fr"
__status__ = "Development"

_start_time = None
_end_time = None
_chrono_start = None
_chrono_stop = None
_css_loaded = False

class fg:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    LIGHTGRAY = "\033[37m"
    DARKGRAY = "\033[90m"
    BLACK = '\033[30m'
    WHITE = "\033[38;5;231m"
    OFF = '\033[0m'

class hl:
    BLINK = "\033[5m"
    blink = "\033[25m" #reset blink
    BOLD = '\033[1m'
    bold = "\033[21m" #reset bold
    UNDERL = '\033[4m'
    underl = "\033[24m" #reset underline
    ITALIC = "\033[3m"
    italic = "\033[23m"
    OFF = '\033[0m'

class bg:
    DARKRED = "\033[38;5;231;48;5;52m"
    DARKREDB = "\033[38;5;231;48;5;52;1m"
    LIGHTRED = "\033[48;5;217m"
    LIGHTREDB = "\033[48;5;217;1m"
    LIGHTYELLOW = "\033[48;5;228m"
    LIGHTYELLOWB = "\033[48;5;228;1m"
    LIGHTGREEN = "\033[48;5;156m"
    LIGHTGREENB = "\033[48;5;156;1m"
    LIGHTBLUE = "\033[48;5;117m"
    LIGHTBLUEB = "\033[48;5;117;1m"
    OFF = "\033[0m"

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    LIGHTGRAY = "\033[37m"
    DARKGRAY = "\033[90m"    
    BLACK = '\033[30m'
    WHITE = "\033[38;5;231m"
    BOLD = '\033[1m'
    OFF = '\033[0m'

def css_styling(base_path: Path):
    global _css_loaded
    css_file = base_path / "css" / "visualID.css"
    if not _css_loaded and css_file.exists():
        styles = css_file.read_text(encoding="utf-8")
        display(HTML(f"<style>{styles}</style>"))
        _css_loaded = True

def embed_banner(base_path: Path):
    svg_path = base_path / "svg" / "pyPCBanner.svg"
    if svg_path.exists():
        svg_content = svg_path.read_text(encoding="utf-8")
        display(HTML(f'<div style="text-align:center;">{svg_content}</div>'))

def embed_end(base_path: Path):
    svg_path = base_path / "svg" / "logoEnd.svg"
    if svg_path.exists():
        svg_content = svg_path.read_text(encoding="utf-8")
        display(HTML(f'<div style="text-align:center;">{svg_content}</div>'))

def display_md(text: str):
    display(Markdown(text))

def hdelay(sec: int) -> str:
    return str(dt.timedelta(seconds=int(sec)))

def hdelay_ms(delay) -> str:
    if isinstance(delay, (int, float)):
        delay = dt.timedelta(seconds=delay)
    sec = delay.total_seconds()
    hh = sec // 3600
    mm = (sec // 60) - (hh * 60)
    ss = sec - hh * 3600 - mm * 60
    ms = (sec - int(sec)) * 1000
    return f'{hh:02.0f}:{mm:02.0f}:{ss:02.0f} {ms:03.0f}ms'

def chrono_start():
    global _chrono_start, _chrono_stop
    _chrono_start = time.time()

def chrono_stop(hdelay=False):
    global _chrono_start, _chrono_stop
    _chrono_stop = time.time()
    sec = _chrono_stop - _chrono_start
    return hdelay_ms(sec) if hdelay else sec

def chrono_show():
    print('\nDuration :', hdelay_ms(time.time() - _chrono_start))

def init(base_path: Path = None):
    global _start_time
    if base_path is None:
        base_path = Path(__file__).parent
    else:
        base_path = Path(base_path)
    css_styling(base_path)
    _start_time = dt.datetime.now()

    start_time = _start_time.strftime("%A %d %B %Y, %H:%M:%S")
    host = platform.uname()
    h = f"{host.node} ({host.system})"
    md = f'**Start at:** {start_time}  \n'
    md += f'**Hostname:** {h}'
    display_md(md)
    embed_banner(base_path)

def end(base_path: Path = None):
    global _end_time
    if base_path is None:
        base_path = Path(__file__).parent
    else:
        base_path = Path(base_path)
    _end_time = dt.datetime.now()
    end_time = time.strftime("%A %d %B %Y, %H:%M:%S")
    duration = hdelay_ms(_end_time - _start_time)
    md = f'**End at:** {end_time}  \n'
    md += f'**Duration:** {duration}'
    display_md(md)
    embed_end(base_path)

if __name__ == "somos.config.visualID_Eng":
    try:
        base_path = Path(__file__).parent
        init(base_path)
    except Exception as e:
        print(f"[visualID_Eng] Could not auto-init: {e}")
