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
        mat = rel.get_pose_matrix()
        if mat is not None:
            rows = ["  ".join("%.4f" % mat[r][c] for c in range(4)) for r in range(3)]
            print("\r" + " | ".join(rows), end="")
        sleep_time = interval - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
