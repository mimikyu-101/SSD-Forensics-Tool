import os
import sys
import argparse
import platform
import ctypes
import time
import subprocess


def print_colored(text, color="white"):
    """
    Print text in the specified color (if terminal supports it).
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[97m",
    }
    reset = "\033[0m"
    print(f"{colors.get(color, colors['white'])}{text}{reset}")


def check_admin():
    """
    Check if the script is running with administrator privileges.
    """
    if platform.system() == "Linux":
        if os.geteuid() != 0:
            print_colored("This application requires admin privileges. Please run with sudo.", color="red")
            sys.exit(1)
    elif platform.system() == "Windows":
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print_colored("This application requires admin privileges. Please run as Administrator.", color="red")
                sys.exit(1)
        except Exception as e:
            print_colored(f"Error checking admin privileges: {e}", color="red")
            sys.exit(1)


def check_trim_status(device_path):
    if platform.system() == "Linux":
        try:
            result = subprocess.run(["hdparm", "-I", device_path], capture_output=True, text=True)
            if "Data Set Management TRIM supported" in result.stdout:
                return "TRIM is supported by the SSD."
            else:
                return "TRIM is not supported by the SSD."
        except Exception as e:
            return f"Error checking TRIM status: {e}"

    elif platform.system() == "Windows":
        try:
            result = subprocess.run(["fsutil", "behavior", "query", "DisableDeleteNotify"], capture_output=True, text=True)
            if "0" in result.stdout:
                return "TRIM is enabled on this system."
            elif "1" in result.stdout:
                return "TRIM is disabled on this system."
            else:
                return "Unable to determine TRIM status."
        except Exception as e:
            return f"Error checking TRIM status: {e}"
    else:
        return "TRIM check is not supported on this platform."
    

def get_ssd_details(device_path):
    if platform.system() == "Linux":
        try:
            result = subprocess.run(["hdparm", "-I", device_path], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            ssd_info = [line.strip() for line in lines if any(keyword in line for keyword in ["Model Number", "Firmware Revision"])]
            if ssd_info:
                return f"SSD detected:\n" + "\n".join(ssd_info) + "\nWarning: Garbage collection may be active."
            else:
                return "No SSD detected, or information is unavailable."
        except Exception as e:
            return f"Error fetching SSD details: {e}"

    elif platform.system() == "Windows":
        try:
            result = subprocess.run(["wmic", "diskdrive", "get", "model,firmwareRevision,mediaType"], capture_output=True, text=True)
            if "SSD" in result.stdout:
                return f"SSD detected:\n{result.stdout.strip()}\nWarning: Garbage collection may be active."
            else:
                return "No SSD detected, or information is unavailable."
        except Exception as e:
            return f"Error fetching SSD details: {e}"
    else:
        return "Garbage collection analysis is not supported on this platform."
    

def assess_recovery_feasibility(device_path):
    """
    Assess the feasibility of data recovery based on SSD features.
    :param device_path: Path to the device (Linux: /dev/sda, Windows: \\.\PhysicalDriveX)
    :return: Feasibility score (1-10) and recommendation
    """
    trim_status = check_trim_status(device_path)
    gc_details = get_ssd_details(device_path)
    
    score = 10  # Start with high recovery feasibility

    if "TRIM is enabled" in trim_status:
        score -= 5  # Major impact if TRIM is enabled

    if "Garbage collection may be active" in gc_details:
        score -= 3  # Moderate impact for GC

    recommendation = "Data recovery is feasible." if score > 5 else "Data recovery may have limited success."
    return score, recommendation


def read_raw_data(device_path, chunk_size=1024*1024):
    """
    Read raw data from the device in chunks.
    :param device_path: Path to the device (Linux: /dev/sda, Windows: \\.\PhysicalDriveX)
    :param chunk_size: Size of each data chunk (default: 1MB)
    :return: Generator yielding chunks of data
    """
    if platform.system() == "Windows":
        return read_raw_data_windows(device_path, chunk_size)
    elif platform.system() == "Linux":
        return read_raw_data_linux(device_path, chunk_size)


def read_raw_data_linux(device_path, chunk_size=1024*1024):
    """
    Read raw data from a Linux device in chunks.
    """
    with open(device_path, 'rb') as device:
        while chunk := device.read(chunk_size):
            yield chunk


def read_raw_data_windows(device_path, chunk_size=1024*1024):
    """
    Read raw data from a Windows device in chunks.
    """
    try:
        with open(device_path, 'rb') as device:
            while chunk := device.read(chunk_size):
                yield chunk
    except Exception as e:
        print_colored(f"Error reading device: {e}", color="red")
        sys.exit(1)


def carve_files(device_path, output_dir, chunk_size=1024*1024, file_types=None, show_hex=False):
    """
    Carve files from raw device data based on magic bytes.
    """
    os.makedirs(output_dir, exist_ok=True)
    offset = 0

    # Filter MAGIC_BYTES if specific file types are provided
    selected_magic_bytes = {
        key: value for key, value in MAGIC_BYTES.items() if file_types is None or key in file_types
    }

    # Read raw data from the device
    for chunk in read_raw_data(device_path, chunk_size):
        for file_type, magic in selected_magic_bytes.items():
            pos = chunk.find(magic)
            if pos != -1:
                # File found, save it
                file_offset = offset + pos
                save_file(device_path, file_offset, file_type, output_dir, show_hex)
                print_colored(f"Recovered {file_type} at offset {file_offset}\n", color="green")
        offset += chunk_size


def save_file(device_path, start_offset, file_type, output_dir, show_hex=False, read_size=1024*1024):
    """
    Save the carved file data to a file.
    """
    output_file = os.path.join(output_dir, f"{file_type}_{start_offset}.recovered")
    is_valid_file = True

    with open(device_path, 'rb') as device:
        device.seek(start_offset)
        data_chunk = device.read(read_size)

        if show_hex:
            print("Displaying Hex:")
            hex_data = data_chunk[:256]  # Limit hex display to the first 256 bytes
            for i in range(0, len(hex_data), 16):
                chunk = hex_data[i:i+16]
                hex_str = ' '.join(f'{b:02X}' for b in chunk)
                ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                print(f"{start_offset + i:08X}: {hex_str:<47} {ascii_str}")
            
            # Pause before proceeding to the next file
            input("Press Enter to continue to the next file...")

        # Write the file
        if is_valid_file:
            with open(output_file, 'wb') as out_file:
                out_file.write(data_chunk)
            print_colored(f"Saved {file_type} to {output_file}", color="green")


if __name__ == "__main__":
    print("""
 __   __   __      ___  __   __   ___       __     __   __                __     ___  __              __   ___  __   __        ___  __         ___  __   __       
