
class FrameData:
    """Przechowuje dane odnośnie klatki zapisanej z kamery parkingowej.

    Attributes
    ----------
    detected_cars : int
        przechowuje ilość aut wykrytych na kamerze (domyślnie 0)
    licence_plates_and_positions : dictionary
        jako klucze posiada numer rejestracji -> type(str)
        jako wartość posiada tuple z tuple pozycji x i y oraz flagi updatu pozycji

    Np.:
        detected_cars = 2
        licence_plates_and_positions = {
            "REJ 000001": ((122, 931), 1)
            "REJ 000002": ((541, 677), 0)
        }

    Methods
    -------
    increment_detected_cars
    decrement_detected_cars
    add_licence_plate
    remove_licence_plate
    remove_not_updated_licence_plates
    print_all_licence_plates_and_positions
    set_licence_plate_update_flag
    set_all_licence_plate_update_flag
    """

    def __init__(self):
        self.detected_cars = 0
        self.licence_plates_and_positions = {}

    def increment_detected_cars(self, number: int = 1) -> None:
        self.detected_cars += number

    def decrement_detected_cars(self, number: int = 1) -> None:
        self.detected_cars -= number
        if self.detected_cars < 0:
            self.detected_cars = 0

    def add_licence_plate(self, licence_plate: str, position: tuple) -> None:
        if licence_plate not in self.licence_plates_and_positions:
            self.licence_plates_and_positions[licence_plate] = (position, 1)

    def remove_licence_plate(self, licence_plate: str) -> None:
        if licence_plate in self.licence_plates_and_positions:
            self.licence_plates_and_positions.pop(licence_plate)

    def remove_not_updated_licence_plates(self) -> list[str]:
        removed_licence_plates = []
        for licence_plate, data in self.licence_plates_and_positions.items():
            if data[1] == 0:
                removed_licence_plates.append(licence_plate)

        for licence_plate in removed_licence_plates:
            self.licence_plates_and_positions.pop(licence_plate)
            print("removed: " + str(licence_plate))

        return removed_licence_plates

    def set_licence_plate_position(self, licence_plate: str, new_position: tuple) -> None:
        if licence_plate in self.licence_plates_and_positions:
            self.licence_plates_and_positions[licence_plate] = (new_position, 1)

    def set_licence_plate_update_flag(self, licence_plate: str, flag: int) -> None:
        if licence_plate in self.licence_plates_and_positions:
            position = self.licence_plates_and_positions[licence_plate][0]
            self.licence_plates_and_positions[licence_plate] = (position, flag)

    def set_all_licence_plate_update_flag(self, flag: int) -> None:
        for licence_plate, data in self.licence_plates_and_positions.items():
            position = self.licence_plates_and_positions[licence_plate][0]
            self.licence_plates_and_positions[licence_plate] = (position, flag)

    def print_all_licence_plates_and_positions(self) -> None:
        print("\nLast frame licence plates and positions attached to them:")
        if len(self.licence_plates_and_positions.keys()):
            for licence_plate, data in self.licence_plates_and_positions.items():
                print(str(licence_plate) + ": " + str(data[0]) + ", isUpdated = " + str(data[1]))
        else:
            print("(empty)")

    def lookup_close_position_in_dictionary(self, position: tuple, x_range: int = 50, y_range: int = 50) -> tuple[int, str]:
        """Searches for licence plate with close position to given position.

        :param position: tuple with x and y coordinates of licence plate to lookup in dictionary
        :param x_range: horizontal range of lookup, in pixels (f.e. 40 means range x-40 &lt;= dictionary_x &lt;= x+40)
        :param y_range: vertical range of lookup, in pixels (f.e. 40 means range y-40 &lt;= dictionary_y &lt;= y+40)
        :return: tuple which contains:
            flag if position was found (1) or not found (0);
            string with the licence plate of car close to position given to function
        """
        new_x, new_y = position
        for licence_plate, data in self.licence_plates_and_positions.items():
            old_x, old_y = data[0]
            if (old_x - x_range <= new_x <= old_x + x_range) and (old_y - y_range <= new_y <= old_y + y_range):
                # print(str(position) + " is inside of box of " + str(data[0]))
                return 1, licence_plate
        return 0, "No match found - new car!"

    def lookup_all_positions_in_dictionary(self, positions: tuple[tuple[int, int], ...], x_range: int = 50, y_range: int = 50) -> list[tuple]:
        unknown_positions = []
        for position in positions:
            result, licence_plate = self.lookup_close_position_in_dictionary(position, x_range, y_range)
            if result:
                self.set_licence_plate_position(licence_plate, position)
            else:
                unknown_positions.append(position)

        return unknown_positions

    def get_all_licence_plates_and_their_positions(self) -> tuple[tuple, tuple]:
        licence_plates = []
        positions = []
        for licence_plate, data in self.licence_plates_and_positions.items():
            licence_plates.append(licence_plate)
            positions.append(data[0])
        return tuple(licence_plates), tuple(positions)


if __name__ == "__main__":
    last_frame = FrameData()

    # print(last_frame.detected_cars)
    # last_frame.increment_detected_cars()
    # print(last_frame.detected_cars)
    # last_frame.decrement_detected_cars()
    # print(last_frame.detected_cars)
    # last_frame.increment_detected_cars(2)
    # print(last_frame.detected_cars)
    # last_frame.decrement_detected_cars(3)
    # print(last_frame.detected_cars)

    last_frame.add_licence_plate("PL 6969", (0, 300))
    last_frame.add_licence_plate("EKU 123123", (120, 100))
    last_frame.add_licence_plate("OK CATCH", (111, 555))
    last_frame.print_all_licence_plates_and_positions()

    # last_frame.add_licence_plate("EL 000000", (666, 666))
    # last_frame.print_all_licence_plates_and_positions()

    last_frame.set_all_licence_plate_update_flag(0)
    last_frame.print_all_licence_plates_and_positions()

    new_frame_positions = ((80, 60), (120, 540), (1, 280))
    unknown_positions = last_frame.lookup_all_positions_in_dictionary(new_frame_positions)
    last_frame.print_all_licence_plates_and_positions()
    if len(unknown_positions):
        print(unknown_positions)

    # last_frame.remove_licence_plate("OK CATCH")
    # last_frame.print_all_licence_plates_and_positions()
    #
    # last_frame.set_all_licence_plate_update_flag(0)
    # last_frame.print_all_licence_plates_and_positions()
    #
    # last_frame.remove_not_updated_licence_plates()
    # last_frame.print_all_licence_plates_and_positions()

    print(last_frame.get_all_licence_plates_and_their_positions())
