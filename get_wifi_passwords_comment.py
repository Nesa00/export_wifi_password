import subprocess
import csv

class wifi_passwords:
    def __init__(self):
        self.cmd = "netsh wlan show profile"  # set the command to show wifi profiles

    def get_passwords(self,export):
        if type(export) == bool:  # check if export is a boolean
            pass
        else:
            print("Please set export to True or False, export = True or export = False")  # print error message if export is not a boolean
            return
        ssid_passwords = []
        output = subprocess.check_output(self.cmd, shell=True)  # run the command to show wifi profiles
        output = output.decode('utf-8')  # decode the output to string
        output = output.splitlines()  # split the output by line
        for line in output:
            if 'All User Profile' in line:  # find wifi profiles in the output
                ssid = line.split(':')[1]  # extract the name of the wifi profile
                ssid = ssid.strip()  # remove any whitespace from the profile name
                cmd = "netsh wlan show profile %s key=clear" % ssid  # set the command to show the password for the wifi profile
                output = subprocess.check_output(cmd, shell=True)  # run the command to show the wifi password
                output = output.decode('utf-8')  # decode the output to string
                output = output.splitlines()  # split the output by line
                for line in output:
                    if 'Key Content' in line:  # find the line with the wifi password
                        password = line.split(':')[1]  # extract the wifi password
                        password = password.strip()  # remove any whitespace from the password
                        ssid_passwords.append((ssid, password))  # add the wifi profile name and password to the ssid_passwords list
                    else:
                        pass
        if export == True:  # if export is set to True
            wifi_passwords.export_passwords(self,ssid_passwords)  # call the export_passwords method to export the wifi passwords to a CSV file
        else:
            pass
        return ssid_passwords  # return the list of wifi profile names and passwords
       
    def export_passwords(self,ss_pwd):
        print("passwords exported to csv file")
        with open('wifi_passwords.csv', 'w', newline='') as file:  # create a new CSV file to store the wifi passwords
            writer = csv.writer(file)  # create a CSV writer object
            writer.writerow(["SSID", "Password"])  # write the header row for the CSV file
            for line in ss_pwd:
                writer.writerow(line)  # write each wifi profile name and password to the CSV file
        pass

password = wifi_passwords().get_passwords(export=True)  # call the get_passwords method to get the wifi passwords and export them to a CSV file
