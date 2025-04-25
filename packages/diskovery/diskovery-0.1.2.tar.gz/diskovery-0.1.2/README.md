## 🧪 DISKOVERY: Disk Forensics Tool for Data Categorization & Keyword Filtering

**DISKOVERY** is a Python-based digital forensics tool designed to analyze disk images. It performs a multi-stage forensic analysis including imaging, partition parsing, file categorization, keyword-based filtering, and automatic PDF reporting. The tool supports both complete and filtered analysis outputs and provides investigators with a concise overview of disk contents.  It is a command-line interface (CLI) tool that works well on **Ubuntu** and **Debian-based systems**.

---

### ⚙️ Features
- **Disk Image Support** (`.img`, `.E01`, `.dd`)
- **Partition Parsing** using `mmls`
- **File Categorization**:
  - Deleted
  - Encrypted
  - Current
  - Hidden
- **File Type Filtering** (e.g., `.pdf`, `.docx`)
- **Keyword Search** in extracted text-based files
- **Visual Summary** via pie charts
- **PDF Report Generation** with listings, and visualizations

---

### Steps to use
1. Insert pendrive.
2. To check the location at which it's inserted: sudo fdisk -l
3. Go to script folder and run main.py: sudo python3 main.py

---

### 📁 Project Structure
```
diskovery/
├── diskovery/                       # Main package
│   ├── __init__.py
│   ├── main.py                      # CLI entry point
│   ├── stages/                      # Stage-wise modular pipeline
│   │   ├── __init__.py
│   │   ├── stage1_disk_imaging.py
│   │   ├── stage2_extraction.py
│   │   ├── stage3_categorization.py
│   │   ├── stage4_filtering.py
│   │   ├── stage4_2_keyword.py
│   │   └── stage5_reporting.py
│   └── utils/                       # Utility functions
│       ├── __init__.py
│       └── run_command.py
│
├── README.md                        # Project overview and usage
├── LICENSE                          # MIT License
├── setup.py                         # Packaging configuration
├── requirements.txt                 # Python dependencies
├── MANIFEST.in                      # Include non-code files for PyPI
├── pyproject.toml                   # Build configuration
└── .gitignore                       # Git ignore rules
```

---

### 🚀 Quick Start

#### 1. Clone the Repository
```bash
git clone https://github.com/simmithapad/DISKOVERY.git
cd DISKOVERY
```

#### 2. Run Setup (Installs Tools + Python Packages)
```bash
pip install -r requirements.txt
```

#### 3. Start the Tool
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 main.py
```

---

### 🛠️ Dependencies
#### System Tools (Installed via `setup.sh`)
- `dcfldd`
- `sleuthkit` (for `mmls`, `fls`, `fsstat`)
- `binwalk`
- `grep` and `pdfgrep`

#### Python Packages
- `fpdf`
- `elasticsearch`
- `docx2txt`
- `re`

---

### 📄 Output
- Disk images saved in `./output_files/`
- PDF reports saved in `./output_files/reports/`
- Extracted files saved in `./output_files/extracted_files/`

---

### 📬 Future Work
- [ ] GPU Acceleration
- [ ] Memory Forensics Integration

---

### 👤 Author
Simmi Thapad   
Vrinda Abrol

---

### License
 This project is licensed under the MIT License - see the LICENSE file for details.

 ---

### 🔒 Disclaimer
> [!Important]
> This tool is intended for **educational and lawful forensic analysis** only. Use responsibly.