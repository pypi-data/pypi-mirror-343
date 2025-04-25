import re
import os

def replace_genesis_bots(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Replace the specific line
    modified_content = re.sub(r'GENESIS_POOL', 'GENESIS_DEMO_POOL', content)

    with open(output_file, 'w') as file:
        file.write(modified_content)

def replace_genesis_bots_eai(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Replace the specific line
    modified_content = re.sub(r'GENESIS_EAI', 'GENESIS_DEMO_EAI', content)

    with open(output_file, 'w') as file:
        file.write(modified_content)

def revert_genesis_bots(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Revert the specific line
    modified_content = re.sub(r'GENESIS_DEMO_POOL', 'GENESIS_POOL', content)

    with open(output_file, 'w') as file:
        file.write(modified_content)

def revert_genesis_bots_eai(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Revert the specific line
    modified_content = re.sub(r'GENESIS_DEMO_EAI', 'GENESIS_EAI', content)

    with open(output_file, 'w') as file:
        file.write(modified_content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "revert":
        try:
            print("Reverting changes...")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Revert POOL changes
            files_to_change = ['../genesis_server/deployments/snowflake_app/setup_script.sql',
                             'Genesis.py', 'page_files/config_pool.py',
                             'page_files/start_service.py', 'page_files/start_stop.py']
            for file in files_to_change:
                input_file = os.path.join(script_dir, file)
                output_file = os.path.join(script_dir, file)
                revert_genesis_bots(input_file, output_file)
                print(f"Revert complete. File '{output_file}' restored to GENESIS_POOL.")

            # Revert EAI changes
            files_to_change = ['../../connectors/snowflake_connector/snowflake_connector.py',
                             '../../core/tools/image_tools.py']
            for file in files_to_change:
                input_file = os.path.join(script_dir, file)
                output_file = os.path.join(script_dir, file)
                revert_genesis_bots_eai(input_file, output_file)
                print(f"Revert complete. File '{output_file}' restored to GENESIS_EAI.")
        except Exception as e:
            print(f"Revert failed: {e}")
    else:
        try:
            print("here we go!")
            # Get the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Define input and output file paths relative to the script directory
            files_to_change = ['../genesis_server/deployments/snowflake_app/setup_script.sql','Genesis.py','page_files/config_pool.py','page_files/start_service.py','page_files/start_stop.py']
            for file in files_to_change:
                input_file = os.path.join(script_dir, file)
                output_file = os.path.join(script_dir, file)

                # Usage
                replace_genesis_bots(input_file, output_file)
                print(f"Replacement complete. New file '{output_file}' created with GENESIS_DEMO_POOL.")

            # Define input and output file paths relative to the script directory
            files_to_change = ['../../connectors/snowflake_connector/snowflake_connector.py','../../core/tools/image_tools.py']
            for file in files_to_change:
                input_file = os.path.join(script_dir, file)
                output_file = os.path.join(script_dir, file)

                # Usage
                replace_genesis_bots_eai(input_file, output_file)
                print(f"Replacement complete. New file '{output_file}' created with GENESIS_DEMO_EAI.")
        except Exception as e:
            print(f"failed: {e}")