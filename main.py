import subprocess
import platform
import getpass
from pprint import pprint


def parser(info: str) -> dict:
    wifies = []
    info = info.split("\n")
    columns = [i for i in info[0].strip().split()]

    for line in info[1:]:
        wifi_info = {}
        flag = 0
        result = []
        for t in line.strip().split():
            if len(t.split(":")) == 6:
                tmp = str(result)[1:-1].replace(',', '').replace('\'', '')
                result = [tmp]
                ap = t
                flag = 1
            elif flag == 1:
                ap = int(t)
                flag = 2
            elif flag == 2:
                ap = [int(i) for i in t.split(',')]
                flag = -1
            else: ap = t
            result.append(ap)


        wifies.append({columns[i]:result[i] for i in range(len(result))})
    return wifies
def get_wifi_list(os_type: str):

    if os_type == "Windows":
        pass

    elif os_type == "Linux":
        pass

    elif os_type == "Darwin":  # macOS
        airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        sudo_password = getpass.getpass("Enter your sudo password: ")
        command = f'echo {sudo_password} | sudo -S {airport_path} -s'
        wifi_str = subprocess.run(command, capture_output=True, text=True, shell=True).stdout

        data = []
        line_list = wifi_str.strip().split('\n')[1:]

        for line in line_list:
            parts = line.split()
            ssid = parts[0]
            bssid = parts[1]
            rssi = int(parts[2])
            channel = [int(ch) for ch in parts[3].split(',')]
            ht = parts[4]
            cc = parts[5]
            security = ' '.join(parts[6:])

            data.append({
                "SSID": ssid,
                "BSSID": bssid,
                "RSSI": rssi,
                "CHANNEL": channel,
                "HT": ht,
                "CC": cc,
                "SECURITY": security
            })


    else: #OS 미지원
        raise NotImplementedError(f"OS type {os_type} is not supported")

    return data


def target_wifi_filtering(wifi_list:list, target_SSID:str):
    return [wifi for wifi in wifi_list if wifi['SSID'] == target_SSID]

def main():
    current_os = platform.system()  # 현재 OS 검사
    target_SSID = input()

    wifi_list = get_wifi_list(os_type=current_os)
    pprint(wifi_list, indent=4)

    filtered_wifi_list = target_wifi_filtering(wifi_list=wifi_list, target_SSID=target_SSID)
    print(filtered_wifi_list)


if __name__ == "__main__":
    main()