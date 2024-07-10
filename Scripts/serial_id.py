import winreg

def get_serial_number():
    try:
        # Open the Windows Registry key where the serial number is stored
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        
        # Query the value of the serial number
        value, _ = winreg.QueryValueEx(key, "MachineGuid")
        
        return value

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    serial_number = get_serial_number()
    print(f"Serial Number: {serial_number}")
