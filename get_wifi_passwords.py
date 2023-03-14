import subprocess
import csv

class wifi_passwords:
    def __init__(self):
        self.cmd = "netsh wlan show profile"

    def get_passwords(self,export):
        if type(export) == bool:
            pass
        else:
            print("Please set export to True or False, export = True or export = False")
            return
        ssid_passwords = []
        output = subprocess.check_output(self.cmd, shell=True)
        output = output.decode('utf-8')
        output = output.splitlines()
        for line in output:
            if 'All User Profile' in line:
                ssid = line.split(':')[1]
                ssid = ssid.strip()
                cmd = "netsh wlan show profile %s key=clear" % ssid
                output = subprocess.check_output(cmd, shell=True)
                output = output.decode('utf-8')
                output = output.splitlines()
                for line in output:
                    if 'Key Content' in line:
                        password = line.split(':')[1]
                        password = password.strip()
                        ssid_passwords.append((ssid, password))
                    else:
                        pass
        if export == True:
            wifi_passwords.export_passwords(self,ssid_passwords)
        else:
            pass
        return ssid_passwords              
       
    def export_passwords(self,ss_pwd):
        print("passwords exported to csv file")
        with open('wifi_passwords.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["SSID", "Password"])
            for line in ss_pwd:
                writer.writerow(line)
        pass

password = wifi_passwords().get_passwords(export=True)

