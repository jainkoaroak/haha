import urllib.request
import re
import random
import time
import subprocess

url = 'https://gmgn.ai/defi/quotation/v1/rank/sol/swaps/1h?orderby=volume&direction=desc'

# New list of user agents
user_agents = [
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
]

# Randomly select a User-Agent
headers = {
    "User-Agent": random.choice(user_agents),
    "Referer": "https://gmgn.ai/defi/quotation/v1/rank/sol/swaps/1h?orderby=volume&direction=desc",
    "Cookie": "__cf_bm=u7sgYmsyRhbI8vupsXI20aKePVzZVhF7d8uUWHl1n.A-1729833831-1.0.1.1-BBxIPbnnZLkd4fZ.e7H0aMYezbUpmYQh0uAKoNuGh3M4uVL1j0CgQr5UWMsLls6J6kaGECbWrnnSelu7jwgOCw; cf_clearance=EwXYIAtfPKykyHZRcGlh2ni1LPAf54m2gNftnpKMauY-1729833779-1.2.1.1-LHjZvq62JAWKBG4LoS3l2ahHhBtYZkT_IM_klue1q8Ld_Wl5ZX5C1trlLuguzomvO37vovoP8A4EsP_b_PPGyuNJkisuw9zUvYJKUtXWOfT9V6SRB81CTDZZ4wxTYsTtIHSUOHEO0pKTblJEPLjgW3WWTiRMCr9X5lgfp2nM9BREfo5x1SwbohuPnerOHLBqDrJ1Gw7Wx559KGINB7_0efmVcPGYq_JfXyxVg3aHPHj4rN0UkqGfNCYhA.hZY4zKhDwxeuHTaqP381qqnbHj33r1_m3jucFzho3czlSHyIO09Tf1Y.XlVc0_BzKpBwCNoPO0YNN3ahyfUbQrJQLUT1CTR7b3IPLk1EU7pnrork7YIDsgEdE8J4Idrrmgns3Ztb1hokCDwgjhmFs7XmwMbg"
}

def fetch_and_push():
    # Create a request object with the headers
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as fhand:
            addresses = []  # List to store addresses
            for line in fhand:
                # Decode the line from bytes to string
                line_str = line.decode('utf-8')
                # Adjust regex to capture "address" and the string of numbers following it
                matches = re.findall(r'"address":\s*"([^"]+)"', line_str)  # Find all matches
                addresses.extend(matches)  # Add matches to the list
                addresses.append("")
                
                # Stop after collecting 20 addresses
                if len(addresses) >= 7:
                    break

            # Format the collected addresses as a JSON-like list
            output = f'[{", ".join([f"{address!r}" for address in addresses[:7]])}]'

            # Write the output to the local file
            with open('mints.txt', 'w') as file:
                file.write(output)

            # Git commands to push the file to the repository
            subprocess.run(["git", "add", "mints.txt"])
            subprocess.run(["git", "commit", "-m", "Update mints.txt"])
            subprocess.run(["git", "push"])

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")

if __name__ == "__main__":
    while True:
        fetch_and_push()
        # Wait for 30 minutes (1800 seconds)
        time.sleep(1800)
