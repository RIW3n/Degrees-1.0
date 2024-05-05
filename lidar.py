
import matplotlib.pyplot as plt
from rplidar import RPLidar
import math

lidar = RPLidar('COM9')
lidar.clean_input()
lidar_data = []


try:
    
    fig, ax = plt.subplots()

    for i, scan in enumerate(lidar.iter_scans()):
        # print('%d: Got %d measurements' % (i, len(scan)))
        
        

        for measurement in scan:
            angle_degrees = math.degrees(math.radians(measurement[1]))
            distance = measurement[2]
            x = distance * math.cos(math.radians(angle_degrees))
            y = distance * math.sin(math.radians(angle_degrees))
            
            # lidar_data.append((x, y))
            # # print(lidar_data)

           

        
            # x_values, y_values = zip(*lidar_data)
            
            
            
            ax.scatter(x, y, marker='o', s=5)  

        
            ax.set_xlim(-10000, 10000)
            ax.set_ylim(-10000, 10000)

            plt.pause(0.01)
            lidar.clean_input()
           
            plt.show
        
        

except :
    lidar.clean_input()

finally:

   
    lidar.clean_input()
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    plt.show()

