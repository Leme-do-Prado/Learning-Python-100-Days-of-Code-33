import requests
from datetime import datetime
import smtplib

sp_latitude = -23.550520
sp_longitude = -46.633308

email_address = input("What's your e-mail address? Type here: ")
password = input("What's your e-mail password? Type here: ")

params = {
    "lat": sp_latitude,
    "lng": sp_longitude,
    "formatted": 0
}

response = requests.get("https://api.sunrise-sunset.org/json", params=params)
response.raise_for_status()
data = response.json()
sunset_time = int(data["results"]["sunset"].split("T")[1].split(":")[0])
sunrise_time = int(data["results"]["sunrise"].split("T")[1].split(":")[0])

current_time = datetime.utcnow().hour

response_iss = requests.get("http://api.open-notify.org/iss-now.json")
response_iss.raise_for_status()
iss_data = response_iss.json()
iss_latitude = float(iss_data["iss_position"]["latitude"])
iss_longitude = float(iss_data["iss_position"]["longitude"])

if sunset_time < current_time or current_time < sunrise_time:
    part_of_the_day = "Nighttime"
else:
    part_of_the_day = "Daytime"

print(f"Sunset time is {sunset_time}!\nSunrise time is {sunrise_time}!\n"
      f"Current time is {current_time} — {part_of_the_day}!")

if (sp_latitude - 5 <= iss_latitude <= sp_latitude + 5 and
    sp_longitude - 5 <= iss_longitude <= sp_longitude + 5 and
    part_of_the_day == "Nighttime"):
    print("ISS is overhead!")
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(email_address, password)
    connection.sendmail(
        from_addr=email_address,
        to_addrs=email_address,
        msg="Subject: Look up!\n\nThe ISS is overhead!"
    )
    connection.quit()
