# KideAppBot

## Features

- Logs into kide.app using provided email and password.
- Refreshes the event page until tickets become available.
- Automatically selects ticket quantity and adds tickets to the cart.
- Uses Selenium WebDriver for automation.

## How to use

1. Update the `emailPassword` dictionary with your email and password.
2. Set the `path` variable to your ChromeDriver location.
3. Update the event URL in `driver.get()` to your target event.
4. Adjust `ticketSaleStart` to the time ticket sales begin.
5. Run the script before ticket sales start.
   
## Limitations

**Recently, the kide.app website introduced bot detection (Cloudflare) that blocks automated scripts like this one.**  
**As a result, this bot does not work anymore.**

## Requirements

- Python 3.x
- Selenium (`pip install selenium`)
- pytz (`pip install pytz`)
- ChromeDriver compatible with your Chrome version
