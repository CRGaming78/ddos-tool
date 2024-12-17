# DDOS Tool Documentation

## Overview
The **DDOS Tool** is a Python-based utility designed for testing server resiliency through simulated HTTP POST floods and DNS flood attacks. It is intended for educational and ethical testing purposes only. Misusing this tool for unauthorized attacks is strictly prohibited.

This tool allows users to target single or multiple endpoints, select different attack intensities, and simulate concurrent flooding attacks with control over the request rate.

## Features
1. **Target Verification**: Verifies if the target server or URL is reachable before initiating attacks.
2. **Attack Types**:
   - **HTTP POST Flood**: Sends repeated HTTP POST requests with dummy data.
   - **DNS Flood Simulation**: Generates randomized subdomain queries to overwhelm the target.
3. **Concurrency Control**: Ensures controlled concurrency for efficiency and to avoid resource overuse.
4. **Intensity Levels**:
   - **Low**: 1 request per second
   - **Medium**: 1 request every 0.5 seconds
   - **High**: 1 request every 0.2 seconds

## Requirements
- Python 3.8+
- Libraries:
  - `aiohttp`
  - `asyncio`
  - `requests`

You can install required libraries using:
```bash
pip install aiohttp requests
```

## Usage
1. Run the script:
   ```bash
   python ddos_tool.py
   ```
2. Choose whether to attack **multiple targets** or a **single target**.
3. Provide the target domain(s) or IP address(es).
4. Select the desired **attack type**:
   - HTTP POST Flood
   - DNS Flood
5. Choose the **attack intensity**:
   - Low
   - Medium
   - High

The tool will then initiate the attack.

### Example Run
1. Select a single target:
   ```
   Enter 'y' for multiple targets or 'n' for a single target: n
   Enter the domain or IP address: http://example.com
   Target http://example.com is reachable.
   Select Attack Type:
   1. HTTP POST Flood
   2. DNS Flood
   Choose attack type (1/2): 1
   Select Intensity:
   1. Low Intensity (1 request every 1 second)
   2. Medium Intensity (1 request every 0.5 seconds)
   3. High Intensity (1 request every 0.2 seconds)
   Choose mode (1/2/3): 3
   Starting attack on single target...
   ```

2. Logs are generated in `ddos_tool.log`:
   ```
   2024-12-17 12:00:00 - HTTP POST | Target: http://example.com | Status Code: 200
   2024-12-17 12:00:01 - HTTP POST | Target: http://example.com | Status Code: 200
   ```

## Code Explanation
### Target Verification
- Verifies whether the given target URL or domain is reachable.
```python
response = requests.get(target, timeout=5, headers=get_random_user_agent())
```

### HTTP POST Flood
- Repeatedly sends HTTP POST requests to overwhelm the target.
```python
async with session.post(target, headers=get_random_user_agent(), data={"key": "value"}) as response:
```

### DNS Flood Simulation
- Simulates DNS flooding by querying randomized subdomains.
```python
dns_query = f"example-{random.randint(1000, 9999)}.com"
async with session.get(target, headers=get_random_user_agent(), params={"q": dns_query}) as response:
```

### Concurrency Control
- Limits the number of concurrent tasks to avoid resource overload.
```python
semaphore = asyncio.Semaphore(200)
```

## Legal Disclaimer
This tool is intended **only for ethical and educational purposes** such as:
- Stress testing your own servers
- Learning about DDoS mitigation techniques
- Security research under appropriate supervision

**Unauthorized use of this tool against systems you do not own or have explicit permission to test is illegal and unethical.**

## Logging
All attack activity, including successes and errors, is logged to `ddos_tool.log` for review and debugging.

## Future Improvements
- Add IP spoofing simulation for testing defenses.
- Implement UDP flooding.
- Integrate attack termination mechanisms.

## Author
This tool is developed for cybersecurity educational purposes. Ensure responsible use of this tool.

---
**Use responsibly and ethically!**
