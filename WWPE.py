import subprocess, json, csv, sys 

class wifi:
    """
    A class that represents a WiFi utility.

    Attributes:
        z (int): A counter variable.

    Methods:
        run_cmd(cmd) -> list: Runs a command and returns the output as a list of strings.
        analysis(ssid, output): Analyzes the output of a WiFi profile and stores the data.
        get_passwords(): Retrieves WiFi profiles and their passwords.
        export(export_path, detail): Exports WiFi profiles and passwords to a file.

    """

    def __init__(self):
        self.z = 0

    def run_cmd(self, cmd) -> list:
        """
        Runs a command and returns the output as a list of strings.

        Args:
            cmd (str): The command to run.

        Returns:
            list: The output of the command as a list of strings.

        """
        return subprocess.check_output(cmd, shell=True).decode('utf-8').splitlines()

    def analysis(self, ssid, output):
        """
        Analyzes the output of a WiFi profile and stores the data.

        Args:
            ssid (str): The SSID of the WiFi profile.
            output (list): The output of the command to retrieve the WiFi profile details.

        """
        data = {}
        for i in output[8:]:
            if ":" in i:
                key, value = i.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key in data:
                    old_value = data[key]
                    if type(old_value) == list:
                        old_value.append(value)
                        data[key] = old_value
                    else:
                        data[key] = [old_value, value]
                else:
                    data[key] = value
        self.long_dict[self.z] = data
        try:
            _key = data["Key Content"]
        except:
            _key = None
        self.short_dict[self.z] = {"SSID": ssid, "Password": _key}

    def get_passwords(self):
        """
        Retrieves WiFi profiles and their passwords.

        Returns:
            wifi: The current instance of the wifi class.

        """
        self.long_dict = {}
        self.short_dict = {}
        output = self.run_cmd("netsh wlan show profile")
        self.z = 0
        for line in output:
            ssid = line.split(':')[1] if 'All User Profile' in line else None
            if ssid:
                cmd = 'netsh wlan show profile "%s" key=clear' % ssid.strip()
                self.analysis(ssid, self.run_cmd(cmd))
                self.z += 1
        return self
    
    def show_passwords(self,detail=False):
        """
        Show WiFi profiles and passwords.

        Args:
            detail (bool): Whether to show detailed information or not. Default is False.

        Returns:
            wifi: The current instance of the wifi class.
        """
        if detail:
            print(self.long_dict)
        else:
            print(self.short_dict)
        return self


    def export(self, export_path="export.txt", detail=False):
        """
        Exports WiFi profiles and passwords to a file.

        Args:
            export_path (str): The path of the file to export to. Default is "export.txt".
            detail (bool): Whether to export detailed information or not. Default is False.

        Raises:
            Exception: If detail is not a boolean value.
            Exception: If get_passwords() has not been called before exporting passwords.

        """
        def export_csv():
            # Export as CSV format
            with open(export_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["SSID", "Password"])
                for key, value in exp.items():
                    writer.writerow([value["SSID"].strip(), value["Password"]])

        def export_txt():
            # Export as plain text format
            with open(export_path, 'w') as file:
                for key, value in exp.items():
                    file.write(f"{key}:\n")
                    for k, v in value.items():
                        file.write(f"\t{k}: {v}\n")

        def export_json():
            # Export as JSON format
            with open(export_path, 'w') as file:
                json.dump(exp, file, indent=4)

        def export_xml():
            # Export as XML format
            with open(export_path, 'w') as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('<wifi>\n')
                for key, value in exp.items():
                    file.write(f'\t<ssid name="{value["SSID"].strip()}">\n')
                    for k, v in value.items():
                        try:
                            v = v.strip()
                        except:
                            pass
                        file.write(f'\t\t<{k}>{v}</{k}>\n')
                    file.write('\t</ssid>\n')
                file.write('</wifi>\n')

        func = {
            # "csv": export_csv, need to fix this
            "txt": export_txt,
            "json": export_json,
            "xml": export_xml
        }

        if type(detail) != bool:
            raise Exception("detail should be a boolean value (True or False)")

        if self.z != 0:
            exp = self.long_dict if detail else self.short_dict
        else:
            raise Exception("Before exporting passwords, you need to call get_passwords() first")

        pth = export_path.split(".")[-1]
        if pth in func.keys():
            func[pth]()
            return self
        export_txt()
        return self

