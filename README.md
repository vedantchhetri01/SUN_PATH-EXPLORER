# SUN_PATH-EXPLORER
This is a Streamlit-based web application that allows users to analyze the position of the sun, including sunrise, sunset, and sunlight duration for any given location and date. The app provides a visual representation of the sun’s position in the sky, along with a scannable QR code linking to the selected location on Google Maps.

![PIC1](https://github.com/user-attachments/assets/85837c98-b3d9-4780-bf6e-aa1131bafcf3)
![PIC2](https://github.com/user-attachments/assets/e4992af2-cdbe-4de8-800d-6a8b5b033e1d)
![PIC3](https://github.com/user-attachments/assets/34fab224-afa3-40db-9327-5b9485fa5195)
![PIC4](https://github.com/user-attachments/assets/1822e3a5-c2f0-4d6a-bc73-3521cee89869)
Features:

    Location-based Sun Data: Get sunrise and sunset times, sunlight duration, and the sun's position (azimuth and altitude) for any location.
    Interactive Map: Displays the selected location on an interactive map using Folium.
    QR Code Generation: Generates a QR code for the location that links directly to Google Maps.
    Feedback System: Users can leave feedback to help improve the app.
Technologies Used:

    Streamlit: For creating the web app.
    Folium: For generating interactive maps.
    Geopy: For location-based geocoding (latitude and longitude).
    Ephem: For calculating the sun's position and times.
    Pytz: For handling time zone conversions.
    QR Code: To generate location-based QR codes.   
How to Use:

    Enter a location (e.g., "Delhi, India") and select a date.
    View the calculated sun position, sunrise, and sunset times.
    Scan the generated QR code to view the location on Google Maps.
