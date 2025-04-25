import os
import subprocess
import shutil

def run_dcfldd():
    print("Welcome to the dcfldd runner script!")
    print("Please provide the required details below.")
    
    dcfldd_path = shutil.which("dcfldd")

    # Ask if the user wants to perform imaging
    imaging_choice = input("Do you want to perform disk imaging? (yes/no): ").strip().lower()

    if imaging_choice == 'yes':
        # Collecting user inputs for imaging
        input_file = input("Enter the input file/device (e.g., /dev/sda or input.img): ").strip()
        while not input_file:
            input_file = input("Input file/device cannot be empty. Please enter again: ").strip()

        # Define the output folder
        output_folder = "./output_files"
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        output_filename = input("Enter the output filename (e.g., output.img): ").strip()
        while not output_filename:
            output_filename = input("Output filename cannot be empty. Please enter again: ").strip()

        output_file = os.path.join(output_folder, output_filename)

        hash_option = input("Enable hashing? (yes/no): ").strip().lower()

        hash_algorithm = None
        if hash_option == 'yes':
            hash_algorithm = input("Enter hash algorithm (e.g., md5, sha1, sha256): ").strip()

        # Constructing the dcfldd command
        command = ["sudo", dcfldd_path, f"if={input_file}", f"of={output_file}"]


        if hash_option == 'yes' and hash_algorithm:
            command.append(f"hash={hash_algorithm}")
            command.append(f"hashlog={output_file}.hash")

        log_file = input("Do you want to save logs? Enter log file name (leave empty for no logs): ").strip()
        if log_file:
            command.append(f"log={log_file}")

        print("\nGenerated dcfldd command:")
        print(" ".join(command))

        # Confirm execution
        confirm = input("\nDo you want to execute this command? (yes/no): ").strip().lower()
        if confirm == 'yes':
            try:
                subprocess.run(command, check=True)
                print("dcfldd command executed successfully.")
                return output_file
            except subprocess.CalledProcessError as e:
                print(f"Error executing dcfldd: {e}")
            except FileNotFoundError:
                print("Error: dcfldd is not installed or not found in the system PATH.")
        else:
            print("Command execution cancelled.")
            return None
    else:
        # Ask for the path of the generated image if not doing imaging
        disk_image_path = input("Enter the path of the previously generated disk image: ").strip()
        if os.path.exists(disk_image_path):
            return disk_image_path
        else:
            print(f"Error: The file {disk_image_path} does not exist.")
            return None