class __cli__(wifi):
    """
    Command-line interface for the WiFi Password Utility.

    Args:
        wifi: The base class for WiFi operations.

    Attributes:
        arg_setup (dict): A dictionary containing the setup for each command-line argument.
        instructions (str): A string containing the usage instructions for the utility.
        sys_args (list): A list of command-line arguments passed to the utility.

    Methods:
        __init__(): Initializes the __cli__ class.
        __help__(): Displays the help message.
        extract_params(arg): Extracts the parameters for a given argument.
        filter_args(): Filters and processes the command-line arguments.
        __main__(): Main method to execute the utility based on the provided arguments.
    """

    def __init__(self):
        super().__init__()
        # self.__wifi__ = wifi()
        self.arg_setup = {
            "-h": {"required": False, "parameter": False, "Function": self.__help__},
            "--help": {"required": False, "parameter": False, "Function": self.__help__},
            "-g": {"required": False, "parameter": False, "Function": self.get_passwords},
            "--get": {"required": False, "parameter": False, "Function": self.get_passwords},
            "-e": {"required": False, "parameter": False, "Function": self.export},
            "--export": {"required": False, "parameter": False, "Function": self.export},
            "-p": {"required": False, "parameter": True, "Function": self.__help__},
            "--path": {"required": False, "parameter": True, "Function": self.__help__},
            "-d": {"required": False, "parameter": False, "Function": self.__help__},
            "--detail": {"required": False, "parameter": False, "Function": self.__help__}
        }
        self.instructions = f"""
        {app_description}
        {app_name} v{app_version} - {app_platform}
        Author: {app_author}

        Usage: [python {app_name}] [options]

        Options:
            -h, --help                  Show this help message and exit
            -g, --get       [REQUIRED]  Get WiFi profiles and passwords
            -e, --export    [OPTIONAL]  Export WiFi profiles and passwords
            -p, --path      [OPTIONAL]  Specify the path to export to
            -d, --detail    [OPTIONAL]  Export detailed information

        Examples:
            python {app_name} -g
            python {app_name} -g -e 
            python {app_name} -g -e -d -p export.csv 
        """

        self.sys_args = sys.argv[1:]

    def __help__(self):
        print(self.instructions)

    def extract_params(self, arg):
        try:
            if self.arg_setup[arg]["parameter"] and not self.indexed_args[self.sys_args.index(arg) + 1].startswith("-"):
                if self.sys_args.index(arg) + 1 not in self.used_args:
                    self._args[arg] = self.indexed_args[self.sys_args.index(arg) + 1]
                    self.used_args.append(self.sys_args.index(arg) + 1)
                    return
                raise Exception(f"Argument {arg} already used")

            self._args[arg] = None
            return
        except KeyError:
            raise Exception(f"A value is required for argument: {arg}")

    def filter_args(self):
        self._args = {}
        self.used_args = []
        self.indexed_args = {i: self.sys_args[i] for i in range(len(self.sys_args))}

        try:
            for arg in self.sys_args:
                if arg.startswith("-"):
                    if arg not in self.arg_setup.keys():
                        raise Exception(f"Invalid argument: {arg}")

                    self.extract_params(arg)
        except Exception as e:
            print(e)
            self.__help__()
            exit()

    def __main__(self):
        self.filter_args()

        if self._args == {}:
            print('No arguments provided')
            self.__help__()
            exit()

        if "-d" in self._args or "--detail" in self._args:
            detail = True
        else:
            detail = False

        if "-p" in self._args or "--path" in self._args:
            path = self._args["-p"]
        else:
            path = "export.txt"

        if "-h" in self._args or "--help" in self._args:
            self.arg_setup["-h"]["Function"]()
            return

        if "-g" in self._args or "--get" in self._args:
            self.arg_setup["-g"]["Function"]().show_passwords(detail)


        if "-e" in self._args or "--export" in self._args:
            self.arg_setup["-e"]["Function"](path, detail)

if __name__ == "__main__":
    app_name = "WWPE.py"
    app_version = "1.0.0"
    app_platform = "Windows"
    app_description = "A utility to retrieve WiFi profiles and passwords."
    app_author = "Nesa"
    app_license = "MIT"
    # __wifi__ = wifi()
    __cli__().__main__()

        