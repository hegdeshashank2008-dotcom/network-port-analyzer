#Author: Shashank Hegde
# #Institute: Moodlakatte INstitute of Technology, Kundapura
import socket
import threading
import time
import queue
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
    3306: 'MySQL', 3389: 'RDP', 5900: 'VNC', 8080: 'HTTP-Alt'
}


class PortScanner:
    def __init__(self, target, start_port, end_port, timeout=0.5, max_threads=500):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.max_threads = max_threads

        self.total_ports = end_port - start_port + 1
        self.scanned_count = 0
        self.open_ports = []
        self.closed_count = 0

        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self.result_queue = queue.Queue()

    def stop(self):
        self._stop_event.set()

    def resolve_target(self):
        return socket.gethostbyname(self.target)

    def _scan_port(self, port):
        if self._stop_event.is_set():
            return

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)

            result = s.connect_ex((self.target, port))

            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                with self._lock:
                    self.open_ports.append((port, service))
                self.result_queue.put(("open", port, service))
            else:
                with self._lock:
                    self.closed_count += 1

            s.close()

        except Exception as e:
            self.result_queue.put(("error", port, str(e)))

        finally:
            with self._lock:
                self.scanned_count += 1
            self.result_queue.put(("progress", self.scanned_count, self.total_ports))

    def run(self):
        sem = threading.Semaphore(self.max_threads)
        threads = []

        for port in range(self.start_port, self.end_port + 1):
            if self._stop_event.is_set():
                break

            sem.acquire()
            t = threading.Thread(target=self._worker, args=(sem, port), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.result_queue.put(("done", None, None))

    def _worker(self, sem, port):
        try:
            self._scan_port(port)
        finally:
            sem.release()



class ScannerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Network Port Scanner")
        self.geometry("720x520")

        self.scanner = None
        self.thread = None
        self.start_time = None

        self._build_ui()

    def _build_ui(self):
        frame = ttk.LabelFrame(self, text="Scan Settings")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Target:").grid(row=0, column=0)
        self.target_entry = ttk.Entry(frame, width=30)
        self.target_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Start Port:").grid(row=0, column=2)
        self.start_entry = ttk.Entry(frame, width=10)
        self.start_entry.insert(0, "1")
        self.start_entry.grid(row=0, column=3)

        ttk.Label(frame, text="End Port:").grid(row=0, column=4)
        self.end_entry = ttk.Entry(frame, width=10)
        self.end_entry.insert(0, "1024")
        self.end_entry.grid(row=0, column=5)

        self.start_btn = ttk.Button(frame, text="Start", command=self.start_scan)
        self.start_btn.grid(row=1, column=4)

        self.stop_btn = ttk.Button(frame, text="Stop", command=self.stop_scan, state="disabled")
        self.stop_btn.grid(row=1, column=5)

        # Status
        self.status = tk.StringVar(value="Idle")
        ttk.Label(self, textvariable=self.status).pack()

        self.progress = ttk.Progressbar(self)
        self.progress.pack(fill="x", padx=10)

        # Output
        self.output = tk.Text(self, height=18)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left")
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side="right")

    def log(self, text):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def start_scan(self):
        target = self.target_entry.get().strip()

        if not target:
            messagebox.showerror("Error", "Enter target")
            return

        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
        except:
            messagebox.showerror("Error", "Invalid ports")
            return

        self.scanner = PortScanner(target, start, end)

        try:
            ip = self.scanner.resolve_target()
        except:
            messagebox.showerror("Error", "Invalid target")
            return

        self.output.delete("1.0", tk.END)

        self.log("="*50 + "\n")
        self.log(" NETWORK PORT SCANNER\n")
        self.log("="*50 + "\n")
        self.log(f"Target: {target} ({ip})\n")
        self.log(f"Ports: {start}-{end}\n")
        self.log(f"Started: {datetime.now()}\n\n")

        self.start_time = time.time()

        self.thread = threading.Thread(target=self.scanner.run, daemon=True)
        self.thread.start()

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        self.after(50, self.update_ui)

    def stop_scan(self):
        if self.scanner:
            self.scanner.stop()

    def update_ui(self):
        try:
            while True:
                msg, a, b = self.scanner.result_queue.get_nowait()

                if msg == "open":
                    self.log(f"[+] Port {a} ({b}) is OPEN\n")

                elif msg == "progress":
                    self.progress.config(maximum=b, value=a)
                    self.status.set(f"Scanning {a}/{b}")

                elif msg == "done":
                    self.finish_scan()

        except queue.Empty:
            pass

        if self.thread.is_alive():
            self.after(50, self.update_ui)

    def finish_scan(self):
        total_open = len(self.scanner.open_ports)
        total_closed = self.scanner.closed_count

        self.log("\n" + "="*50 + "\n")
        self.log("SCAN COMPLETE\n")
        self.log("="*50 + "\n")
        self.log(f"Total Ports: {self.scanner.total_ports}\n")
        self.log(f"Open Ports: {total_open}\n")
        self.log(f"Closed Ports: {total_closed}\n")
        self.log("="*50 + "\n")

        self.status.set("Completed")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def clear(self):
        self.output.delete("1.0", tk.END)
        self.status.set("Idle")

    def save(self):
        if not self.scanner:
            return

        file = filedialog.asksaveasfilename(defaultextension=".txt")

        if not file:
            return

        with open(file, "w") as f:
            f.write("PORT SCAN REPORT\n")
            f.write("="*50 + "\n")

            for port, service in self.scanner.open_ports:
                f.write(f"{port} ({service}) OPEN\n")

            f.write("\nSUMMARY\n")
            f.write(f"Open: {len(self.scanner.open_ports)}\n")
            f.write(f"Closed: {self.scanner.closed_count}\n")

        messagebox.showinfo("Saved", "Report saved successfully")



if __name__ == "__main__":
    app = ScannerGUI()
    app.mainloop()