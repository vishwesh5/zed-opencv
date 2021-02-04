import sys
import numpy as np
import pyzed.sl as sl
import ogl_viewer.viewer as gl
#import cv2

def main() :

    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.depth_mode = sl.DEPTH_MODE.ULTRA
    init.coordinate_units = sl.UNIT.METER
    init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    # Open the camera
    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS :
        print(repr(err))
        zed.close()
        exit(1)

    # Display help in console
    print_help()
    
    res = sl.Resolution()
    res.width = 720
    res.height = 404
    point_cloud = sl.Mat(res.width,res.height,sl.MAT_TYPE.F32_C4,sl.MEM.CPU)
    image_zed = sl.Mat(res.width, res.height, sl.MAT_TYPE.U8_C4)
    
    camera_model = zed.get_camera_information().camera_model
    # Create OpenGL viewer
    viewer = gl.GLViewer()
    viewer.init(len(sys.argv), sys.argv, camera_model, res)
    
    while viewer.is_available():
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
            viewer.updateData(point_cloud)
    viewer.exit()
    zed.close()
#     key = ' '
#     while key != 113 :
#         err = zed.grab()
#         if err == sl.ERROR_CODE.SUCCESS :
#             zed.retrieve_image(image_zed, sl.VIEW.LEFT, sl.MEM.CPU, res)
#             zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU, res)

#             # To recover data from sl.Mat to use it with opencv, use the get_data() method
#             # It returns a numpy array that can be used as a matrix with opencv
#             image_ocv = image_zed.get_data()

#             cv2.imshow("Image", image_ocv)

#             key = cv2.waitKey(10)

#             process_key_event(zed, key)

#     cv2.destroyAllWindows()
#     zed.close()

#     print("\nFINISH")

if __name__ == "__main__":
    main()
