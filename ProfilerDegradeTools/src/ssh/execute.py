import os
import time
from src.ssh.link import LinkSSH


class ExecuteScript(object):
    def __init__(self):
        print(os.getcwd())
        self.windows_controller = os.getcwd() + r"\bin\ProfilerSplitType\LNXInstall_8000C_2_0_1.run"
        self.windows_path_8030 = os.getcwd() + r"\bin\ProfilerSplitType\LNXInstall_8030_2_1_2.run"
        self.windows_path_8300 = os.getcwd() + r"\bin\ProfilerSplitType\LNXInstall_8300_3_0_2.run"
        self.windows_path_8080 = os.getcwd() + r"\bin\ProfilerSplitType\LNXInstall_8080_4_0_1.run"
        self.windows_path_verision_map = os.getcwd() + r"\bin\ProfilerSplitType\version_map.json"
        self.windows_path_profiler_firmware = os.getcwd() + r"\bin\ProfilerSplitType\mmind_eye_Zynq_Ubuntu18"

        self.linux_controller_split_type = r"/home/ubuntu/AutoAPI/LNXInstall_8000C_2_0_1.run"
        self.linux_path_8030 = "/home/ubuntu/AutoAPI/LNXInstall_8030_2_1_2.run"
        self.linux_path_8300 = "/home/ubuntu/AutoAPI/LNXInstall_8300_3_0_2.run"
        self.linux_path_8080 = "/home/ubuntu/AutoAPI/LNXInstall_8080_4_0_1.run"
        self.linux_path_version_map = r"/home/ubuntu/Server/resource_runtime/version_map.json"
        self.linux_path_profiler_firmware = "/home/ubuntu/Server/mmind_eye"

    def connect_mecheye(self, ipaddress, username="ubuntu", password="ubuntu", retry="ubuntu"):
        print("ipaddress: {}, username: {}, password: {}".format(ipaddress, username, password))
        self.link = LinkSSH(hostname=ipaddress, username=username, password=password, retry=retry)
        self.link.connect()
        self.link.execute_command("sudo mkdir AutoAPI")
        self.link.execute_command("sudo chmod 777 AutoAPI")

    def stop_mmind(self):
        self.link.execute_command("sudo systemctl stop mmind")

    def start_mmind(self):
        self.link.execute_command("sudo systemctl start mmind")

    def reboot(self):
        print("profiler reboot...")
        self.link.execute_command("sudo reboot")

    def update_controller_run_package(self):
        print("update controller run package...")

        self.link.update_file(self.windows_controller, self.linux_controller_split_type)
        # /home/ubuntu/AutoAPI/LNXInstall_8000C_2_0_1.run
        self.link.execute_command("sudo chmod 777 " + self.linux_controller_split_type)
        self.link.execute_command("sudo ." + self.linux_controller_split_type)
        time.sleep(2)

    def update_run_package(self, mecheye_type_name):
        print("update {} run package...".format(mecheye_type_name))

        if mecheye_type_name == "Mech-Eye LNX 8300":
            self.link.execute_command("sudo chmod 777 " + self.linux_path_8300)
            self.link.update_file(self.windows_path_8300, self.linux_path_8300)
            self.link.execute_command("sudo chmod 777 " + self.linux_path_8300)
            self.link.execute_command("sudo ." + self.linux_path_8300)

        elif mecheye_type_name == "Mech-Eye LNX 8080":
            self.link.execute_command("sudo chmod 777 " + self.linux_path_8080)
            self.link.update_file(self.windows_path_8080, self.linux_path_8080)
            self.link.execute_command("sudo chmod 777 " + self.linux_path_8080)
            self.link.execute_command("sudo ." + self.linux_path_8080)

        elif mecheye_type_name == "Mech-Eye LNX 8030":
            self.link.execute_command("sudo chmod 777 " + self.linux_path_8300)

            self.link.update_file(self.windows_path_8030, self.linux_path_8030)
            self.link.execute_command("sudo chmod 777 " + self.linux_path_8030)
            self.link.execute_command("sudo ." + self.linux_path_8030)

        else:
            pass
        time.sleep(2)

    def update_version_map(self):
        print("update version map...")

        self.link.execute_command("sudo chmod 777 " + self.linux_path_version_map)
        self.link.update_file(self.windows_path_verision_map, self.linux_path_version_map)
        self.link.execute_command("sudo chmod 777 " + self.linux_path_version_map)

    def update_firmware(self, mecheye_type_name):
        print("update firmware...")

        if mecheye_type_name in ["Mech-Eye LNX 8030", "Mech-Eye LNX 8080", "Mech-Eye LNX 8300"]:
            self.link.update_file(self.windows_path_profiler_firmware, self.linux_path_profiler_firmware)
            self.link.execute_command("sudo chmod 777 " + self.linux_path_profiler_firmware)

        else:
            pass


if __name__ == "__main__":
    es = ExecuteScript()
    es.connect_mecheye("192.168.20.199", "ubuntu", password="ubuntu", retry="ubuntu")
    es.stop_mmind()
    es.update_firmware("Mech-Eye LNX 8080")
    es.update_version_map()
    es.update_run_package("Mech-Eye LNX 8080")
    es.update_controller_run_package()
    es.reboot()
