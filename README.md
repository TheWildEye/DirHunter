# DirHunter

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python_3.x-blue" />
  <img src="https://img.shields.io/badge/Tool-Directory_Brute_Forcer-red" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" />
</p>

---

## 🔥 Overview

**DirHunter (`DirHunter.py`)** is a multithreaded directory brute-forcer built for fast reconnaissance.  
It enumerates hidden directories using a wordlist and highlights actionable HTTP responses:

- `200` (Public)  
- `301/302` (Redirect)  
- `403` (Forbidden)  
- `401` (Unauthorized)  

---

## ✨ Features

- 🚀 High-speed multithreaded scanning  
- 📁 Supports any custom wordlist  
- ⏳ Live ETA display  
- 🎨 Color-coded output  
- 🧵 Automatic thread handling  
- 🎯 Detailed results table  

---

## 📦 Requirements
```bash
pip install requests
```
---

## 📥 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/TheWildEye/DirHunter
cd DirHunter
```
---
### 2. Install dependencies
```bash
pip install requests
```
---
### 3. Verify default wordlist

**Located at:**
```bash
wordlists/common.txt
```
---
### 4. Run the tool
```bash
python DirHunter.py
```
---
## 🖥 Example Output
```
🌐 Enter target: https://target.com

[200] /admin                → https://target.com/admin
[301] /old                  → https://target.com/login
[403] /restricted
[401] /secure

⏱ Scan completed in 11.2 seconds
```
---
