import socket
import subprocess
import sys
from datetime import datetime


# -----------------------------------------
# Blank Screen
# -----------------------------------------

subprocess.call("clear", shell=True)


# -----------------------------------------
# Prompt user for Server Information
# -----------------------------------------

remoteServer = input("Enter a remote host to scan: ")

try:
    remoteServerIp = socket.gethostbyname(remoteServer)

except socket.gaierror:
    print("Hostname could not be resolved. Exiting.")
    sys.exit()


print(f"\nScanning host: {remoteServer}")
print(f"IP address: {remoteServerIp}")


# -----------------------------------------
# Create Results File
# -----------------------------------------

report_file = "scan_results.txt"

try:

    report = open(report_file, "w")

    # Write scan date and time
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report.write(f"Scan time - {scan_time}\n")
    report.write(f"Remote host - {remoteServer}\n")
    report.write(f"IP address - {remoteServerIp}\n")
    report.write("\n")

except OSError:

    print("Could not create the scan results file.")
    sys.exit()


# -----------------------------------------
# Prompt user for Scan Type
# -----------------------------------------

portsToScan = 0

while portsToScan not in (1, 2):

    try:

        portsToScan = int(
            input(
                "\nEnter '1' to scan all ports "
                "or '2' to scan a range of ports: "
            )
        )

        if portsToScan not in (1, 2):
            print("Invalid option. Please enter 1 or 2.")

    except ValueError:

        print("Please enter 1 or 2.")


# -----------------------------------------
# Option 1 - Scan All Ports
# -----------------------------------------

if portsToScan == 1:

    print("\nScanning all ports from 1 to 65535...")
    print("-" * 40)

    try:

        for port in range(1, 65536):

            print("\nScanning port:", port)

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            # Set connection timeout to 0.1 seconds
            sock.settimeout(0.1)

            try:

                # Attempt to connect to the port
                sock.connect(
                    (remoteServerIp, port)
                )

                # Connection succeeded
                status = "Open"

            except socket.timeout:

                # Connection timed out
                status = "Timed Out"

            except socket.error:

                # Connection was refused or another
                # socket error occurred
                status = "Closed"

            finally:

                # Always close the socket
                sock.close()

            # Display result
            print(f"Port {port}: {status}")

            # Write result to text file
            report.write(
                f"Port : {port}   Status: {status}\n"
            )

    except KeyboardInterrupt:

        print("\nYou pressed Ctrl+C")
        print("Scan stopped.")

        report.write(
            "\nScan interrupted by user.\n"
        )

        report.close()

        sys.exit()


# -----------------------------------------
# Option 2 - Scan a Range of Ports
# -----------------------------------------

elif portsToScan == 2:

    while True:

        try:

            start_port = int(
                input(
                    "\nEnter the starting port (1-65535): "
                )
            )

            end_port = int(
                input(
                    "Enter the ending port (1-65535). "
                    "For a single port, enter the same value "
                    "as the starting port: "
                )
            )

            # Check that both ports are valid
            if 1 <= start_port <= 65535 and 1 <= end_port <= 65535:

                # Check that starting port isn't greater
                # than ending port
                if start_port <= end_port:

                    if start_port == end_port:

                        print(
                            f"\nScanning a single port: "
                            f"{start_port}"
                        )

                    else:

                        print(
                            f"\nScanning ports "
                            f"{start_port} through {end_port}"
                        )

                    break

                else:

                    print(
                        "Invalid range: starting port "
                        "must be <= ending port."
                    )

            else:

                print(
                    "Invalid port number. "
                    "Ports must be between 1 and 65535."
                )

        except ValueError:

            print("Please enter numbers only.")


    # -----------------------------------------
    # Scan the Selected Port Range
    # -----------------------------------------

    print("-" * 40)

    try:

        for port in range(start_port, end_port + 1):

            print("\nScanning port:", port)

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            # Set connection timeout to 0.1 seconds
            sock.settimeout(0.1)

            try:

                # Attempt to connect to the port
                sock.connect(
                    (remoteServerIp, port)
                )

                # Connection succeeded
                status = "Open"

            except socket.timeout:

                # Connection timed out
                status = "Timed Out"

            except socket.error:

                # Connection was refused or another
                # socket error occurred
                status = "Closed"

            finally:

                # Always close the socket
                sock.close()

            # Display result
            print(f"Port {port}: {status}")

            # Write result to text file
            report.write(
                f"Port : {port}   Status: {status}\n"
            )

    except KeyboardInterrupt:

        print("\nYou pressed Ctrl+C")
        print("Scan stopped.")

        report.write(
            "\nScan interrupted by user.\n"
        )

        report.close()

        sys.exit()


# -----------------------------------------
# Close Report File
# -----------------------------------------

report.close()

print("\nScan complete.")
print(f"Scan results saved to: {report_file}")