/__` /__` |  \    |__  /  \ |__) |__  |\ | /__` | /  ` /__`     /\  |\ | |  \     |  |__) |  |\/|    |__) |__  /  ` /  \ \  / |__  |__) \ /     |  /  \ /  \ |    
.__/ .__/ |__/    |    \__/ |  \ |___ | \| .__/ | \__, .__/    /~~\ | \| |__/     |  |  \ |  |  |    |  \ |___ \__, \__/  \/  |___ |  \  |      |  \__/ \__/ |___ 
          """)

    # Check admin privileges
    check_admin()

    # Define magic bytes for common file types
    MAGIC_BYTES = {
        "JPEG": b'\xFF\xD8\xFF',                # JPEG image
        "PNG": b'\x89\x50\x4E\x47',             # PNG image
        "ZIP": b'\x50\x4B\x03\x04',             # ZIP file
        "PDF": b'\x25\x50\x44\x46',             # PDF document
        "GIF": b'\x47\x49\x46\x38',             # GIF image
        "MP4": b'\x00\x00\x00\x18\x66\x74\x79\x70', # MP4 video
        "EXE": b'\x4D\x5A',                     # Windows executable
        "BMP": b'\x42\x4D',                     # BMP image
        "AVI": b'\x52\x49\x46\x46',             # AVI video
        "DOCX": b'\x50\x4B\x03\x04',            # DOCX document (2007+)
        "XLSX": b'\x50\x4B\x03\x04',                 # Excel spreadsheet (2007+)
        "PPTX": b'\x50\x4B\x03\x04',                 # PowerPoint presentation (2007+)
        "DOC": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',  # Word document (pre-2007)
        "XLS": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',  # Excel spreadsheet (pre-2007)
        "PPT": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',  # PowerPoint presentation (pre-2007)
    }

    # Dynamically generate the list of supported extensions
    supported_extensions = ', '.join(MAGIC_BYTES.keys())

    # Command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Cross-Platform Live Data Recovery Tool",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--device", required=True, help="Path to the device (Linux: /dev/sdX, Windows: \\\\.\\PhysicalDriveX)")
    parser.add_argument("--output", required=True, help="Directory to save recovered files")
    parser.add_argument("--chunk_size", type=int, default=1024*1024, help="Chunk size in bytes (default: 1MB)")
    parser.add_argument("--extensions", nargs='+', help=("List of file extensions to recover.\n"f"Supported types:\n{supported_extensions}"))
    parser.add_argument("--show_hex", action="store_true", help="Display hex data of found artifacts")

    args = parser.parse_args()

    # Check SSD features
    print_colored("\nChecking SSD Features...\n", color="yellow")
    print_colored(check_trim_status(args.device), color="yellow")
    print_colored(get_ssd_details(args.device), color="yellow")

    print_colored("\nWARNING: Recovery on SSDs with TRIM or aggressive Garbage Collection may have limited success.", color="red")

    # Analyze recovery feasibility
    print_colored("\nAnalyzing recovery feasibilty...", color="yellow")
    score, recommendation = assess_recovery_feasibility(args.device)
    print_colored(f"Feasibility Score: {score}/10", color="yellow")
    print_colored(f"Recommendation: {recommendation}\n\n", color="yellow")

    time.sleep(5)

    # Run the carving process
    carve_files(args.device, args.output, args.chunk_size, args.extensions, args.show_hex)

