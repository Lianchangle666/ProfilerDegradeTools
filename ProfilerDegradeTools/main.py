import time
from src.api.discover import Discover
from src.ssh.execute import ExecuteScript


def write_log(test):
    with open("update.log", "a+", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S [D]: ", time.localtime()) + test + "\n")


profiler = Discover()
profilers_info = profiler.find_profiler()
for n, profiler_info in enumerate(profilers_info):
    print("\nProfilerNo: {}".format(n))
    print("=" * 40)
    print("Model Name: {}\nIPAddress : {}\nFirmware V: {}".format(profiler_info[0], profiler_info[1], profiler_info[2]))
# print(profiler.find_camera())


while True:
    index_list = input("Please input profiler No.(such as 1,2,3,4):")
    for index in index_list.split(','):
        if not (index.isdigit() and int(index) < len(profilers_info)):
            print("Invalid input, ", end="")

        else:
            es = ExecuteScript()
            if profilers_info[int(index)][0] in ["Mech-Eye LNX 8030", "Mech-Eye LNX 8080", "Mech-Eye LNX 8300"]:
                write_log(",".join(profilers_info[int(index)]))
                es.connect_mecheye(profilers_info[int(index)][1])
                es.stop_mmind()
                es.update_firmware(profilers_info[int(index)][0])
                es.update_version_map()
                es.update_run_package(profilers_info[int(index)][0])
                es.update_controller_run_package()
                es.reboot()
    break


input("Enter any key to quit")