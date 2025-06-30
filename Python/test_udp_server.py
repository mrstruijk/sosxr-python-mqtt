#!/usr/bin/env python3
"""
Simple UDP test client to verify the server is working
Run this from the same machine or another device on the network
"""

import socket
import time


def test_udp_server(server_ip, server_port=8080):
    """Test the UDP server by sending some data"""

    print(f"🧪 Testing UDP server at {server_ip}:{server_port}")

    try:
        # Create UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Test messages
        test_messages = [
            "Hello World!",
            "BUTTON:A_PRESSED",
            "POSITION:1.23,4.56,7.89",
            "GESTURE:WAVE",
            "Test message from Python client"
        ]

        for i, message in enumerate(test_messages, 1):
            print(f"📤 Sending message {i}: '{message}'")

            # Send the message
            client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

            print(f"✅ Sent successfully")
            time.sleep(1)  # Wait 1 second between messages

        client_socket.close()
        print("🎉 All test messages sent!")

    except Exception as e:
        print(f"❌ Error testing server: {e}")


if __name__ == "__main__":
    # Test locally first
    print("Testing localhost...")
    test_udp_server("127.0.0.1")

    print("\n" + "=" * 50)

    # Test your actual IP (change this to your server's IP)
    server_ip = input("Enter server IP address (or press Enter for localhost): ").strip()
    if not server_ip:
        server_ip = "127.0.0.1"

    print(f"\nTesting {server_ip}...")
    test_udp_server(server_ip)