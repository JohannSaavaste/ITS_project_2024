from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import Camera, Lidar
import cv2
import numpy as np

def main():
    set_up_simple_logging()

    beamng_home = r'C:\\ITS\\BeamNG.tech.v0.32.5.0'
    user_folder = r'C:\\Users\\kaspe\\AppData\\Local\\BeamNG.drive\\0.32'

    bng = BeamNGpy('localhost', 64256, home=beamng_home, user=user_folder)
    bng.open(launch=True)

    scenario = Scenario('smallgrid', 'AI_Car_Test')

    mycar = Vehicle('mycar', model='etk800', license='ITS', color='Red')
    scenario.add_vehicle(mycar, pos=(0, 0, 0), rot_quat=(0, 0, 0, 1))

    ai_vehicle = Vehicle('ai_vehicle', model='etk800', license='AI_CAR', color='Blue')
    scenario.add_vehicle(ai_vehicle, pos=(0, -10, 0), rot_quat=(0, 0, 0, 1))  # Position it 10 meters in front

    scenario.make(bng)
    bng.settings.set_deterministic(60)
    bng.scenario.load(scenario)
    bng.scenario.start()

    # Create camera and attach it to vehicle
    camera = Camera(
        name='camera1',
        bng=bng,
        vehicle=mycar,
        is_streaming=True)


    lidar = Lidar(
        "lidar1",
        bng,
        mycar,
        requested_update_time=0.1,
        is_using_shared_memory=False,
        vertical_angle=90,
        horizontal_angle=120,
        vertical_resolution=64,
        pos=(0, -2, 1),
        dir=(0, 0, 0),  
        is_360_mode=False,  # [DEMO: DEFAULT - 360 MODE].  Uses shared memory.
    )


    mycar.ai.set_mode('disabled') 
    ai_vehicle.ai.set_mode('span')

    try:
        while True:
            bng.control.step(10)

            lidar_data = lidar.poll()
            print(lidar_data['pointCloud'].shape)

            #if lidar_data is not None:
            #                # Process the LiDAR data here
            #                points = np.array(lidar_data['points'])
            #                print(f"LiDAR points: {points.shape}")

            #camera_data = camera.poll()

            '''if camera_data is not None and 'depth' in camera_data:
                # Convert the raw data into an image format
                img = np.array(camera_data['depth'], dtype=np.uint8)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Display the image
                cv2.imshow('Camera View', img)
                
                # Break on key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break'''
    except KeyboardInterrupt:
        print("Simulation stopped by the user.")
    finally:
        bng.close()

if __name__ == '__main__':
    main()