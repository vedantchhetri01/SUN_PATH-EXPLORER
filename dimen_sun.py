import streamlit as st
import folium
from geopy.geocoders import Nominatim
import ephem
import datetime
import pytz
from streamlit_folium import st_folium
from folium import plugins
import qrcode
from io import BytesIO

def get_location_from_name(location_name):
    geolocator = Nominatim(user_agent="sun_position_app")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

def convert_utc_to_local(utc_time, timezone_str):
    local_tz = pytz.timezone(timezone_str)
    utc_time = pytz.utc.localize(utc_time) 
    local_time = utc_time.astimezone(local_tz)
    return local_time

def calculate_sun_position(latitude, longitude, selected_date):
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    
    observer.date = datetime.datetime(selected_date.year, selected_date.month, selected_date.day, 12, 0, 0) 
    sunrise = observer.next_rising(ephem.Sun()).datetime()
    sunset = observer.next_setting(ephem.Sun()).datetime()
    local_sunrise = convert_utc_to_local(sunrise, 'Asia/Kolkata')
    local_sunset = convert_utc_to_local(sunset, 'Asia/Kolkata')
    observer.date = datetime.datetime(selected_date.year, selected_date.month, selected_date.day, 12, 0, 0)  
    sun = ephem.Sun(observer)
    azimuth = sun.az
    altitude = sun.alt
    sunlight_duration = local_sunset - local_sunrise

    return local_sunrise, local_sunset, sunlight_duration, azimuth, altitude, selected_date

def generate_qr_code_for_location(latitude, longitude):
    maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    qr = qrcode.make(maps_url)
    img_byte_arr = BytesIO()
    qr.save(img_byte_arr)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def app():
    st.title("🌞 Sun Position and Solar Data")
    with st.sidebar:
        st.markdown(
            """
            <style>
                .sidebar .sidebar-content {
                    font-size: 20px;
                    font-weight: bold;
                }
            </style>
            """, unsafe_allow_html=True
        )

        st.markdown("### Sun Position App")
        st.markdown("Analyze the position of the sun, sunrise, sunset, and much more!")

        # Location selection using input button
        location_name = st.text_input("Enter a Location", "Delhi, India")

        selected_date = st.date_input("Select a date:", datetime.date.today())
        st.markdown(
            """
            <a href="https://www.suncalc.org/#/18.969,72.8212,14/2025.01.03/18:11/1/1" target="_blank">
                <button style="font-size:18px; background-color:#00bcd4; color:white; padding:10px 20px; border:none; border-radius:5px;">
                    <i class="fa fa-bar-chart"></i> View Analysis
                </button>
            </a>
            """, unsafe_allow_html=True
        )
        st.markdown(
            """
            <style>
                body {
                    background-color: #121212;
                    color: white;
                }
                .sidebar .sidebar-content {
                    background-color: #2a2a2a;
                    color: white;
                }
            </style>
            """, unsafe_allow_html=True
        )

        with st.expander("Click to reveal the QR Code for Location"):
            location_coords = get_location_from_name(location_name)

            if location_coords:
                latitude, longitude = location_coords

                qr_img = generate_qr_code_for_location(latitude, longitude)
                st.markdown("### 📍 Scan this QR code to view the location on Google Maps!")
                st.image(qr_img, width=150) 
            else:
                st.error("Location not found!")
        st.markdown("### 📝 We value your feedback!")
        feedback = st.text_area("Please leave your feedback here:")
        if st.button("Submit Feedback"):
            if feedback:
                st.success("Thank you for your feedback!")
            else:
                st.warning("Please write some feedback before submitting.")

    # Only run calculations and display the map if the location exists
    with st.spinner("Fetching location data..."):
        location_coords = get_location_from_name(location_name)
    
    if location_coords:
        latitude, longitude = location_coords
        st.write(f"**Location:** {location_name} (Lat: {latitude}, Lon: {longitude})")
        st.write(f"**Selected Date:** {selected_date}")

        # Display map with the location
        sun_map = folium.Map(location=[latitude, longitude], zoom_start=12, control_scale=True)
        folium.Marker([latitude, longitude], popup="Your location").add_to(sun_map)
        plugins.ScrollZoomToggler().add_to(sun_map)
        st_folium(sun_map, width=700, height=500)

        # Calculate and display sun data
        local_sunrise, local_sunset, sunlight_duration, azimuth, altitude, current_time = calculate_sun_position(latitude, longitude, selected_date)
        st.markdown("### 🌅 Sun Data")

        st.markdown(f"**Sunrise Time (Local):** {local_sunrise.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"**Sunset Time (Local):** {local_sunset.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"**Total Sunlight Duration:** {str(sunlight_duration)}")

        # Add a visual indicator of the sun's position
        st.markdown("### 🌞 Visualizing Sun's Position:")
        st.write(f"**Sun's Position in the Sky:**")
        st.write(f"Azimuth: {azimuth:.2f} rad (from North)")
        st.write(f"Altitude: {altitude:.2f} rad (above the horizon)")

        if altitude > 0:
            st.markdown("The sun is currently visible in the sky!")
        else:
            st.markdown("The sun is below the horizon!")

        # Hide the footer (Streamlit default)
        st.markdown(
            """
            <style>
                footer {
                    visibility: hidden;
                }
            </style>
            """, unsafe_allow_html=True
        )

        # Footer
        st.markdown(f"**App made with love by Vedant Chhetri** 💡")

    else:
        st.error("Location not found! Please try a valid city name.")

if __name__ == "__main__":
    app()
