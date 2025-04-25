import os
import re
from pathlib import Path
from diskovery.utils.run_command import run_command


OUTPUT_DIR = "output_files"  # Folder where disk images are stored
VALID_EXTENSIONS = [".dd", ".E01", ".img"]  # Supported image formats


def analyze_disk_image(disk_image_path):
    print(f"\nAnalyzing Disk Image: {disk_image_path}")

    # Step 1: Run mmls to get partition info
    print("\n--- Partition Table (mmls) ---")
    mmls_output = run_command(f"mmls {disk_image_path}")
    if not mmls_output:
        print("Failed to retrieve partition info with mmls.")
        return None

    print(mmls_output)
    orig_mmls = mmls_output
    # Step 2: Extract the start sector of the first non-meta/non-unallocated partition
    for line in mmls_output.splitlines():
        line = line.strip()
        if not line or "Meta" in line or "Unallocated" in line:
            continue

        parts = re.split(r'\s+', line)
        if len(parts) >= 6:
            slot = parts[0].strip(":")
            start_sector = parts[2]
            description = " ".join(parts[5:])

            print(f"\n📌 Selected Partition: Slot {slot} | Start Sector: {start_sector} | Type: {description}")
            return start_sector , orig_mmls                 # Found the partition to analyze

    print("❌ No valid partition found in mmls output.")
    return None


# Main Execution
if __name__ == "__main__":
    image_files = sorted(
        [file for ext in VALID_EXTENSIONS for file in Path(OUTPUT_DIR).glob(f"*{ext}")],
        key=os.path.getmtime,
        reverse=True
    )
    image_path = str(image_files[0]) if image_files else input("No disk image found in output_files/. Enter image path manually: ").strip()

    if image_path:
        analyze_disk_image(image_path)
    else:
        print("No disk image provided. Exiting.")
