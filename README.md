# Yad2 Apartment Notifier Script

This script is designed to monitor real estate listings on [Yad2](https://www.yad2.co.il/) and notify users about new apartments based on specified criteria. It utilizes the Telegram API to send notifications.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Required Python packages: `requests`, `json`, `time`, `urllib`, `telegram`

## Usage

1. Clone the repository:
   
   ```bash
   git clone https://github.com/Toms422/Yad2Search.git

2. Install the required packages:
   
   ```bash
   pip install -r requirements.txt
   
3. Obtain a Telegram Bot Token:
   ```bash
   Create a new bot on Telegram by talking to the @BotFather.

  Copy the generated token.

4. Update the script:
    ```bash  
   Replace 'YOUR_BOT_TOKEN' with the token you obtained.
   Replace 'YOUR_CHAT_ID_TOM' with your actual chat IDs

5. Run the script:
    ```bash
   python main.py


## Customization
You can customize the search parameters for each neighborhood by modifying the params dictionaries in the script. Adjust the parameters such as city, rooms, price, etc., according to your preferences.

## Contributing
Feel free to contribute to the development of this script by submitting issues or pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


Make sure to replace `'YOUR_BOT_TOKEN'`, `'YOUR_CHAT_ID_TOM'`, and `'YOUR_CHAT_ID_LEE'` with your actual Telegram bot token and chat IDs. Additionally, update the Git repository link in the clone command if your script is in a Git repository.


