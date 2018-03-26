# TeleDoor
Open your garage door with python, telegram and ARM boards.

## Description
Python3 code to open/close your garage door using a telegram bot. I used an OrangePi zero WiFi board to control my door using a wired connection from a relay board to the door motor.

* [relay](https://images-na.ssl-images-amazon.com/images/I/41lrKvuQtqL._SY355_.jpg)
* [orangePi Zero](https://ae01.alicdn.com/kf/HTB1LJ0WOXXXXXXEaXXXq6xXFXXXT/Orange-PI-Zero-H2-Quad-Core-de-c-digo-abierto-256-MB-Placa-de-desarrollo-m.jpg)

## Dependencies
You need to install:
* [Python telegram bot](https://github.com/python-telegram-bot/python-telegram-bot) to interact with Telegram
* [orangepi_PC_gpio_pyH3](https://github.com/duxingkei33/orangepi_PC_gpio_pyH3) to control onboard leds

## Usage
You need to create a `token id` at [bot_father bot in Telegram](https://telegram.me/BotFather). Also you need to your `chat_id` to receive notifications and send commands to your bot. These two parameters should be used at `door.py`.

Then, move the door.service file to `/lib/systemd/system/` directory and enable the service to stat on boot. Finally add the following code to the end of your `/etc/rc.local` if you want monitor your wifi connection using the onboard red led:

```
python3 /root/moni.py &
exit 0
```

If the red led is blinking, there is no internet access. If the red led is lit, then you have internet on your board. 
