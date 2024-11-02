import subprocess
import logging
from twilio.rest import Client
import google.generativeai as genai

# Twilio Configuration
account_sid = ['YourAccount_sid']
auth_token = ['YourToken']  # Replace with your actual auth token
client = Client(account_sid, auth_token)

# Configure logging
logging.basicConfig(filename='ans.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the Gemini API
genai.configure(api_key=["your token"])  # Replace with your Gemini API key

def send_whatsapp_notification(message_text):
    """Send a WhatsApp notification, splitting it if it's too long."""
    max_length = 1600  # Twilio's character limit for WhatsApp messages
    messages = [message_text[i:i + max_length] for i in range(0, len(message_text), max_length)]

    for part in messages:
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio's WhatsApp number
            to='whatsapp:+91*******',    # Replace with your WhatsApp number
            body=part
        )
        print(f"Message sent with SID: {message.sid}")

def get_gemini_suggestions(test_output):
    """Get suggestions from the Gemini API based on the test output."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Log output: {test_output}")

    if response and hasattr(response, 'text'):
        suggestions = response.text
        send_whatsapp_notification(f"Gemini AI Suggestions: {suggestions}")
        return suggestions
    else:
        print("Error retrieving suggestions.")
        return None

def memory_stress():
    """Perform a memory stress test."""
    logging.info("Starting memory stress test")
    try:
        result = subprocess.run("stress-ng --vm 1 --vm-bytes 80% -t 30s", shell=True, check=True, capture_output=True, text=True)
        logging.info("Memory stress test completed")
        logging.info(f"Memory stress test output: {result.stdout}")

        # Get suggestions from Gemini
        suggestions = get_gemini_suggestions(result.stdout)
        if suggestions:
            logging.info(f"Suggestions from Gemini: {suggestions}")
            print(f"Suggestions from Gemini: {suggestions}")
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
        # Run the iperf3 client to connect to the iperf3 server on localhost
        result = subprocess.run(
            "iperf3 -c 127.0.0.1 -t 30",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logging.info("Network stress test completed")
        logging.info(f"Network stress test output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Network stress test failed: {e}")
        logging.error(f"Error output: {e.stderr}")

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
            "sysbench --mysql-host=192.168.1.7 --mysql-user=root "
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
