
IP Address Tracking System – Detailed Overview
This IP Address Tracking System is a Tkinter-based Python application that allows users to retrieve detailed information about a given IP address, including geolocation data and device information. The application provides an intuitive user interface with features such as IP validation, data export, search history, and a loading animation for a better user experience.

🔹 Features
IP Address Validation

Ensures that the entered IP follows the correct format before making requests.
IP Information & Geolocation Retrieval

Fetches data from ipapi.co, including:
Country, region, city
Postal code
Latitude & longitude
Device Information Collection

Displays details of the system running the application:
OS version, hostname, machine type, processor details
Local IP, MAC address, and uptime statistics
Live Loading Animation

Enhances user experience by displaying a temporary loading message while fetching data.
Data Export (TXT & JSON)

Saves the retrieved information in text or JSON format for later use.
Search History Tracking

Logs previously searched IP addresses for quick reference.
Modern UI with Tkinter & ttk

A clean, responsive, and easy-to-use interface.
🛠 How It Works
User Inputs an IP Address

The program verifies if the IP is correctly formatted.
If valid, it proceeds with fetching details from the external API.
Data Retrieval & Display

Calls ipapi.co to obtain location-based data.
Fetches system-related details via platform, socket, and psutil modules.
Output Presentation

Displays all collected information in a text box within the UI.
Updates the search history list.
Additional Functionality

Clear Data: Clears both the output and input fields.
Export Data: Saves retrieved information as a .txt or .json file.
