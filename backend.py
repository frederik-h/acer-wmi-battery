import socket
import subprocess
import os

sock_path = "/tmp/acer-battery-control.sock"  # Choose a secure location
default_module_path = "/etc/acer-battery-control-gui/"
if os.path.exists(sock_path):
    os.remove(sock_path)

def run_command(command):
    print("run command: %s" % command)
    try:
        result = subprocess.run("sudo " + command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

def main():
    
    make_result = run_command(f"make -C {default_module_path}")
    make_result_str = make_result.decode("utf-8") # Decode to string

    if "error" not in make_result_str.lower():  # Check if make was successful
        insmod_command = f"insmod {default_module_path}acer-wmi-battery.ko"  # Only run insmod if make succeeded
        insmod_result = run_command(insmod_command)
        response = f"Make output:\n{make_result}\n\nInsmod output:\n{insmod_result}"
    else:
       response = f"Make error:\n{make_result}"  
    
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(sock_path)
    os.chmod(sock_path, 0o666)  # Set permissions for socket file
    sock.listen(5)

    print("backend started successfully")
    while True:
        conn, _ = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break

                command = data.strip()  # Get command from GUI
                       
                if command == "health_mode_on":
                    response = run_command("echo 1 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode")
                elif command == "health_mode_off":
                    response = run_command("echo 0 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/health_mode")
                elif command == "calibration_mode_on":
                     response = run_command("echo 1 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode")
                elif command == "calibration_mode_off":
                     response = run_command("echo 1 | sudo tee /sys/bus/wmi/drivers/acer-wmi-battery/calibration_mode")
                elif command.startswith("insmod"):  # Example: "insmod /path/to/module.ko"
                    response = run_command(f"{command}")  # Run insmod with sudo
                elif command == "ping":
                    response = "pong"
                else:
                    response = "Invalid command"

                if isinstance(response, bytes):
                    conn.sendall(response)  # Send bytes as is
                elif isinstance(response, str):
                    conn.sendall(response.encode("utf-8"))  # Encode string to bytes before sending
                else:
                    conn.sendall(str(response).encode("utf-8")) # Encode other types to bytes

if __name__ == "__main__":
    main()
