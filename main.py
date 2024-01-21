# Created by chinchill (discord) please do not reupload, copy, change, modify without my consent, thanks :)
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedStyle
import threading
import time

app = tk.Tk()
app.title("CMM®")
app.resizable(False, False)

MODS_TO_EXCLUDE = set([
    "x64a.rpf", "x64b.rpf", "x64c.rpf", "x64d.rpf", "x64e.rpf", "x64f.rpf", "x64g.rpf", "x64h.rpf",
    "x64i.rpf", "x64j.rpf", "x64k.rpf", "x64l.rpf", "x64m.rpf", "x64n.rpf", "x64o.rpf", "x64p.rpf",
    "x64q.rpf", "x64r.rpf", "x64s.rpf", "x64t.rpf", "x64u.rpf", "x64v.rpf", "x64w.rpf", "x64x.rpf",
    "x64y.rpf", "x64z.rpf", "common.rpf", "GTA5.exe", "GTAVLanguageSelect.exe", "GTAVLauncher.exe",
    "bink2w64.dll", "d3dcompiler.dll", "d3dcsx.dll", "GFSDK_ShadowLib.win64.dll", "GFSDK_TXAA.win64.dll",
    "GFSDK_TXAA_AlphaResolve.win64.dll", "GPUPerfAPIDX11-x64.dll", "NvPmApi.Core.win64.dll", "version.txt",
    "index.bin", "d3dcompiler_46.dll", "d3dcsx_46.dll", "PlayGTAV.exe", "uninstall.exe", "commandline.txt",
    "zlib1.dll", "toxmod.dll", "opusenc.dll", "opus.dll", "libcurl.dll", "fvad.dll", "title.rgl",
])

FOLDERS_TO_EXCLUDE = set(["ReadMe", "Redistributables", "update", "x64"])

translations = {
    "en": {
        "title": "CMM®",
        "source_folder": "Folder with mods:",
        "destination_folder": "Destination Folder:",
        "move_button": "Move Mods",
        "success_message": "Mods have been moved.",
        "select_game_folder": "Select Game Folder",
        "select_destination_folder": "Select Destination Folder",
        "success": "Success!",
    },
    "pl": {
        "title": "CMM®",
        "source_folder": "Folder z modami:",
        "destination_folder": "Folder docelowy:",
        "move_button": "Przenieś mody",
        "success_message": "Mody zostały przeniesione.",
        "select_game_folder": "Wybierz folder z GTA V",
        "select_destination_folder": "Wybierz folder docelowy",
        "success": "Sukces!",
    },
}
current_language = "pl"  # Default language

def select_gta_v_directory():
    gta_v_directory = filedialog.askdirectory(title=translations[current_language]["select_game_folder"])
    if gta_v_directory:
        gta_v_entry.delete(0, tk.END)
        gta_v_entry.insert(0, gta_v_directory)

def select_destination_directory():
    destination_directory = filedialog.askdirectory(title=translations[current_language]["select_destination_folder"])
    if destination_directory:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, destination_directory)

def move_mod(mod, src_directory, dst_directory, pbar, progress_label, current_file_label):
    src_path = os.path.join(src_directory, mod)
    dst_path = os.path.join(dst_directory, mod)

    try:
        shutil.move(src_path, dst_path)
    except PermissionError:
        messagebox.showerror("Error", f"Cannot move mod '{mod}'. Permission denied. Set correct folder permissions.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while moving mod '{mod}': {str(e)}")
        return False

    return True

def move_mods(mods, src_directory, dst_directory, pbar, progress_label, current_file_label):
    total_mods = len(mods)
    current_file_label.config(text="")  # Set the initial text to an empty string

    for i, mod in enumerate(mods):
        current_progress = (i + 1) / total_mods * 100
        progress_label.config(text=f"{current_progress:.2f}%")
        file_name = f"{mod}"
        current_file_label.config(text=file_name)

        # Calculate the initial x position for the label to center it
        label_x = (app.winfo_width() - current_file_label.winfo_reqwidth()) / 2
        current_file_label.place(x=label_x, y=185)

        if not move_mod(mod, src_directory, dst_directory, pbar, progress_label, current_file_label):
            return False

        time.sleep(0.05)
        pbar.set(pbar.get() + 1)

    return True

