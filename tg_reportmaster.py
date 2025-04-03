import time
import random
import asyncio
import json
import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ReportSpamRequest
from datetime import datetime

# 🚀 Colorful Terminal Support
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# 🎮 Menu Design
def print_menu():
    print(f"""
    {BLUE}====================================================={RESET}
    {YELLOW}🚀 TG-ReportMaster - Leronru Edition{RESET}
    {BLUE}====================================================={RESET}
    {GREEN}1. Report Channel{RESET}
    {GREEN}2. Configure Proxy Settings{RESET}
    {GREEN}3. Select Language{RESET}
    {GREEN}4. View Report History{RESET}
    {GREEN}5. Exit{RESET}
    {BLUE}====================================================={RESET}
    """)

# 🎮 Making a Selection
def get_choice():
    choice = input(GREEN + "Choose an option (1-5): " + RESET)
    return choice

# 🛠 Proxy Management and Verification
def configure_proxy():
    print(BLUE + "Configuring proxy settings..." + RESET)
    proxy_type = input(GREEN + "Proxy type (socks5/http): " + RESET).strip()
    proxy_address = input(GREEN + "Proxy address: " + RESET).strip()
    proxy_port = input(GREEN + "Proxy port: " + RESET).strip()

    # Proxy validation
    try:
        proxy = (proxy_type, proxy_address, int(proxy_port))
        print(f"{GREEN}Proxy set to {proxy_type}://{proxy_address}:{proxy_port}." + RESET)
    except Exception as e:
        print(RED + f"Invalid proxy settings: {e}" + RESET)

# 🌐 Language Selection
def choose_language():
    print(BLUE + "Language Selection Menu:" + RESET)
    print("1. Turkish")
    print("2. English")
    lang_choice = input(GREEN + "Choose language (1-2): " + RESET).strip()
    
    if lang_choice == '1':
        print(GREEN + "Turkish selected." + RESET)
    else:
        print(GREEN + "English selected." + RESET)

# 📜 Viewing Report History
def show_report_history():
    log_file = "report_logs.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
            if logs:
                for log in logs:
                    print(f"{YELLOW}Report Time: {log['timestamp']}{RESET}")
                    print(f"{BLUE}Channel: {log['channel']}{RESET}")
                    print(f"{RED}Reason: {log['reason']}{RESET}")
                    print(f"{GREEN}Report Count: {log['report_number']}{RESET}")
                    print("-" * 50)
            else:
                print(RED + "No previous reports found." + RESET)
    else:
        print(RED + "No previous reports saved." + RESET)

# 🔹 Getting Target Channel and Report Information
def get_target_info():
    print(BLUE + "\n🎯 Enter target channel information." + RESET)
    target_channel = input(GREEN + "⚠️ Channel to report (@channelname): " + RESET).strip()
    reason = input(GREEN + "⚠️ Reason for report (e.g., spam, inappropriate content): " + RESET).strip()
    return target_channel, reason

# 🔹 Getting API Information
def get_api_info():
    print(BLUE + "📢 TG-ReportMaster Tool v10000000000000000000000000000" + RESET)
    print(YELLOW + "🔹 Enter your API ID and Hash information." + RESET)

    api_id = input(GREEN + "⚙️ API ID: " + RESET).strip()
    api_hash = input(GREEN + "🔑 API Hash: " + RESET).strip()
    phone = input(GREEN + "📱 Phone number (+90... or bot token): " + RESET).strip()

    return {"api_id": api_id, "api_hash": api_hash, "phone": phone}

# 🔹 Report Function (Asynchronous)
async def report_channel(client, channel, reason, max_reports=900000000):
    try:
        entity = await client.get_entity(channel)
        success_count = 0
        for i in range(max_reports):
            await client(ReportSpamRequest(peer=entity))
            success_count += 1
            print(GREEN + f"✅ [{success_count}/{max_reports}] {channel} successfully reported for {reason}!" + RESET)

            # 🔹 Log Record
            log_report({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "channel": channel,
                "reason": reason,
                "report_number": success_count
            })

            await asyncio.sleep(random.uniform(0.1, 0.5))

    except Exception as e:
        print(RED + f"❌ Error: {e}" + RESET)

# 🔹 Start the Bot
def start_bot():
    api_info = get_api_info()
    target_channel, reason = get_target_info()

    print(f"{YELLOW}Starting the bot...{RESET}")
    with TelegramClient(api_info["phone"], api_info["api_id"], api_info["api_hash"]) as client:
        try:
            client.loop.run_until_complete(report_channel(client, target_channel, reason))
        except Exception as e:
            print(RED + f"⚠️ Login error: {e}" + RESET)
            sys.exit(1)

# 🔹 Log Record Function
def log_report(data):
    log_file = "report_logs.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(data)
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

# 🎮 Run Main Menu
def main_menu():
    while True:
        print_menu()
        choice = get_choice()

        if choice == '1':
            start_bot()
        elif choice == '2':
            configure_proxy()
        elif choice == '3':
            choose_language()
        elif choice == '4':
            show_report_history()
        elif choice == '5':
            print(f"{RED}Exiting...{RESET}")
            break
        else:
            print(RED + "Invalid choice. Please try again." + RESET)

# 🎮 Start Program
if __name__ == "__main__":
    main_menu()
