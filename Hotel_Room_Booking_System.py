import tkinter as tk
from tkinter import messagebox

class Hotel:
    def __init__(self):
        self.floors = {i: [True] * (10 if i < 10 else 7) for i in range(1, 11)}  # True means available

    def find_best_rooms(self, num_rooms):
        for floor, rooms in self.floors.items():
            available_rooms = [i+1 for i, r in enumerate(rooms) if r]
            if len(available_rooms) >= num_rooms:
                return [(floor, available_rooms[:num_rooms])]

        best_combination = []
        min_travel_time = float("inf")

        for start_floor in range(1, 11):
            selected_rooms = []
            travel_time = 0
            remaining = num_rooms

            for floor in range(start_floor, 11):
                available_rooms = [i+1 for i, r in enumerate(self.floors[floor]) if r]
                if available_rooms:
                    taken = available_rooms[:min(remaining, len(available_rooms))]
                    selected_rooms.append((floor, taken))
                    remaining -= len(taken)
                    if remaining == 0:
                        break
                    travel_time += 2  # Moving to next floor

            if remaining == 0 and travel_time < min_travel_time:
                best_combination = selected_rooms
                min_travel_time = travel_time

        return best_combination if best_combination else None

    def book_rooms(self, num_rooms):
        best_rooms = self.find_best_rooms(num_rooms)
        if best_rooms:
            for floor, rooms in best_rooms:
                for room in rooms:
                    self.floors[floor][room-1] = False  # Mark as booked
            return best_rooms
        return "Not enough rooms available."

class HotelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Room Booking")
        self.hotel = Hotel()

        tk.Label(root, text="Enter number of rooms (1-5):").pack(pady=5)
        self.room_entry = tk.Entry(root)
        self.room_entry.pack(pady=5)

        self.book_button = tk.Button(root, text="Book Rooms", command=self.book_rooms)
        self.book_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", fg="blue")
        self.result_label.pack(pady=5)

        self.visualize_hotel()

    def book_rooms(self):
        try:
            num_rooms = int(self.room_entry.get())
            if num_rooms < 1 or num_rooms > 5:
                messagebox.showerror("Error", "You can only book 1 to 5 rooms.")
                return

            result = self.hotel.book_rooms(num_rooms)
            if isinstance(result, str):
                self.result_label.config(text=result, fg="red")
            else:
                booked_rooms = ", ".join([f"Floor {f}, Rooms {r}" for f, r in result])
                self.result_label.config(text=f"Booked: {booked_rooms}", fg="green")
                self.update_visualization()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def visualize_hotel(self):
        self.canvas = tk.Canvas(self.root, width=300, height=500, bg="white")
        self.canvas.pack(pady=10)
        self.draw_hotel()

    def draw_hotel(self):
        self.canvas.delete("all")
        y_offset = 20
        for floor in range(10, 0, -1):
            num_rooms = 10 if floor < 10 else 7
            for room in range(num_rooms):
                x = 30 + room * 25
                y = y_offset + (10 - floor) * 40
                color = "green" if self.hotel.floors[floor][room] else "red"
                self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=color)
                self.canvas.create_text(x + 10, y + 10, text=f"{floor}{room+1}", font=("Arial", 7))

    def update_visualization(self):
        self.draw_hotel()

# Run the GUI
root = tk.Tk()
app = HotelGUI(root)
root.mainloop()