def move_mods_async_handler():
    gta_v_directory = gta_v_entry.get()
    destination_directory = destination_entry.get()

    if not os.path.isdir(destination_directory):
        messagebox.showerror("Error", translations[current_language]["select_destination_folder"])
        return

    mods = os.listdir(gta_v_directory)
    mods_to_move = [mod for mod in mods if mod not in MODS_TO_EXCLUDE and mod not in FOLDERS_TO_EXCLUDE]

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(app, mode="determinate", variable=progress_var, maximum=len(mods_to_move))
    progress_bar.place(x=20, y=170, width=270, height=8)

    move_thread = threading.Thread(target=move_mods, args=(mods_to_move, gta_v_directory, destination_directory, progress_var, progress_label, current_file_label))
    move_thread.start()

    def show_success_message():
        move_thread.join()

        if progress_var.get() == progress_bar['maximum']:
            messagebox.showinfo(translations[current_language]["success"], translations[current_language]["success_message"])

        progress_bar.stop()

    success_thread = threading.Thread(target=show_success_message)
    success_thread.start()

def swap_directories():
    gta_v_directory = gta_v_entry.get()
    destination_directory = destination_entry.get()

    # Swap the values between the two entry widgets
    gta_v_entry.delete(0, tk.END)
    gta_v_entry.insert(0, destination_directory)
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, gta_v_directory)

def switch_to_english():
    global current_language
    current_language = "en"
    update_language()

def switch_to_polish():
    global current_language
    current_language = "pl"
    update_language()

def update_language():
    app.title(translations[current_language]["title"])
    source_folder_label.config(text=translations[current_language]["source_folder"])
    destination_folder_label.config(text=translations[current_language]["destination_folder"])
    move_mods_button.config(text=translations[current_language]["move_button"])

app.configure(bg="#2b2b2b")
style = ThemedStyle(app)
style.set_theme("equilux")

app.geometry("310x215")


def create_transparent_label(parent, x, y, text):
    label = tk.Label(parent, text=text, bg="#2b2b2b", fg="white")
    label.place(x=x, y=y)
    return label

def create_dlclist_txt(directory_path):
    dlclist_path = os.path.join(directory_path, "dlclist.txt")
    try:
        with open(dlclist_path, "w") as file:
            for folder_name in os.listdir(directory_path):
                if os.path.isdir(os.path.join(directory_path, folder_name)):
                    file.write(f"\t\t<Item>dlcpacks:/{folder_name}/</Item>\n")
        return dlclist_path
    except Exception as e:
        return str(e)

def select_directory():
    directory_path = filedialog.askdirectory(title="Select Directory")
    if directory_path:
        result = create_dlclist_txt(directory_path)
        open_dlclist(result)

def open_dlclist(file_path):
    try:
        if os.name == 'nt':  # Check if running on Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # Check if running on Linux or macOS
            subprocess.run(["xdg-open", file_path], check=True)
    except Exception as e:
        print(f"Error opening dlclist.txt: {e}")

select_button = ttk.Button(app, text="dc", command=select_directory, width=3)
select_button.place(x=37, y= 190)

english_button = ttk.Button(app, text="EN", command=switch_to_english, width=3)
english_button.place(x=275, y=190)

polish_button = ttk.Button(app, text="PL", command=switch_to_polish, width=3)
polish_button.place(x=5, y=190)

source_folder_label = create_transparent_label(app, 20, 5, translations[current_language]["source_folder"])
destination_folder_label = create_transparent_label(app, 20, 60, translations[current_language]["destination_folder"])

gta_v_entry = tk.Entry(app, width=40)
gta_v_entry.place(x=20, y=25)
select_gta_v_button = ttk.Button(app, text="...", command=select_gta_v_directory, width=1.5)
select_gta_v_button.place(x=270, y=24)

destination_entry = tk.Entry(app, width=40)
destination_entry.place(x=20, y=80)
select_destination_button = ttk.Button(app, text="...", command=select_destination_directory, width=1.5)
select_destination_button.place(x=270, y=79.4)

move_mods_button = ttk.Button(app, text=translations[current_language]["move_button"], command=move_mods_async_handler)
move_mods_button.place(x=90, y=110)

progress_label = create_transparent_label(app, 130, 145, f"0.00%")
current_file_label = create_transparent_label(app, 70, 185, "")

swap_directories_button = ttk.Button(app, text="sw", command=swap_directories, width=3)
swap_directories_button.place(x=270, y=52)

select_gta_v_button["padding"] = (3, -1)
select_destination_button["padding"] = (3, -1)
move_mods_button["padding"] = (20, 5)
polish_button["padding"] = (1, -1)
english_button["padding"] = (1, -1)
swap_directories_button["padding"] = (-1, -1)
select_button["padding"] = (-1, -1)

app.mainloop()
