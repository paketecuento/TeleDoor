import subprocess
import sys
import time
import subprocess
import socket
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def lamp_red_on_fix():
  subprocess.run("echo 1 > /sys/class/leds/orangepi\:red\:status/brightness", shell=True)


def lamp_red_on_blink(tim):
  timeout = time.time() + tim   # 5 minutes from now
  while True:
    subprocess.run("echo 0 > /sys/class/leds/orangepi\:red\:status/brightness", shell=True)
    time.sleep(0.5)
    subprocess.run("echo 1 > /sys/class/leds/orangepi\:red\:status/brightness", shell=True)
    time.sleep(0.5)
    if time.time() > timeout:
      break


def internet(host="8.8.8.8", port=53, timeout=3):
   """
   Host: 8.8.8.8 (google-public-dns-a.google.com)
   OpenPort: 53/tcp
   Service: domain (DNS/TCP)
   """
   try:
     socket.setdefaulttimeout(timeout)
     socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
     logger.info('Internet is there!!')
     return True
   except Exception as ex:
     logger.warning('Internet is gone!!')
     return False


def main():
  test = 0
  while True:
    test+=1
    success = internet()
    if success:
      lamp_red_on_fix()
      time.sleep(60)
    else:
      lamp_red_on_blink(30)

if __name__ == '__main__':
  try:
    main()
  except (KeyboardInterrupt, SystemExit):
    subprocess.run("echo 0 > /sys/class/leds/orangepi\:red\:status/brightness", shell=True)
    print('\nkeyboardinterrupt found!')
    print('...Program Stopped Manually!')
