import cv2
from skimage import filters, io, color
import matplotlib.pyplot as plt
import numpy as np
from database import database_operations

def find_cameras():
    """
    Funkcja wykrywa dostępne kamery podłączone do komputera.
    """
    available_cameras = []
    for i in range(10):  # Zakładamy, że może być maksymalnie 10 kamer.
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras


def show_cameras(cameras):
    """
    Funkcja wyświetla obraz z podłączonych kamer.
    """
    caps = {cam_id: cv2.VideoCapture(cam_id) for cam_id in cameras}

    while True:
        for cam_id, cap in caps.items():
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f'Camera {cam_id}', frame)

        # Wyjście z programu po wciśnięciu klawisza 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cap in caps.values():
        cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # cameras = find_cameras()
    # if cameras:
    #     print(f"Znalezione kamery: {cameras}")
    #     show_cameras(cameras)
    # else:
    #     print("Nie znaleziono żadnych kamer.")
    database_operations.path_to_database = r'./database/cyber_parking.db'
    # database_operations.add_sample_employee()
    database_operations.display_entries(database_operations.TABLE_NAMES[0])

    database_operations.get_newest_car_licence_plate()

    chuj = database_operations.Event("PL 6969", "spotted")

    database_operations.add_event(chuj)

    database_operations.display_entries(database_operations.TABLE_NAMES[3])

    database_operations.clear_database()



    # image = io.imread("rejestracja3.webp")
    # if len(image.shape) == 3:
    #     image = color.rgb2gray(image)
    #
    # filters.try_all_threshold(image)
    # plt.show()

