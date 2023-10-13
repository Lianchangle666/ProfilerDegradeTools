from mecheye.profiler import Profiler
from mecheye.area_scan_3d_camera import Camera


class Discover(object):
    def __init__(self):
        self.profiler = Profiler()
        self.camera = Camera()

    def find_profiler(self):
        profiler_info = self.profiler.discover_profilers()
        return [[info.model, info.ip_address, info.firmware_version.to_string()] for info in profiler_info]

    def find_camera(self):
        camera_info = self.camera.discover_cameras()
        return [[info.model, info.ip_address, info.firmware_version.to_string()] for info in camera_info]


if __name__ == "__main__":
    profiler = Discover()
    print(profiler.find_profiler())
    print(profiler.find_camera())