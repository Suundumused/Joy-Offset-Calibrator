import ctypes
import subprocess

from translation import translate_txt

def show_message(message):
    try:
        try:
            ctypes.windll.user32.MessageBoxW(0, translate_txt(message), "Error", 0x10)
        except:
            raise Exception
    except:
        subprocess.run(["zenity", "--error", "--text", translate_txt(message)])