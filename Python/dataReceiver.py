#!/usr/bin/env python3
"""
UDP Server for Mac/Raspberry Pi to receive data from Meta Quest
This replaces the serial connection from your original Arduino/ESP32 setup
Works on both macOS and Linux (Raspberry Pi)
"""

import socket
import threading
import time
import json
import platform
import subprocess
from datetime import datetime


class QuestDataReceiver:
    def __init__(self, host='0.0.0.0', port=8080):
        """
        Initialize the UDP server
        host: '0.0.0.0' means listen on all network interfaces
        port: Must match the port in your Unity Quest app
        """
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.received_data = []

    def start_server(self):
        """Start the UDP server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Allow reusing the address/port
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.running = True

            print(f"🚀 Quest Data Receiver started on {self.host}:{self.port}")
            print(f"📡 Server IP Address: {self.get_pi_ip()}")
            print(f"🔧 Debug mode: Enhanced logging enabled")
            print("👀 Waiting for data from Quest...")
            print("-" * 50)

            # Start listening in a separate thread
            listen_thread = threading.Thread(target=self._listen_for_data)
            listen_thread.daemon = True
            listen_thread.start()

            return True

        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False

    def _listen_for_data(self):
        """Listen for incoming UDP data"""
        self.socket.settimeout(1.0)  # Add timeout to prevent hanging

        while self.running:
            try:
                # Receive data (buffer size 1024 bytes)
                print("🔍 Listening for data...")  # Debug: Show we're actively listening
                data, client_address = self.socket.recvfrom(1024)

                # Decode the received data
                message = data.decode('utf-8')
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                # Log the received data
                print(f"[{timestamp}] 📨 From {client_address[0]}:{client_address[1]}")
                print(f"         Data: '{message}' (Length: {len(message)} bytes)")
                print(f"         Raw bytes: {data}")

                # Store the data
                self.received_data.append({
                    'timestamp': timestamp,
                    'client': f"{client_address[0]}:{client_address[1]}",
                    'data': message
                })

                # Process the data (this is where you'd add your custom logic)
                self._process_received_data(message, client_address)

            except socket.timeout:
                # This is normal - just continue listening
                continue
            except socket.error as e:
                if self.running:  # Only print error if we're supposed to be running
                    print(f"❌ Socket error: {e}")
                break
            except Exception as e:
                print(f"❌ Error receiving data: {e}")
                import traceback
                traceback.print_exc()

    def _process_received_data(self, message, client_address):
        """
        Process the received data from Quest
        This is where you'd add your custom logic based on what the Quest sends
        """

        # Example: Handle different types of messages
        if message.startswith("BUTTON:"):
            button_data = message.replace("BUTTON:", "")
            print(f"   🎮 Button pressed: {button_data}")

        elif message.startswith("POSITION:"):
            position_data = message.replace("POSITION:", "")
            print(f"   📍 Position update: {position_data}")

        elif message.startswith("GESTURE:"):
            gesture_data = message.replace("GESTURE:", "")
            print(f"   👋 Gesture detected: {gesture_data}")

        elif message == "Hello World!":
            print(f"   👋 Received test message from Quest!")

        else:
            print(f"   💬 Raw message: {message}")

        # You could also send a response back to the Quest if needed
        # self._send_response(client_address, "ACK")

    def _send_response(self, client_address, response):
        """Send a response back to the Quest (optional)"""
        try:
            response_data = response.encode('utf-8')
            self.socket.sendto(response_data, client_address)
            print(f"   📤 Sent response: '{response}'")
        except Exception as e:
            print(f"❌ Failed to send response: {e}")

    def get_pi_ip(self):
        """Get the local IP address on Mac or Raspberry Pi"""
        system = platform.system().lower()

        try:
            # Method 1: Connect to remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]

            # Method 2: Get all network interfaces for verification
            interfaces = self._get_network_interfaces()

            print(f"🖥️  System: {platform.system()} {platform.release()}")
            print(f"📍 Primary IP: {local_ip}")

            if interfaces:
                print("🌐 Available network interfaces:")
                for interface, ip in interfaces.items():
                    marker = " ← Using this" if ip == local_ip else ""
                    print(f"   {interface}: {ip}{marker}")

            return local_ip

        except Exception as e:
            print(f"⚠️  Could not determine IP automatically: {e}")
            return self._fallback_ip_detection()

    def _get_network_interfaces(self):
        """Get network interfaces for both Mac and Linux"""
        interfaces = {}
        system = platform.system().lower()

        try:
            if system == "darwin":  # macOS
                # Use ifconfig on Mac
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                interfaces = self._parse_ifconfig_mac(result.stdout)
            elif system == "linux":  # Raspberry Pi
                # Use ip command on Linux (preferred) or fallback to ifconfig
                try:
                    result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
                    interfaces = self._parse_ip_addr_linux(result.stdout)
                except FileNotFoundError:
                    # Fallback to ifconfig if ip command not available
                    result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                    interfaces = self._parse_ifconfig_linux(result.stdout)

        except Exception as e:
            print(f"⚠️  Could not get network interfaces: {e}")

        return interfaces

    def _parse_ifconfig_mac(self, ifconfig_output):
        """Parse macOS ifconfig output"""
        interfaces = {}
        current_interface = None

        for line in ifconfig_output.split('\n'):
            if line and not line.startswith('\t') and not line.startswith(' '):
                # New interface line
                current_interface = line.split(':')[0]
            elif 'inet ' in line and current_interface:
                # Extract IP address
                parts = line.strip().split()
                for i, part in enumerate(parts):
                    if part == 'inet' and i + 1 < len(parts):
                        ip = parts[i + 1]
                        if not ip.startswith('127.'):  # Skip localhost
                            interfaces[current_interface] = ip
                        break

        return interfaces

    def _parse_ifconfig_linux(self, ifconfig_output):
        """Parse Linux ifconfig output"""
        interfaces = {}
        current_interface = None

        for line in ifconfig_output.split('\n'):
            if line and not line.startswith(' '):
                # New interface line
                current_interface = line.split(':')[0]
            elif 'inet ' in line and current_interface:
                # Extract IP address
                parts = line.strip().split()
                for i, part in enumerate(parts):
                    if part == 'inet' and i + 1 < len(parts):
                        ip = parts[i + 1]
                        if not ip.startswith('127.'):  # Skip localhost
                            interfaces[current_interface] = ip
                        break

        return interfaces

    def _parse_ip_addr_linux(self, ip_output):
        """Parse Linux 'ip addr show' output"""
        interfaces = {}
        current_interface = None

        for line in ip_output.split('\n'):
            if ': ' in line and not line.startswith(' '):
                # New interface line
                parts = line.split(': ')
                if len(parts) > 1:
                    current_interface = parts[1].split('@')[0]  # Remove @if_name suffix
            elif 'inet ' in line and current_interface:
                # Extract IP address
                line = line.strip()
                if line.startswith('inet '):
                    ip = line.split()[1].split('/')[0]  # Remove subnet mask
                    if not ip.startswith('127.'):  # Skip localhost
                        interfaces[current_interface] = ip

        return interfaces

    def _fallback_ip_detection(self):
        """Fallback IP detection method"""
        try:
            # Get hostname and resolve it
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if not ip.startswith('127.'):
                return ip
        except:
            pass

        # Last resort - return localhost
        return "127.0.0.1"

    def stop_server(self):
        """Stop the UDP server"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("\n🛑 Server stopped")

    def get_stats(self):
        """Get statistics about received data"""
        return {
            'total_messages': len(self.received_data),
            'server_running': self.running,
            'last_10_messages': self.received_data[-10:] if self.received_data else []
        }


def main():
    """Main function to run the server"""
    receiver = QuestDataReceiver(port=8081)  # Use port 8080 to match Unity code

    try:
        if receiver.start_server():
            print("\n💡 Commands:")
            print("   - Press Ctrl+C to stop the server")
            print("   - Make sure your Quest app uses this server's IP address")
            print(f"   - In Unity, set m_serverIP to: {receiver.get_pi_ip()}")

            # Keep the main thread alive
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n⏹️  Shutting down server...")
        receiver.stop_server()

        # Print final stats
        stats = receiver.get_stats()
        print(f"\n📊 Final Stats:")
        print(f"   Total messages received: {stats['total_messages']}")
        if stats['last_10_messages']:
            print(f"   Last message: {stats['last_10_messages'][-1]['data']}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        receiver.stop_server()


if __name__ == "__main__":
    main()