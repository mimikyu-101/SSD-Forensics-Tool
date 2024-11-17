<a id="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/mimikyu-101/SSD-Forensics_Tool">
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

  <h1 align="center">Cross-Platform Live SSD Forensics and TRIM Recovery Tool</h1>

  <p align="center">
    A powerful and user-friendly tool for carving files from raw device data, supporting both Linux and Windows platforms. Designed for digital forensic investigators (DFIs) and data recovery professionals, this tool allows you to recover files based on their magic bytes signatures while optionally displaying hex data for found artifacts.
    <br />
    <a href="https://github.com/mimikyu-101/SSD-Forensics_Tool"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/mimikyu-101/SSD-Forensics_Tool">View Demo</a>
    ·
    <a href="https://github.com/mimikyu-101/SSD-Forensics_Tool/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/mimikyu-101/SSD-Forensics_Tool/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

---


### 🎯 Features

- **Cross-Platform Compatibility**: Works seamlessly on both **Linux** and **Windows**.
- **File Recovery**: Recovers files using pre-defined magic bytes for common file types.
- **Hex Viewer**: Displays hex data for identified files (optional).
- **Customizable Options**: Supports flexible chunk sizes and targeted file recovery based on extensions.
- **Admin Privilege Check**: Ensures proper permissions are in place for device access.

---


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 📂 Supported File Types

The following file types are supported for recovery:

| File Type | Magic Bytes (Hexadecimal)           |
|-----------|-------------------------------------|
| **JPEG**  | `FF D8 FF`                          |
| **PNG**   | `89 50 4E 47`                       |
| **ZIP**   | `50 4B 03 04`                       |
| **PDF**   | `25 50 44 46`                       |
| **GIF**   | `47 49 46 38`                       |
| **MP4**   | `00 00 00 18 66 74 79 70`           |
| **EXE**   | `4D 5A`                             |
| **BMP**   | `42 4D`                             |
| **AVI**   | `52 49 46 46`                       |
| **DOCX**  | `50 4B 03 04` (with XML validation) |
| **XLSX**  | `50 4B 03 04`                       |
| **PPTX**  | `50 4B 03 04`                       |
| **DOC**   | `D0 CF 11 E0 A1 B1 1A E1`           |
| **XLS**   | `D0 CF 11 E0 A1 B1 1A E1`           |
| **PPT**   | `D0 CF 11 E0 A1 B1 1A E1`           |

---


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🛠️ Installation

### Prerequisites
1. **Python 3.7+** is required.
2. Ensure you have proper privileges:
   - **Linux**: Run as `sudo`.
   - **Windows**: Run as an **Administrator**.
3. Install Python dependencies if any (e.g., `argparse`).

### Clone the Repository
```bash
git clone https://github.com/mimikyu-101/SSD-Forensics-Tool.git
cd SSD-Forensics-Tool
```

---


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🚀 Usage

### Command Syntax
```bash
python3 SSD_Recover.py --device <DEVICE_PATH> --output <OUTPUT_DIR> [OPTIONS]
```

### Required Arguments
| Argumnent | Description                                                     |
|-----------|-----------------------------------------------------------------|
| --device  | Path to the target device.                                      |
|           | **Linux:** `/dev/sdX` (e.g., `/dev/sda`).                       |
|           | **Windows:** `\\.\PhysicalDriveX` (e.g., `\\.\PhysicalDrive1`). |
| --output  | Directory to save the recovered files.                          |

### Optional Arguments
| Argumnent    | Description                                                       |
|--------------|-------------------------------------------------------------------|
| --chunk_size | Chunk size for reading data (default: `1MB`).                     |
| --extensions | List of file types/extensions to recover (e.g., `JPEG PNG PDF`).  |
| --show_hex   | Display the hex dump of found files during recovery..             |


### Example
### Linux
Recover All Supported Data Types
```bash
python3 recovery_tool.py --device /dev/sda --output ./recovered_files
```
Recover Specific File Types
```bash
python3 recovery_tool.py --device /dev/sda --output ./recovered_files --extensions JPEG PNG
```
Recover Files with Hex Display
```bash
python3 recovery_tool.py --device /dev/sda --output ./recovered_files --show_hex
```
Custom Chunk Size
```bash
python3 recovery_tool.py --device /dev/sda --output ./recovered_files --chunk_size 524288
```

### Windows
Recover All Supported Data Types
```bash
python3 recovery_tool.py --device \\.\PhysicalDrive0 --output ./recovered_files
```
Recover Specific File Types
```bash
python3 recovery_tool.py --device \\.\PhysicalDrive0 --output ./recovered_files --extensions JPEG PNG
```
Recover Files with Hex Display
```bash
python3 recovery_tool.py --device \\.\PhysicalDrive0 --output ./recovered_files --show_hex
```
---


<p align="right">(<a href="#readme-top">back to top</a>)</p>



## 🛡️ Admin Privileges
### Linux
- Run the script with `sudo` to access the raw device.
```bash
sudo python3 recovery_tool.py --device /dev/sda --output ./recovered_files
```
### Windows
- Right-click on your terminal or IDE and select **Run as Administrator** to avoid access errors.

---


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🧑‍💻 How It Works
- **Privilege Check:** Ensures the tool has the necessary permissions to access the device.
- **Raw Data Reading:** Reads data from the specified device in configurable chunks.
- **Magic Bytes Search:** Scans for predefined signatures to identify files.
- **File Recovery:** Extracts and saves files with proper validation.
- **Hex Viewer _(optional)_:** Displays the first 256 bytes of identified files in hex and ASCII format.

---


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## ⚠️ Disclaimer
This tool is intended for legal and ethical use only. Ensure you have proper authorization to access and analyze the device data. The authors are not responsible for misuse.

---


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Authors

- Abdullah Nadeem [@mimikyu-101](https://www.github.com/mimikyu-101)
- Muhammad Shaayan [@](https://github.com/M-Shaayan)
- Rizwanullah [@](https://github.com/)
- Fatima Farooq [@](https://github.com/)


---


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Project Link: [https://github.com/mimikyu-101/SSD-Forensics_Tool](https://github.com/mimikyu-101/SSD-Forensics_Tool)

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

Happy Recovering! 🚀

