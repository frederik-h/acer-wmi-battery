import socket
import subprocess
import os

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

def main():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock_path = "/tmp/acer-battery-control.sock"  # Choose a secure location

    try:
        os.unlink(sock_path)  # Remove existing socket if any
    except FileNotFoundError:
        pass

    sock.bind(sock_path)
    sock.listen(1)

    while True:
        conn, _ = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break

                command = data.strip()  # Get command from GUI
                if command.startswith("make_and_insmod"):
                    module_path = command.split(" ", 1)[1] # Get module path from command
                    make_result = run_command(f"sudo make -C {module_path}") # Run make with sudo

                    if "error" not in make_result.lower(): # Check if make was successful
                       insmod_command = f"sudo insmod {module_path}/acer-wmi-battery.ko" # Only run insmod if make succeeded
                       insmod_result = run_command(insmod_command)
                       response = f"Make output:\n{make_result}\n\nInsmod output:\n{insmod_result}"

                    else:
                       response = f"Make error:\n{make_result}"
                       
                elif command == "health_mode_on":
                    response = run_command("sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode <<< 1")
                elif command == "health_mode_off":
                    response = run_command("sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode <<< 0")
                elif command == "calibration_mode_on":
                     response = run_command("sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode <<< 1")
                elif command == "calibration_mode_off":
                     response = run_command("sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode <<< 0")
                elif command.startswith("insmod"):  # Example: "insmod /path/to/module.ko"
                    response = run_command(f"sudo {command}")  # Run insmod with sudo
                else:
                    response = "Invalid command"

                conn.sendall(response.encode("utf-8"))

if __name__ == "__main__":
    main()