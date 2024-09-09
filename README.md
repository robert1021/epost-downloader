# ePost Downloader

## Overview

ePost Downloader is a Python application using the Eel library to create a desktop application with a Bootstrap-based frontend.
This app utilizes the Canada Post ePost API to download messages from applicants with various options for filtering and categorization.

## Features

- **Download Messages:** Download messages from ePost Connect using the API.
- **Date Range Filtering:** Specify start and end dates to filter messages.
- **Message Selection:** Choose to download all messages or only the new ones.
- **Categorization:** Optionally categorize messages.
- **Metadata Scraping:** Scrape metadata from the ePost Connect website.
- **Automatic Triage:** Move downloaded messages to the triage folder automatically.

## Prerequisites

- **Python 3.11.6:** Ensure you have Python 3.11.6 installed.
- **Canada Post Token:** Obtain a token from Canada Post to access the ePost API. 
- **ePost Connect Credentials:** If scraping metadata, you will need the username and password for your ePost Connect account.

## Installation

1. **Clone the Repository:** https://github.com/robert1021/epost-downloader.git
2. **Install Dependencies:** Create a virtual environment and install the required packages (pip install -r requirements.txt)

## Usage

1. **Run the Application:** python main.py
2. **Using the interface:**
    
    - Open the application and enter the start and end dates for the messages you want to download.
    - Choose whether to download all messages or only new ones.
    - Optionally, select if you want to categorize messages.
    - If scraping metadata, ensure the ePost Connect credentials are provided.
    - Optionally, select if you want to move the messages to the triage folder.
    - Click "Start" to begin the download process.

## Screenshots

*App*

![App](./assets/app.PNG)

*Enter Start Date*

![Enter Start Date](./assets/start-date.PNG)

*Enter End Date*

![Enter End Date](./assets/end-date.PNG)

*Run With Categorize Messages*

![Run With Categorize Messages](./assets/start-categorize-messages.PNG)

*Scrape ePost Connect*
![Scrape ePost Connect](./assets/scrape-epost-connect.PNG)