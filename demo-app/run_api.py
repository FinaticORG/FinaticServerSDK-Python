#!/usr/bin/env python3
"""
Convenience script to run the Finatic Python Server SDK API
"""

import subprocess
import sys
import os


def main():
    """Run the API server with uvicorn"""
    print("🚀 Starting Finatic Python Server SDK API...")
    print("   Port: 8002")
    print("   CORS enabled for: http://localhost:3000")
    print("   Make sure FINATIC_API_KEY is set in your environment")
    print()

    # Check if .env file exists
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found. Please copy env.example to .env and configure it.")
        print()

    try:
        # Run uvicorn with the API server
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api_server:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8002",
                "--reload",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n🔄 Shutting down API server...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
