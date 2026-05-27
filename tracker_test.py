import triad_openvr
import time
import sys
import msvcrt

# Position of tracker_1 (reference) in your world frame (metres, z = vertical)
p_ref = [0.0, 0.0, 0.0]

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

rel = triad_openvr.RelativeTrackerSystem(
    tracker_ref=v.devices["tracker_1"],
    tracker_moving=v.devices["tracker_2"],
    p_ref=p_ref
)
rel.calibrate()

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

if interval:
    print("Press Q to stop.")
    while True:
        if msvcrt.kbhit() and msvcrt.getwch().lower() == "q":
            break
        start = time.time()
        ref_pose = rel.tracker_ref.get_pose_euler()
        mat = rel.get_pose_matrix()
        if ref_pose is not None and mat is not None:
            rx, ry, rz, ryaw, rpitch, rroll = ref_pose
            x, y, z, yaw, pitch, roll = triad_openvr.convert_to_euler(mat)
            print("\r[ref]  x=%.4f y=%.4f z=%.4f  yaw=%.2f pitch=%.2f roll=%.2f    "
                  "[moving]  x=%.4f y=%.4f z=%.4f  yaw=%.2f pitch=%.2f roll=%.2f"
                  % (rx, ry, rz, ryaw, rpitch, rroll, x, y, z, yaw, pitch, roll), end="")
        sleep_time = interval - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
