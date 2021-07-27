# capture only luminescence
import time
import picamera
import picamera.array
import numpy as np

with picamera.PiCamera() as camera:
    camera.resolution = (100, 100)
    time.sleep(2)
    y_data = np.empty((112, 128), dtype=np.uint8)
    try:
        camera.capture(y_data, 'yuv')
    except IOError:
        pass
    y_data = y_data[:100, :100]
    # y_data now contains the Y-plane only

    print(f"luminance array{y_data}")
    print(f"luminance array sum {np.sum(y_data)}")
    np.savetxt('y_data-luminance.csv', y_data, delimiter=',')


# capture whole yuv
# import time
# import picamera
# import picamera.array

# with picamera.PiCamera() as camera:
#     with picamera.array.PiYUVArray(camera) as stream:
#         camera.resolution = (100, 100)
#         camera.start_preview()
#         time.sleep(2)
#         camera.capture(stream, 'yuv')
#         # Show size of YUV data
#         print(stream.array.shape)
#         # Show size of RGB converted data
#         print(stream.rgb_array.shape)