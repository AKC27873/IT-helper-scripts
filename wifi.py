import subprocess
import sys
import getpass
import time


def get_available_networks():
    print("Scanning for Wi-Fi Networks")
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=Bssid"],
            capture_output=True, text=True
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error scanning networks: {e}")


def connect_to_wifi():
    ssid = input("Enter the SSID(Name of Network): ").strip()
    password = getpass.getpass(f"Enter the password for '{ssid}': ")

    print(f"Attempting to connect to the provided {ssid}... ")
    try:
        profiles = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True, text=True
        )
        profile_exists = ssid in profiles.stdout

        if profile_exists:
            print(f"\033[92mProfile found for '{ssid}', connecting...\033[0m")
            profiles = subprocess.run(
                ["netsh", "wlan", "connect", f"name={ssid}"])
        else:
            print(f"\033[92mNo Profile found for '{
                  ssid}', creating a new profile for you using the credentials provided...\033[0m")
            # Builds a Wi-Fi profile XML and add it
            profile_xml = f"""<?xml version=\"1.0\"?>
            <WLANProlfile xmlns = "http://www.microsoft.com/networking/WLAN/profile/v1" >
                <name>{ssid}<name>
                <SSIDConfig>
                    <SSID>
                        <name>{ssid}<name>
                    </SSID>
                </SSIDConfig>
                <connectionType>ESS</connectionType>
                <connectionMode>manual</connectionMode>
                <MSM>
                    <security>
                        <authEncryption>
                            <authentication>WPA2PSK</authentication>
                            <encryption>AES</encryption>
                        </authEncryption>
                        <sharedKey>
                            <KeyType>passPhrase</KeyType>
                            <protected>false</protected>
                            <keymaterial>{password}</keymaterial>
                        </sharedKey>
                    </security>
                <MSM>
            </WLANProlfile>"""
            profile_path = "wifi_profile.xml"
            with open(profile_path, "w") as f:
                f.write(profile_xml)
                subprocess.run(
                    ["netsh", "wlan", "add", "profile",
                        f"filename={profile_xml}"],
                    subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"]))

        time.sleep(3)
        get_available_networks()

    except Exception as e:
        print(f"Error conenecting to network {e}")


def disconnect_wifi():
    print("\033[96mDisconnecting from current Wi-Fi network...\033[0m")
    try:
        subprocess.run(["netsh", "wlan", "disconnect"])
        print("\033[92mDisconnected Successfully. \033[0m")
    except Exception as e:
        print(f"Error disconnecting: {e}")


def get_connection_status():
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"],
                                capture_output=True, text=True
                                )
        print("\033[96mCurrent Wi-Fi Connection Status: \033[0m")
        print(result.stdout)
    except Exception as e:
        print(f"Error retrieving status: {e}")


def show_menu():
    menu_options = {
        "1": ("Veiw Available Wi-Fi Networks", get_available_networks()),
        "2": ("Connect to a Wi-Fi Network", connect_to_wifi()),
        "3": ("Disconnect from Current Wi-Fi", disconnect_wifi()),
        "4": ("Show Current Wi-Fi Connection Status", get_connection_status()),
        "5": ("Exit", None,),
    }
    while True:
        print("\n\033[92m -- Wi-Fi Mangement Menu ---\033[0m")
        for key, (label, _) in menu_options.items():
            print(f"  {key}. {label}")

        choice = input("Enter your choice: ").strip()

        if choice == "5":
            print("\033[92mExiting program. Goodbye!\033[0m")
            sys.exit(0)
        elif choice in menu_options:
            menu_options[choice][1]()
        else:
            print(
                "\033[91mInvalid choice. Please pick a choice from the menu list.\033[0m")


if __name__ == "__main__":
    show_menu()
