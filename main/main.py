import os, random, netifaces, subprocess, ctypes, sys, time

def admincheck():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def runcmd(command):
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"{process.stderr}")
    else:
        print(process.stdout)

def promptuser():
    response = input("Your PC needs to restart for the changes to take effect.\nRestart now? (y/n): ")
    if response.lower() == 'y':
        os.system("shutdown /r /t 0")

def getinterface():
    interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    return interface

def spoofmac():
    interface = getinterface()
    newmac = f"DE:{''.join(random.choices('0123456789ABCDEF', k=2))}:{''.join(random.choices('0123456789ABCDEF', k=2))}:{''.join(random.choices('0123456789ABCDEF', k=2))}:{''.join(random.choices('0123456789ABCDEF', k=2))}:{''.join(random.choices('0123456789ABCDEF', k=2))}"
    runcmd(f"netsh interface set interface \"{interface}\" admin=disable")
    runcmd(f"reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\0001 /v NetworkAddress /t REG_SZ /d {newmac} /f")
    runcmd(f"netsh interface set interface \"{interface}\" admin=enable")
    print(f"MAC Address spoofed to: {newmac}")
    print("[38;5;41mSpoofed! [0m")
    promptuser()

def unspoof():
    interface = getinterface()
    runcmd(f"netsh interface set interface \"{interface}\" admin=disable")
    runcmd(f"reg delete HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\0001 /v NetworkAddress /f")
    runcmd(f"netsh interface set interface \"{interface}\" admin=enable")
    print("[38;5;41mUnspoofed! [0m")
    promptuser()

def unpoison():
    tempfolder = os.getenv('TEMP')
    localfolder = os.getenv('LOCALAPPDATA')
    rblxfolder = os.path.join(localfolder, "Roblox")

    runcmd(f'cd /d "{tempfolder}" && del /q /f * && rd /s /q "{tempfolder}"')
    print("Temp Cleared...")

    if os.path.exists(rblxfolder):
        runcmd(f'rd /s / q "{rblxfolder}"')
        print("RBLX folder deleted...")
    else:
        print("RBLX folder not found...")

    print("[38;5;41mUnpoisoned![0m")

def mainmenu():
    while True:
        logo = """--------------------------------------------------------------
 ______         _       _____                    __          
|  ____|       | |     / ____|                  / _|         
| |__ ___  _ __| | __ | (___  _ __   ___   ___ | |_ ___ _ __ 
|  __/ _ \| '__| |/ /  \___ \| '_ \ / _ \ / _ \|  _/ _ \ '__|
| | | (_) | |  |   <   ____) | |_) | (_) | (_) | ||  __/ |   
|_|  \___/|_|  |_|\_\ |_____/| .__/ \___/ \___/|_| \___|_|   
                             | |                            
toasty.dev <3                |_|                             
--------------------------------------------------------------
"""
        os.system('cls')
        print(f"""[38;5;212m{logo}[38;5;41m
[1] Spoof MAC
[2] Unspoof MAC
[3] Unpoison Roblox
[4] Exit""")
        
        ui = input("\n[0;36mSelect an option: ")

        if ui == '1':
            os.system('cls')
            print(f"""[38;5;212m{logo}
[38;5;196mSpoofing...[0m""")
            time.sleep(2)
            spoofmac()
            
        elif ui == '2':
            os.system('cls')
            print(f"""[38;5;212m{logo}
[38;5;196mUnspoofing...[0m""")
            time.sleep(2)
            unspoof()

        elif ui == '3':
            os.system('cls')
            print(f"""[38;5;212m{logo}
[38;5;196mUnposion...[0m""")
            time.sleep(2)
            unpoison()
            
        elif ui == '4':
            os.system('cls')
            print(f"""[38;5;212m{logo}[38;5;41m
[38;5;196mExiting...[0m""")
            time.sleep(2)
            os.system('cls')
            break
        else:
            print("Invalid input, please try again.")
        
        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    if admincheck():
        mainmenu()
    else:
        timer = 3
        os.system('cls')
        print("Forkspoofer requires administrative privileges, please run it as an administrator.")
        while timer > 0:
            time.sleep(1)
            print(f"Program will now close in {timer}...")
            timer -= 1
        sys.exit()
