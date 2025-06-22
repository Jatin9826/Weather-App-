import tkinter as tk
from tkinter import messagebox
import requests

# API utility
def geocode_city(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    res = requests.get(url).json()
    if not res.get("results"):
        return None, None
    loc = res["results"][0]
    return loc["latitude"], loc["longitude"]

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    res = requests.get(url).json()
    cw = res.get("current_weather")
    if not cw:
        return None
    return {
        "temperature": cw["temperature"],
        "windspeed": cw["windspeed"],
        "weathercode": cw["weathercode"]
    }

def describe_weather(code):
    mapping = {
        0: "☀️ Clear sky", 1: "🌤️ Mainly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast",
        45: "🌫️ Fog", 48: "🌫️ Rime fog", 51: "🌦️ Light drizzle",
        61: "🌧️ Slight rain", 80: "🌧️ Slight rain showers"
    }
    return mapping.get(code, "🌥️ Unknown")

# Action on button click
def show_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    lat, lon = geocode_city(city)
    if lat is None:
        messagebox.showerror("City Not Found", f"Could not find city: {city}")
        return

    data = get_weather(lat, lon)
    if not data:
        messagebox.showerror("Weather Error", "Could not retrieve weather data.")
        return

    weather = describe_weather(data['weathercode'])
    result = (
        f"📍 City: {city.title()}\n"
        f"🌡️ Temp: {data['temperature']} °C\n"
        f"💨 Wind: {data['windspeed']} km/h\n"
        f"{weather}"
    )
    result_label.config(text=result)

# GUI Setup
root = tk.Tk()
root.title("🌤️ Weather App")
root.geometry("500x400")
root.configure(bg="#5072E1")  # Dark background

# Title Label
tk.Label(root, text="☁️ Real-Time Weather", font=("Segoe UI", 20, "bold"), fg="white", bg="#1E1E2F").pack(pady=20)

# City input
input_frame = tk.Frame(root, bg="#3AE34B")
input_frame.pack(pady=10)

tk.Label(input_frame, text="🔎 City:", font=("Segoe UI", 14), bg="#1E1E2F", fg="#FFFFFF").grid(row=0, column=0, padx=5)
city_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=25, bg="#EEEEEE")
city_entry.grid(row=0, column=1, padx=5)

# Button
def on_enter(e):
    weather_btn.config(bg="#1abc9c")

def on_leave(e):
    weather_btn.config(bg="#16a085")

weather_btn = tk.Button(root, text="Get Weather", font=("Segoe UI", 13, "bold"),
                        bg="#16a085", fg="white", padx=20, pady=6, command=show_weather, relief="raised", bd=4)
weather_btn.pack(pady=15)
weather_btn.bind("<Enter>", on_enter)
weather_btn.bind("<Leave>", on_leave)

# Result display
result_label = tk.Label(root, text="", font=("Segoe UI", 13), bg="#1E1E2F", fg="#ECF0F1", justify="left", wraplength=400)
result_label.pack(pady=25)

# Footer
tk.Label(root, text="🔗 @Jatin Kumar", font=("Segoe UI", 9), bg="#D3B9E6", fg="#95a5a6").pack(side="bottom", pady=10)

root.mainloop()
