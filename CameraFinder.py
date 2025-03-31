import cv2

def find_cameras():
    """
    Funkcja wykrywa dostępne kamery podłączone do komputera.
    """
    available_cameras = []
    for i in range(10):
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

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cap in caps.values():
        cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    cameras = find_cameras()
    if cameras:
        print(f"Znalezione kamery: {cameras}")
        show_cameras(cameras)
    else:
        print("Nie znaleziono żadnych kamer.")

