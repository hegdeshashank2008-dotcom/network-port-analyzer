# 🔐 Network Port Scanner (GUI)
## Author: Shashank Hegde
## Institute: Moodlakatte Institute OF Technology, Kundapura, India

A high-performance, multi-threaded TCP Network Port Scanner with a graphical user interface built using Python and Tkinter. This tool is designed to identify open ports on a target system and assist in basic network security analysis.

---

## 📌 Project Description

In modern computer networks, open ports can serve as potential entry points for unauthorized access and cyber attacks. Monitoring these ports is essential for maintaining system security.

This project implements a **Network Port Scanner** that scans a specified range of ports on a target machine and determines which ports are open.

The scanner uses **TCP socket connections** to check port status and provides real-time results through an interactive GUI.

---

## 🎯 Objectives

* To understand network communication using sockets
* To implement port scanning using TCP connections
* To improve performance using multithreading
* To build a user-friendly GUI for cybersecurity tools
* To analyze system vulnerabilities through open ports

---

## ✨ Key Features

* 🖥️ Simple and intuitive GUI (Tkinter-based)
* ⚡ Fast multi-threaded scanning (up to 500 threads)
* 📡 Real-time scanning updates
* 📊 Progress bar with live status tracking
* ⏱️ Elapsed time display
* 🧠 Service detection for common ports
* 🛑 Stop scan functionality
* 💾 Save scan results to a file
* 🌍 Cross-platform support

---

## 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core programming language |
| Socket     | Network communication     |
| Threading  | Parallel execution        |
| Tkinter    | GUI development           |
| Queue      | Thread-safe communication |

---

## ⚙️ Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/network-port-scanner.git
cd network-port-scanner
```

### Step 2: Run Application

```bash
python portscanergui.py
```

---

## ▶️ Usage Guide

1. Enter the **Target IP Address or Hostname**
2. Enter **Start Port** and **End Port**
3. Click **Start Scan**
4. Monitor progress in real-time
5. View detected open ports
6. Save results if required

---

## 🧠 Working Principle

The scanner works using the following steps:

1. Resolves hostname into IP address
2. Iterates through a range of ports
3. Attempts TCP connection using:

   ```
   socket.connect_ex()
   ```
4. If connection is successful → port is OPEN
5. Uses multithreading to scan multiple ports simultaneously
6. Displays results in GUI

---

## 🔄 Multithreading Implementation

* Uses Python's `threading` module
* Creates multiple threads to scan ports concurrently
* Semaphore limits thread usage to avoid system overload
* Improves speed significantly compared to sequential scanning

---

## 📡 Service Detection

The scanner maps common ports to services:

| Port | Service |
| ---- | ------- |
| 21   | FTP     |
| 22   | SSH     |
| 80   | HTTP    |
| 443  | HTTPS   |
| 3306 | MySQL   |
| 3389 | RDP     |

Ports not recognized are labeled as **Unknown**.

---

## 📊 Sample Output

```
[+] Port 80 (HTTP) is open
[+] Port 443 (HTTPS) is open

Scan complete.
Open ports found: 2
```

---

## 📁 Project Structure

```
network-port-scanner/
│── portscanergui.py   # Main application
│── README.md          # Documentation
```

---

## ⚠️ Limitations

* Supports only TCP scanning
* Does not detect vulnerabilities beyond open ports
* Performance depends on network speed
* May be blocked by firewalls

---

## 🚀 Future Enhancements

* UDP port scanning
* OS detection
* Vulnerability scanning integration
* Dark mode UI
* Export results in CSV/JSON

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes only**.
Do not use it on systems without proper authorization.

---

## 📜 License

This project is licensed under the MIT License.
