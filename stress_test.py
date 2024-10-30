import subprocess
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(filename='ans.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the Gemini API
genai.configure(api_key="AIzaSyD8PpACndf1IzZSUuzVBQlyYrcEWIRJKy4")

def get_gemini_suggestions(test_output):
    """Get suggestions from the Gemini API based on the test output."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Log output: {test_output}")

    # Check for a valid response
    if response and hasattr(response, 'text'):
        return response.text  # Return the generated content
    else:
        print("Error retrieving suggestions.")
        return None

def memory_stress():
    """Perform a memory stress test."""
    logging.info("Starting memory stress test")
    try:
        result = subprocess.run("stress-ng --vm 1 --vm-bytes 80% -t 30s", shell=True, check=True, capture_output=True, text=True)
        logging.info("Memory stress test completed")

        # Log the output of the stress test
        logging.info(f"Memory stress test output: {result.stdout}")
        print(f"Memory stress test output: {result.stdout}")  # Print output to console

        # Get suggestions from Gemini
        suggestions = get_gemini_suggestions(result.stdout)
        if suggestions:
            logging.info(f"Suggestions from Gemini: {suggestions}")
            print(f"Suggestions from Gemini: {suggestions}")  # Print suggestions to console
        else:
            logging.warning("Could not retrieve suggestions from Gemini.")
            print("Could not retrieve suggestions from Gemini.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Memory stress test failed: {e}")
        print(f"Memory stress test failed: {e}")

def disk_stress():
    """Perform a disk stress test."""
    logging.info("Starting disk stress test")
    try:
        result = subprocess.run("stress-ng --hdd 1 --hdd-bytes 80% -t 30s", shell=True, check=True, capture_output=True, text=True)
        logging.info("Disk stress test completed")
        logging.info(f"Disk stress test output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Disk stress test failed: {e}")

def network_stress():
    """Perform a network stress test."""
    logging.info("Starting network stress test")
    try:
        subprocess.run("iperf3 -c 127.0.0.1 -t 30", shell=True, check=True)
        logging.info("Network stress test completed")
    except subprocess.CalledProcessError as e:
        logging.error(f"Network stress test failed: {e}")

def cpu_stress():
    """Perform a CPU stress test."""
    logging.info("Starting CPU stress test")
    try:
        result = subprocess.run("stress-ng --cpu 4 --cpu-load 80 -t 30s", shell=True, check=True, capture_output=True, text=True)
        logging.info("CPU stress test completed")
        logging.info(f"CPU stress test output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"CPU stress test failed: {e}")

def mysql_stress():
    """Perform a MySQL stress test."""
    logging.info("Starting MySQL stress test")
    try:
        result = subprocess.run(
            "sysbench --mysql-host=192.168.1.10 --mysql-user=exporter "
            "--mysql-password=Nikhil@25 --db-driver=mysql oltp_read_write "
            "--tables=10 --table-size=1000 --threads=4 --time=60 run",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logging.info("MySQL stress test completed")
        logging.info(f"MySQL stress test output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"MySQL stress test failed: {e}")

# Main menu function
def main_menu():
    """Display the main menu for stress tests."""
    while True:
        print("\nStress Testing Menu:")
        print("1. Memory Stress Testing")
        print("2. Disk Stress Testing")
        print("3. Network Stress Testing")
        print("4. CPU Stress Testing")
        print("5. MySQL Stress Testing")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            memory_stress()
        elif choice == '2':
            disk_stress()
        elif choice == '3':
            network_stress()
        elif choice == '4':
            cpu_stress()
        elif choice == '5':
            mysql_stress()
        elif choice == '6':
            logging.info("Exiting stress test script")
            print("Exiting...")
            break
        else:
            logging.warning("Invalid choice selected")
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main_menu()