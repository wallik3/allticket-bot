# 🤏🎫 AllTicket Reservation Bot

- This repository hosts a Selenium-based ticket bot designed to automate ticket reservations on the AllTicket platform. Developed with pure Selenium, without relying on any additional frameworks, this bot is intended strictly for educational purposes. 
- In our tests, the average time taken to reserve a ticket is approximately 30 seconds. Once you've configured the bot with your event name and payment method, it will execute the process, culminating in rendering the payment method as the final step.

## Demo Usage
- The following video demonstrate how our bot works regarding to the configuration `user.json`
![Demonstration](https://github.com/wallik3/allticket-bot/blob/main/output/allticketbot%20example.mp4](https://github.com/wallik3/allticket-bot/blob/main/output/allticketbot%20example.gif?raw=true)

## Features

- **Automated Ticket Reservation:** The bot navigates the AllTicket website, selects the desired event, and reserves tickets based on the user's predefined preferences.
- **Customizable Settings:** Users can easily modify the bot to select different events, ticket quantities, and seating preferences.
- **Error Handling:** Basic error handling to manage common issues like page loading errors, network timeouts, and unresponsive elements.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/allticket-reservation-bot.git
   cd allticket-reservation-
   ```
   
2. **Install Dependencies:**
- Ensure you have Python installed on your machine. Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Google Chrome WebDriver:**
- Download the appropriate Chrome WebDriver for your browser and operating system. Place the WebDriver executable either in your system's PATH or in the project directory.
- The code assumes that the WebDriver is installed and located at `C:\Program Files (x86)\chromedriver-win64\chromedriver.`, otherwise, you have to change variable `driver_path` in `main.py`

4. **Configuration in user.json**
You can specify the details for the ticket reservation in the user.json file. Typically, there are four key fields, each with its description:

    1. **event_name**: The name of the event you want to reserve tickets for. This field is crucial for the bot to identify and select the correct event on the AllTicket platform.
    
    2. **prior_seat_type**: (Optional) The specific seat type(s) you want the bot to prioritize. If you want the bot to start with a particular seat type, you can list it here. You can include more than one seat type if needed.
    
    3. **chrome_profile_path**: The path to your Google Chrome profile. This allows the bot to use an already logged-in session, avoiding the need for repeated logins. This field ensures that the bot can directly access the AllTicket platform without requiring your AllTicket email and password.
    
    4. **payment_method**: (Optional) Currently, there are 2 options: 'cash' and 'promptpay', if not being specified, we will use cash by default

    Remove the key of configuration out if you don't have, for example, if you has no prior_seat_type, then remove that key from `user.json`

5. **Start your ticketbot**
- Run the bot with `python main.py` or by using `make reserve-allticket.`

## Future Implication
- Simplified Setup with Docker: Cloning the repository and installing dependencies alone isn't sufficient. To streamline the setup process, we'll be uploading a Docker image that includes all essential packages, such as the WebDriver and FFmpeg.

- Enhanced Speed: Currently, the bot uses a brute-force method that iterates through all available seats without optimization. We plan to make the bot faster by improving this approach.

- User Interface: We aim to add a user-friendly interface, potentially using Tkinter, to make the bot easier to configure and use.

## Limitation
- Last time, this ticketbot was tested on March 2024, If allticket website is updated, it is possible that it might not work anymore. 
