import redis
import time
import multiprocessing

redis_host = 'localhost' 
heartbeat_interval = 3 
key_expiry = 10 

def simulate_device(device_id, start_delay, fail_after):
    r = redis.Redis(host=redis_host, port=6379, db=0)
    time.sleep(start_delay) 

    count = 0
    while True:
        r.setex(f"device:{device_id}", key_expiry, "alive")
        print(f"Device {device_id} heartbeat sent.")
        time.sleep(heartbeat_interval)

        count += 1
        if count >= fail_after: 
            print(f"Device {device_id} simulating failure.")
            break

def main():
    devices = {
        'A': multiprocessing.Process(target=simulate_device, args=('A', 0, 5)),  
        'B': multiprocessing.Process(target=simulate_device, args=('B', 5, 5)),  
        'C': multiprocessing.Process(target=simulate_device, args=('C', 10, 5)), 
    }

    for device in devices.values():
        device.start()

    for device in devices.values():
        device.join()

if __name__ == "__main__":
    main()
