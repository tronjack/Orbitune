# WARNING: This code has been intentionally made hard to read and modify.
# It is not recommended for production use as it is difficult to debug.

import pygame as pg
import sys
import tkinter as tk
from tkinter import filedialog as fd, messagebox as mb, ttk
import os
import random as r
import io
from PIL import Image as Im, ImageTk as ImTk
import base64

class OPlayer:
    def __init__(self, m):
        self.m = m
        self.m.title(base64.b64decode(b'T3JiaXR1bmUgTWVkaWEgUGxheWVyIFYxLjA=').decode('utf-8'))
        self.m.geometry("700x550")
        self.m.resizable(False, False)

        try:
            ico = self.create_icon()
            if ico:
                self.m.iconphoto(False, ico)
        except Exception as e:
            print(f"Failed to set icon: {e}")

        self.m.tk_setPalette(background='#333333', foreground='#c0c0c0', activeBackground='#555555', activeForeground='white')
        
        s = ttk.Style(m)
        s.theme_create("o_style", parent="clam", settings={
            "TFrame": {"configure": {"background": "#333333"}},
            "TLabel": {"configure": {"background": "#333333", "foreground": "#a0a0a0"}},
            "TButton": {"configure": {"background": "#696969", "foreground": "white", "font": ("Arial", 10, "bold"), "borderwidth": 1, "relief": "raised"},
                        "map": {"background": [("active", "#888888"), ("!disabled", "#696969")], "foreground": [("active", "#c0c0c0")]}},
            "TCombobox": {"configure": {"fieldbackground": "#696969", "foreground": "white", "selectbackground": "#888888", "selectforeground": "white", "background": "#696969", "arrowcolor": "white"}},
        })
        s.theme_use("o_style")

        try:
            pg.mixer.init(44100, -16, 2, 2048)
        except pg.error as e:
            mb.showerror("Error", f"Could not initialize mixer: {e}")
            sys.exit()

        self.ip = False
        self.ipa = False
        self.pl = []
        self.ci = -1
        self.vl = tk.DoubleVar(value=50)
        self.vt = tk.StringVar(value="Static Bars")
        self.vo = []
        self.ps1 = []
        self.bd = []
        self.c = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]

        self.mf = ttk.Frame(m, padding="10")
        self.mf.pack(fill=tk.BOTH, expand=True)
        self.tf = ttk.Frame(self.mf)
        self.tf.pack(pady=(0, 10))
        self.vcf = ttk.Frame(self.mf)
        self.vcf.pack(pady=5)
        self.vf = ttk.Frame(self.mf)
        self.vf.pack(pady=10)
        self.plf = ttk.Frame(self.mf)
        self.plf.pack(fill=tk.BOTH, expand=True)
        self.cc = ttk.Frame(self.mf, padding=10)
        self.cc.pack(pady=10)

        self.cw()

    def create_icon(self):
        try:
            img = Im.open("Screenshot 2025-08-01 221921.png")
            img = img.resize((64, 64), Im.LANCZOS)
            ico = ImTk.PhotoImage(img)
            return ico
        except FileNotFoundError:
            print("Icon file not found. Using default icon.")
            return None
        except ImportError:
            print("Pillow library not installed. Using default icon.")
            return None

    def cw(self):
        self.tl = ttk.Label(self.tf, text="No file loaded", font=("Helvetica", 14, "bold"), foreground="#00FFFF")
        self.tl.pack()
        
        ttk.Label(self.vcf, text="Visualizer:").pack(side=tk.LEFT, padx=5)
        vo = [base64.b64decode(b'U3RhdGljIEJhcnM=').decode('utf-8'),
              base64.b64decode(b'UFMxIFN0eWxl').decode('utf-8'),
              base64.b64decode(b'V2F2ZWZvcm0=').decode('utf-8'),
              base64.b64decode(b'Qm91bmNpbmcgRG90cw==').decode('utf-8')]
        self.vc = ttk.Combobox(self.vcf, textvariable=self.vt, values=vo, state="readonly")
        self.vc.pack(side=tk.LEFT, padx=5)
        self.vc.bind("<<ComboboxSelected>>", self.ovc)

        self.vc_canvas = tk.Canvas(self.vf, width=650, height=100, bg="#1a1a1a", highlightthickness=0)
        self.vc_canvas.pack(pady=5)
        
        self.pl_label = ttk.Label(self.plf, text="Playlist", font=("Arial", 12))
        self.pl_label.pack(anchor="w")

        self.pl_lb = tk.Listbox(self.plf, bg="#1a1a1a", fg="#00FF00", selectbackground="#404040", selectforeground="white", borderwidth=0, highlightthickness=0, height=10, font=("Arial", 11))
        self.pl_lb.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        v_frame = ttk.Frame(self.cc)
        v_frame.pack()
        self.v_label = ttk.Label(v_frame, text=f"Volume: {int(self.vl.get())}%")
        self.v_label.pack(side=tk.LEFT, padx=5)
        
        self.v_slider = ttk.Scale(v_frame, from_=0, to=100, orient="horizontal", command=self.sv, variable=self.vl)
        self.v_slider.pack(side=tk.LEFT, padx=5)
        
        b_frame = ttk.Frame(self.cc)
        b_frame.pack()
        
        self.add_b = ttk.Button(b_frame, text="Add to Playlist", command=self.atp)
        self.add_b.grid(row=0, column=0, padx=5, pady=5)

        self.prev_b = ttk.Button(b_frame, text="<< Prev", command=self.pp)
        self.prev_b.grid(row=0, column=1, padx=5, pady=5)
        
        self.play_b = ttk.Button(b_frame, text="▶ Play", command=self.pm)
        self.play_b.grid(row=0, column=2, padx=5, pady=5)

        self.pause_b = ttk.Button(b_frame, text="❚❚ Pause", command=self.paum)
        self.pause_b.grid(row=0, column=3, padx=5, pady=5)
        
        self.stop_b = ttk.Button(b_frame, text="■ Stop", command=self.sm)
        self.stop_b.grid(row=0, column=4, padx=5, pady=5)

        self.next_b = ttk.Button(b_frame, text="Next >>", command=self.pn)
        self.next_b.grid(row=0, column=5, padx=5, pady=5)
        
        self.about_b = ttk.Button(b_frame, text="About", command=self.sa)
        self.about_b.grid(row=0, column=6, padx=5, pady=5)

        self.pl_lb.bind("<Double-Button-1>", self.pfl)
        
        self.m.after(100, self.cfs)
        self.m.after(100, self.uv)

    def ovc(self, event):
        self.vc_canvas.delete("all")
        self.vo = []
        self.ps1 = []
        self.bd = []
        
        vt = self.vc.get()
        if vt == "Static Bars":
            self.cvb()
        elif vt == "PS1 Style":
            self.cps1()
        elif vt == "Bouncing Dots":
            self.cbd()
            
        self.vt.set(vt)
        if not self.ip:
            self.rv()

    def sv(self, value):
        v = float(value) / 100
        pg.mixer.music.set_volume(v)
        self.v_label.config(text=f"Volume: {int(float(value))}%")

    def cvb(self):
        bc = 64
        bw = self.vc_canvas.winfo_width() / bc
        for i in range(bc):
            x1 = i * bw + 1
            y1 = 90
            x2 = (i + 1) * bw
            y2 = 100
            bar = self.vc_canvas.create_rectangle(x1, y1, x2, y2, fill="#00FF00", outline="#003300")
            self.vo.append(bar)

    def cps1(self):
        gs = 10
        w = self.vc_canvas.winfo_width()
        h = self.vc_canvas.winfo_height()
        
        for x in range(gs):
            for y in range(gs):
                cx = (x + 0.5) * (w / gs)
                cy = (y + 0.5) * (h / gs)
                size = 5
                
                sq = self.vc_canvas.create_rectangle(cx - size, cy - size, cx + size, cy + size, fill="#00FFFF", outline="")
                self.ps1.append(sq)

    def cbd(self):
        w = self.vc_canvas.winfo_width()
        h = self.vc_canvas.winfo_height()
        dc = 50
        
        for _ in range(dc):
            x = r.randint(10, w - 10)
            y = r.randint(10, h - 10)
            size = r.randint(2, 5)
            color = r.choice(self.c)
            vx = r.uniform(-2, 2)
            vy = r.uniform(-2, 2)
            dot = self.vc_canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="")
            self.bd.append({'id': dot, 'vx': vx, 'vy': vy, 'size': size})

    def rv(self):
        self.vc_canvas.delete("all")
        self.vo = []
        self.ps1 = []
        self.bd = []

        if self.vt.get() == "Static Bars":
            self.cvb()
            for bar in self.vo:
                self.vc_canvas.coords(bar, self.vc_canvas.coords(bar)[0], 90, self.vc_canvas.coords(bar)[2], 100)
        elif self.vt.get() == "Waveform":
            self.vc_canvas.create_line(0, 50, self.vc_canvas.winfo_width(), 50, fill="#00FFFF", width=2)
        elif self.vt.get() == "PS1 Style":
            self.cps1()
            for sq in self.ps1:
                self.vc_canvas.itemconfig(sq, fill="#00FFFF")
        elif self.vt.get() == "Bouncing Dots":
            self.cbd()
            for dot in self.bd:
                self.vc_canvas.itemconfig(dot['id'], fill=r.choice(self.c))
                dot['vx'] = 0
                dot['vy'] = 0

    def uv(self):
        if self.ip:
            vt = self.vt.get()
            
            if vt == "Static Bars":
                if not self.vo:
                    self.cvb()
                for bar in self.vo:
                    h = r.randint(10, 100)
                    self.vc_canvas.coords(bar, self.vc_canvas.coords(bar)[0], 100 - h, self.vc_canvas.coords(bar)[2], 100)
            
            elif vt == "PS1 Style":
                if not self.ps1:
                    self.cps1()
                for sq in self.ps1:
                    size = r.randint(1, 15)
                    fc = r.choice(self.c)
                    coords = self.vc_canvas.coords(sq)
                    if coords:
                        cx = (coords[0] + coords[2]) / 2
                        cy = (coords[1] + coords[3]) / 2
                        self.vc_canvas.coords(sq, cx - size, cy - size, cx + size, cy + size)
                        self.vc_canvas.itemconfig(sq, fill=fc)

            elif vt == "Waveform":
                self.vc_canvas.delete("all")
                w = self.vc_canvas.winfo_width()
                h = self.vc_canvas.winfo_height()
                points = []
                np = 100
                amp = r.randint(1, 50)
                
                for i in range(np):
                    x = i * (w / np)
                    y = h / 2 + r.uniform(-amp, amp)
                    points.append((x, y))
                
                if len(points) > 1:
                    self.vc_canvas.create_line(points, fill="#00FFFF", smooth=True, width=2)
            
            elif vt == "Bouncing Dots":
                if not self.bd:
                    self.cbd()
                
                w = self.vc_canvas.winfo_width()
                h = self.vc_canvas.winfo_height()
                
                for dot_info in self.bd:
                    coords = self.vc_canvas.coords(dot_info['id'])
                    if not coords: continue
                    x1, y1, x2, y2 = coords
                    
                    x1 += dot_info['vx']
                    y1 += dot_info['vy']
                    x2 += dot_info['vx']
                    y2 += dot_info['vy']
                    
                    if x1 <= 0 or x2 >= w:
                        dot_info['vx'] *= -1
                    if y1 <= 0 or y2 >= h:
                        dot_info['vy'] *= -1
                    
                    self.vc_canvas.coords(dot_info['id'], x1, y1, x2, y2)
                    size = r.randint(2, 8)
                    self.vc_canvas.coords(dot_info['id'], x1, y1, x1 + size, y1 + size)
                    self.vc_canvas.itemconfig(dot_info['id'], fill=r.choice(self.c))
        else:
            self.rv()
        
        self.m.after(50, self.uv)

    def oc(self):
        self.sm()
        pg.mixer.quit()
        self.m.destroy()

    def atp(self):
        fps = fd.askopenfilenames(
            defaultextension=".mp3",
            filetypes=[(base64.b64decode(b'QXVkaW8gRmlsZXM=').decode('utf-8'), "*.mp3 *.wav *.ogg")]
        )
        if fps:
            for fp in fps:
                self.pl.append(fp)
                fn = os.path.basename(fp)
                self.pl_lb.insert(tk.END, fn)
            print(f"Added {len(fps)} files to the playlist.")
            if self.ci == -1:
                self.ci = 0
                self.pl_lb.select_set(0)

    def pm(self):
        if not self.pl:
            mb.showinfo("Info", "The playlist is empty. Please add a file.")
            return

        if self.ipa:
            pg.mixer.music.unpause()
            self.ipa = False
            self.ip = True
            print("Resuming playback.")
            return

        try:
            ci_tuple = self.pl_lb.curselection()
            if not ci_tuple:
                if self.ci == -1:
                    self.ci = 0
                self.pl_lb.select_set(self.ci)
                ci_tuple = (self.ci,)
            else:
                self.ci = ci_tuple[0]

            fp = self.pl[self.ci]
            pg.mixer.music.load(fp)
            pg.mixer.music.play()
            self.ip = True
            self.ipa = False
            self.tl.config(text=f"Now Playing: {os.path.basename(fp)}")
            self.sv(self.vl.get())
            print(f"Starting playback of: {fp}")
        except pg.error as e:
            mb.showerror("Error", f"Could not play the file: {e}")

    def pfl(self, event):
        self.sm()
        self.pm()

    def paum(self):
        if self.ip:
            pg.mixer.music.pause()
            self.ip = False
            self.ipa = True
            print("Playback paused.")
        else:
            print("Nothing is playing to pause.")

    def sm(self):
        if self.ip or self.ipa:
            pg.mixer.music.stop()
            self.ip = False
            self.ipa = False
            self.tl.config(text="Stopped")
            print("Playback stopped.")
            self.rv()

    def pn(self):
        if not self.pl:
            return
        
        self.ci = (self.ci + 1) % len(self.pl)
        self.pl_lb.selection_clear(0, tk.END)
        self.pl_lb.select_set(self.ci)
        self.pm()

    def pp(self):
        if not self.pl:
            return
        
        self.ci = (self.ci - 1 + len(self.pl)) % len(self.pl)
        self.pl_lb.selection_clear(0, tk.END)
        self.pl_lb.select_set(self.ci)
        self.pm()

    def cfs(self):
        if self.ip and not pg.mixer.music.get_busy():
            print("Song ended, playing next.")
            self.pn()
        
        self.m.after(100, self.cfs)
    
    def sa(self):
        at = (base64.b64decode(b'T3JiaXR1bmUgdjEuMCBieSBKb3JkYW4gT2FtZWxkYQ==').decode('utf-8') +
              "\n\n" +
              base64.b64decode(b'VGhpcyB2ZXJzaW9uIGZlYXR1cmVzIGEgbXVzaWMgdmlzdWFsaXplciwgYSB2b2x1bWUgc2xpZGVyLCBhIHBsYXlsaXN0LCBhbmQgYSBjdXN0b20gZGFyayB0aGVtZS4=').decode('utf-8') +
              "\n" +
              base64.b64decode(b'SXRzIG5hbWUgaXMgZW5zcGlyZWQgYnkgdGhlIGhhcm1vbmlvdXMgYW5kIGN5Y2xpY2FsIG5hdHVyZSBvZiBvcmJpdHMs').decode('utf-8') +
              "\n" +
              base64.b64decode(b'bWlycm9yaW5nIHRoZSB3YXkgbXVzaWMgY2FuIGxvb3AgYW5kIGZpbGwgeW91ciBzcGFjZSB3aXRoIGEgc3RlYWR5IHJoeXRobS4=').decode('utf-8') +
              "\n" +
              base64.b64decode(b'RW5qb3kgdGhlIHNpbXBsZSwgZWxlZ2FudCBzb3VuZHNjYXBlIGl0IHByb3ZpZGVzLg==').decode('utf-8'))
        mb.showinfo(base64.b64decode(b'QWJvdXQgT3JiaXR1bmU=').decode('utf-8'), at)

def main():
    root = tk.Tk()
    app = OPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.oc)
    root.mainloop()

if __name__ == "__main__":
    main()
