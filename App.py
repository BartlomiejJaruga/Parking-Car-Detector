import cv2
import random
import string
from CarDetector import findCars, drawAllLicencePlateNumbers
from FrameData import FrameData


def generate_random_licence_plate():
    """
        Generuje losową polską tablicę rejestracyjną w formacie: LLL NNNN lub LLL NNLL.
    """
    prefixes = [
        "PO",  # Wielkopolska
        "WA",  # Warszawa
        "KR",  # Kraków
        "GD",  # Gdańsk
        "SZ",  # Szczecin
        "LU",  # Lublin
        "EL"   # Łódź
    ]

    prefix = random.choice(prefixes)

    format_type = random.choice(["NNNN", "NNLL"])

    if format_type == "NNNN":
        suffix = "".join(random.choices(string.digits, k=4))
    else:  # Format NNLL
        suffix = "".join(random.choices(string.digits, k=2)) + "".join(random.choices(string.ascii_uppercase, k=2))

    return f"{prefix} {suffix}"



if __name__ == "__main__":
    device = 0
    cap = cv2.VideoCapture(device)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    while not cap.isOpened():
        cap = cv2.VideoCapture(device)
        print("Czekam na video.")
        cv2.waitKey(2000)

    current_detected_cars = 0
    current_licence_plates = []
    unknown_positions = []
    last_frame_data = FrameData()

    while True:
        flag, frame = cap.read()
        if flag:
            # ================== GŁÓWNA FUNCKJA PROGRAMU ===================
            new_frame_with_rectangles, new_frame_car_positions = findCars(frame)

            current_detected_cars = len(new_frame_car_positions)

            car_difference_between_frames = current_detected_cars - last_frame_data.detected_cars
            if car_difference_between_frames > 0: # auto wjechało na parking
                newest_licence_plate = generate_random_licence_plate()  # [!] w tej linijce pobrać rejestracje z bazy [!]
                current_licence_plates.append(newest_licence_plate)

            elif car_difference_between_frames < 0: # auto wyjechało z parkingu
                pass
            else: # brak zmian w ilości aut na parkingu
                pass

            cv2.imshow("cars", new_frame_with_rectangles)
        if cv2.waitKey(1) == 27: # ESC
            cv2.destroyAllWindows()
            break

    cap.release()

