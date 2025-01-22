import os
import time
import json
import turtle
import gmplot
import webbrowser
import googlemaps
import tkinter as tk
from tkinter import messagebox

API_KEY = "AIzaSyDHG4BxBfhyhGdVAcwIoABp4F-lG272Kjo"  # Replace with your actual Google Maps API key
gmaps = googlemaps.Client(key=API_KEY)

def geocode(location_name):
    try:
        geocode_result = gmaps.geocode(location_name)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None
    except Exception as e:
        print(f"Error geocoding location '{location_name}': {e}")
        return None

def draw_opening_animation():
    screen = turtle.Screen()
    screen.title("Campus Navigation Helper")
    screen.bgcolor("white")
    screen.setup(width=600, height=600)

    pen = turtle.Turtle()
    pen.speed(3)
    pen.hideturtle()

    # Draw a compass-like circle
    pen.penup()
    pen.goto(0, -150)
    pen.pendown()
    pen.pensize(3)
    pen.color("blue")
    pen.circle(150)

    # Draw directional lines
    directions = ["N", "E", "S", "W"]
    angle = 90
    pen.color("black")
    for direction in directions:
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(angle)
        pen.forward(150)
        pen.write(direction, align="center", font=("Arial", 16, "bold"))
        pen.backward(150)
        angle -= 90

    # Draw a navigation arrow
    pen.penup()
    pen.goto(0, -20)
    pen.setheading(60)
    pen.pendown()
    pen.color("red")
    pen.begin_fill()
    for _ in range(3):
        pen.forward(40)
        pen.left(120)
    pen.end_fill()

    # Display welcome message
    pen.penup()
    pen.goto(0, -200)
    pen.color("green")
    pen.write("Welcome to Campus Navigation Helper!", align="center", font=("Arial", 18, "bold"))

    # Pause for 3 seconds before closing animation
    time.sleep(3)
    screen.bye()

class CampusNavigationHelper:
    def __init__(self):
        self.locations = {}
        self.transport_updates = []
        self.crowded_areas = []
        self.weather_data = "Clear"
        self.load_data()

    def save_data(self):
        with open("campus_data.json", "w") as file:
            json.dump({
                "locations": self.locations,
                "transport_updates": self.transport_updates,
                "crowded_areas": self.crowded_areas
            }, file)

    def load_data(self):
        if os.path.exists("campus_data.json"):
            with open("campus_data.json", "r") as file:
                data = json.load(file)
                self.locations = data.get("locations", {})
                self.transport_updates = data.get("transport_updates", [])
                self.crowded_areas = data.get("crowded_areas", [])

    def display_menu(self):
        root = tk.Tk()
        root.title("Campus Navigation Helper")
        root.geometry("600x400")

        def display_home(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()
            tk.Label(content_frame, text="Welcome to Campus Navigation Helper", font=("Helvetica", 16)).pack(pady=20)

        def display_save_location(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Save Location", font=("Helvetica", 14)).pack(pady=10)
            tk.Label(content_frame, text="Location Name:").pack()
            location_entry = tk.Entry(content_frame, width=30)
            location_entry.pack()

            tk.Label(content_frame, text="Description:").pack()
            description_entry = tk.Entry(content_frame, width=30)
            description_entry.pack()

            def save_location(*args, **kwargs):
                location_name = location_entry.get()
                description = description_entry.get()
                if location_name and description:
                    self.locations[location_name] = description
                    messagebox.showinfo("Success", f"Location '{location_name}' saved successfully.")
                    location_entry.delete(0, tk.END)
                    description_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")

            tk.Button(content_frame, text="Save", command=save_location).pack(pady=10)

        def display_transport_updates(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Transport Updates", font=("Helvetica", 14)).pack(pady=10)

            def open_transport_updates():
                webbrowser.open("http://bustrackerutem.atwebpages.com/")

            tk.Button(content_frame, text="View Transport Updates", command=open_transport_updates, width=20).pack(pady=10)

        def display_heatmap(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Heatmap of Crowded Areas", font=("Helvetica", 14)).pack(pady=10)

            gmap = gmplot.GoogleMapPlotter(2.310405, 102.314717, 13)
            crowded_areas = kwargs.get("crowded_areas", [
                (2.310405, 102.314717),
                (2.311048, 102.314438),
                (2.310281, 102.314223),
            ])
            latitudes, longitudes = zip(*crowded_areas)
            gmap.heatmap(latitudes, longitudes)
            heatmap_file = "heatmap.html"
            gmap.draw(heatmap_file)
            webbrowser.open(heatmap_file)
            tk.Label(content_frame, text="Heatmap generated. Opening in browser...", font=("Helvetica", 12)).pack(pady=10)

        def display_simulate_route(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Simulate Route with Stop", font=("Helvetica", 14)).pack(pady=10)

            tk.Label(content_frame, text="Starting Location:").pack()
            start_var = tk.StringVar()
            start_entry = tk.Entry(content_frame, textvariable=start_var, width=30)
            start_entry.pack(pady=5)

            tk.Label(content_frame, text="Stop Location:").pack()
            stop_var = tk.StringVar()
            stop_entry = tk.Entry(content_frame, textvariable=stop_var, width=30)
            stop_entry.pack(pady=5)

            tk.Label(content_frame, text="Final Destination:").pack()
            end_var = tk.StringVar()
            end_entry = tk.Entry(content_frame, textvariable=end_var, width=30)
            end_entry.pack(pady=5)

            def plot_route():
                start = start_var.get().strip()
                stop = stop_var.get().strip()
                end = end_var.get().strip()

                if start and stop and end:
                    # Google Maps Directions URL with a stop
                    google_maps_url = (
                        f"https://www.google.com/maps/dir/?api=1"
                        f"&origin={start}"
                        f"&destination={end}"
                        f"&waypoints={stop}"
                        f"&travelmode=walking"
                    )
                    webbrowser.open(google_maps_url)
                    tk.Label(content_frame, text="Route with stop opened in Google Maps!", fg="green").pack(pady=10)
                else:
                    messagebox.showerror("Error", "Please enter the starting location, stop, and destination.")

            tk.Button(content_frame, text="Simulate Route", command=plot_route).pack(pady=20)
            tk.Label(content_frame, text="Enter the starting location, stop, and final destination.", fg="gray").pack(pady=10)


        # Sidebar for navigation
        sidebar = tk.Frame(root, width=200, bg="gray")
        sidebar.pack(side="left", fill="y")

        tk.Button(sidebar, text="Home", command=lambda: display_home(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Save Location", command=lambda: display_save_location(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Transport Updates", command=lambda: display_transport_updates(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Heatmap", command=lambda: display_heatmap(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Simulate Route", command=lambda: display_simulate_route(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Exit", command=lambda: (self.save_data(), root.quit()), width=20).pack(pady=10)

        content_frame = tk.Frame(root, bg="white")
        content_frame.pack(side="right", fill="both", expand=True)

        display_home()
        root.mainloop()

def main():
    draw_opening_animation()
    app = CampusNavigationHelper()
    app.display_menu()

if __name__ == "__main__":
    main()

