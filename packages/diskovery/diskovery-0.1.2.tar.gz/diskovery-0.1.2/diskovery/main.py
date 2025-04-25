import os

from diskovery.utils.run_command import run_command
from diskovery.stages.stage1_disk_imaging import run_dcfldd
from diskovery.stages.stage2_extraction import analyze_disk_image
from diskovery.stages.stage3_categorization import categorize_data
from diskovery.stages.stage4_filtering import get_files_by_type
from diskovery.stages.stage4_2_keyword import MasterFunc
from diskovery.stages.stage4_2_keyword import mount_and_extract_files
from diskovery.stages.stage5_reporting import generate_report


def main():
    print("🔍 DISKOVERY: Disk Operation Tool for Data Categorization and Keyword Filtering - CLI Version")

    # Stage 1: Disk Imaging or Use Existing Image
    disk_image = run_dcfldd()
    if not disk_image:
        print("❌ Disk imaging failed or cancelled. Exiting...")
        return

    print(f"\n✅ Using Disk Image: {disk_image}")

    # Stage 2: Partition Analysis (Get start sector)
    print("\n📊 Analyzing disk image to identify partition...")
    start_sector, mmls_output = analyze_disk_image(disk_image)
    if not start_sector:
        print("❌ Disk image analysis failed. Exiting...")
        return

    # Stage 3: Data Categorization
    print("\n📂 Proceeding to data categorization...")
    categorized_output = categorize_data(disk_image, start_sector)
    if not categorized_output:
        print("❌ Categorization failed. Exiting...")
        return

    # Stage 4
    print("\n📂 Proceeding to Filtering...")
    
    # File type filtering
    file_types = input("Enter file types (comma-separated, e.g., .pdf, .png): ").split(", ")
    matching_files = "No Extension Selected"
    if file_types[0] == '':
        print("No File Type Selected")
    else:
        matching_files = get_files_by_type(disk_image, categorized_output['current'], file_types)
        if matching_files:
            print("\nMatching files:")
            for ext in matching_files:
                print(f'.{ext} Files')
                for files in matching_files[ext]:
                    print(files)
                print()
        else:
            print("No files found with the specified extensions.")
        

    # Keyword Filtering from Text Files.
    image_name = os.path.basename(disk_image)
    image_stem = os.path.splitext(image_name)[0]

    keywords = input("Enter Keywords (comma-separated, e.g.: Lorem, Ipsum, dolor): ").split(",")
    kw_res = "No Keyword Selected"
    if keywords[0] == '':
        print("No Keywords Chosen")
    else:
        keywords = [kw.strip().lower() for kw in keywords]
        output_dir = "./output_files/extracted_files"
        output_dir = os.path.join(output_dir, image_stem)
        kw_res = MasterFunc(disk_image, keywords, output_dir, start_sector)
    
    # Stage 4.2: Extracting Images, Videos and Audios.
    ans = input("Do You Want to Exract Media (like images, videos, audios etc.)?: (y/n): ")
    media_file_types = "Not Selected"
    if ans.lower() == 'y':
        output_dir = "./output_files/extracted_files"
        output_dir = os.path.join(output_dir, image_stem)
        media_file_types = input("Enter File Types (comma-separated, e.g.: .png, .mp4, .mp3): ").split(", ")
        if media_file_types == ['']:
            media_file_types = ['.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mp3']
        mount_and_extract_files(disk_image, output_dir, start_sector, media_file_types)

    # Stage 5: Report Generation
    print("\n📝 Generating PDF report...")
    filtered_only = input("Do You want the Filtered Output Only? (type n for no): ")
    if filtered_only.lower() == 'n':
        filtered_only = False
    else:
        filtered_only = True
    
    print(f'filtered only: {filtered_only}')
    generate_report(disk_image, mmls_output, categorized_output, output_dir,
                    filtered_output=matching_files, keyword_hits=kw_res, 
                    media_file_types = media_file_types,
                    filtered_only=filtered_only, include_metadata=True)

if __name__ == "__main__":
    main()