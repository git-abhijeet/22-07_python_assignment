"""
Redis Setup and Start Script for Zomato V3
==========================================

This script helps set up and start Redis for the Zomato V3 caching system.
It will attempt to connect to Redis and provide instructions if Redis is not available.
"""

import subprocess
import sys
import time
import socket
from redis_config import redis_config

def check_redis_connection():
    """Check if Redis is running and accessible"""
    try:
        import redis
        client = redis.Redis(
            host=redis_config.REDIS_HOST,
            port=redis_config.REDIS_PORT,
            password=redis_config.REDIS_PASSWORD,
            db=redis_config.REDIS_DB,
            socket_connect_timeout=5
        )
        client.ping()
        print("✅ Redis is running and accessible!")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def check_port_available(host, port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((host, port))
        return result != 0  # Port is available if connection fails
    finally:
        sock.close()

def install_redis_instructions():
    """Provide Redis installation instructions"""
    print("\n🔧 Redis Installation Instructions:")
    print("="*50)
    
    if sys.platform.startswith('win'):
        print("For Windows:")
        print("1. Download Redis from: https://github.com/microsoftarchive/redis/releases")
        print("2. Extract and run redis-server.exe")
        print("3. Or use Docker: docker run -d -p 6379:6379 redis:latest")
        print("4. Or use WSL2 with Ubuntu and install redis-server")
    
    elif sys.platform.startswith('darwin'):
        print("For macOS:")
        print("1. Install Homebrew: https://brew.sh/")
        print("2. Run: brew install redis")
        print("3. Start Redis: brew services start redis")
        print("4. Or use Docker: docker run -d -p 6379:6379 redis:latest")
    
    else:
        print("For Linux (Ubuntu/Debian):")
        print("1. Update packages: sudo apt update")
        print("2. Install Redis: sudo apt install redis-server")
        print("3. Start Redis: sudo systemctl start redis-server")
        print("4. Enable auto-start: sudo systemctl enable redis-server")
        print("5. Or use Docker: docker run -d -p 6379:6379 redis:latest")
    
    print("\n🐳 Docker Option (All Platforms):")
    print("docker run -d --name redis-zomato -p 6379:6379 redis:latest")
    print("\nAfter installation, restart this application!")

def start_redis_docker():
    """Attempt to start Redis using Docker"""
    try:
        print("🐳 Attempting to start Redis using Docker...")
        
        # Check if Docker is available
        subprocess.run(['docker', '--version'], 
                      check=True, capture_output=True)
        
        # Try to start Redis container
        result = subprocess.run([
            'docker', 'run', '-d', 
            '--name', 'redis-zomato-v3',
            '-p', '6379:6379',
            'redis:latest'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Redis container started successfully!")
            print("⏳ Waiting for Redis to initialize...")
            
            # Wait for Redis to start
            for i in range(10):
                time.sleep(1)
                if check_redis_connection():
                    return True
                print(f"⏳ Waiting... ({i+1}/10)")
            
            print("❌ Redis container started but connection failed")
            return False
        else:
            print(f"❌ Failed to start Redis container: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Docker is not available")
        return False
    except Exception as e:
        print(f"❌ Failed to start Redis: {e}")
        return False

def main():
    """Main function to check and setup Redis"""
    print("🗄️ Zomato V3 Redis Setup")
    print("="*30)
    
    # Check if Redis is already running
    if check_redis_connection():
        print("🚀 Redis is ready! You can start the Zomato V3 application.")
        return True
    
    print(f"🔍 Checking if port {redis_config.REDIS_PORT} is available...")
    if not check_port_available(redis_config.REDIS_HOST, redis_config.REDIS_PORT):
        print(f"⚠️ Port {redis_config.REDIS_PORT} is in use but Redis connection failed.")
        print("Please check if Redis is running or if another service is using the port.")
        return False
    
    print("🔧 Redis is not running. Attempting to start...")
    
    # Try to start Redis with Docker
    if start_redis_docker():
        print("✅ Redis is now running! You can start the Zomato V3 application.")
        return True
    
    # If Docker fails, provide installation instructions
    print("\n❌ Could not start Redis automatically.")
    install_redis_instructions()
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
