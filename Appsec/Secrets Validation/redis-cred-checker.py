import redis      
import argparse      
import sys      
      
def check_redis_credentials(hostname, username, password, port=6379):      
    """      
    Check if Redis credentials are valid by attempting to connect      
    and perform a simple operation      
    """      
    try:      
        # Create Redis connection      
        redis_client = redis.Redis(      
            host=hostname,      
            port=port,      
            username=username,      
            password=password,      
            decode_responses=True,      
            socket_timeout=5      
        )      
      
        # Try to ping the Redis server      
        if redis_client.ping():      
            print("[+] Successfully connected to Redis server!")      
                  
            # Try to get server info      
            info = redis_client.info()      
            print(f"[+] Redis Version: {info['redis_version']}")      
            print(f"[+] Connected clients: {info['connected_clients']}")      
            print(f"[+] Used memory: {info['used_memory_human']}")      
                  
            return True      
      
    except redis.AuthenticationError:      
        print("[-] Authentication failed: Invalid username or password")      
        return False      
          
    except redis.ConnectionError:      
        print("[-] Connection failed: Unable to connect to Redis server")      
        return False      
          
    except Exception as e:      
        print(f"[-] Error: {str(e)}")      
        return False      
          
    finally:      
        try:      
            redis_client.close()      
        except:      
            pass      
      
def main():      
    # Create argument parser      
    parser = argparse.ArgumentParser(description='Redis Credential Checker')      
          
    # Add arguments      
    parser.add_argument('-H', '--host', required=True, help='Redis host')      
    parser.add_argument('-u', '--username', default='default', help='Redis username (default: default)')      
    parser.add_argument('-p', '--password', required=True, help='Redis password')      
    parser.add_argument('-P', '--port', type=int, default=6379, help='Redis port (default: 6379)')      
      
    # Parse arguments      
    args = parser.parse_args()      
      
    print(f"[*] Attempting to connect to Redis server at {args.host}:{args.port}")      
    print(f"[*] Using username: {args.username}")      
      
    # Check credentials      
    success = check_redis_credentials(      
        hostname=args.host,      
        username=args.username,      
        password=args.password,      
        port=args.port      
    )      
      
    # Exit with appropriate status code      
    sys.exit(0 if success else 1)      
      
if __name__ == "__main__":      
    main()      
