import time
import picamera
import smtplib
import urllib.request
from gpiozero import MotionSensor, LED
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

fromaddr = 'portalportal001@gmail.com'
toaddr = 'mukeettransworld@gmail.com'
 
mail = MIMEMultipart()
 
mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = 'Intruder Alert'
body = 'Dear user, someone has tried to enter your smart room. Is this you?'

camera = picamera.PiCamera()
camera.rotation=180
camera.awb_mode= 'auto'
camera.brightness=55

THINGSPEAKKEY = 'JSLL5EUWJMBIYZW0'
THINGSPEAKURL = 'https://api.thingspeak.com/update'

pir_1 = MotionSensor(27)
pir_2 = MotionSensor(22)
led = LED(20)

occupancy = 0

def sendMail(data):
    mail.attach(MIMEText(body, 'plain'))
    dat='{}.jpg'.format(data)
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, 'flask_mail')
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def capture_image():
    data= time.strftime('%d-%b-%Y | %H:%M:%S')
    camera.start_preview()
    time.sleep(5)
    print(data)
    camera.capture('{}.jpg'.format(data))
    camera.stop_preview()
    time.sleep(1)
    return data

while True:
    if pir_1.motion_detected and not pir_2.motion_detected:
        pir_2.wait_for_motion()
        occupancy += 1
        led.on()
        print('Moved in...')
        print('Occupancy: {}'.format(occupancy))
        if occupancy == 1:
            data = capture_image()
            sendMail(data)
        urllib.request.urlopen('{}?api_key={}&field1={}'.format(THINGSPEAKURL, THINGSPEAKKEY, occupancy))
        pir_1.wait_for_no_motion()
        pir_2.wait_for_no_motion()
    print('OK')
    if pir_2.motion_detected and occupancy:
        pir_1.wait_for_motion()
        occupancy -=1
        if occupancy == 0:
            led.off()
        print('Moved out...')
        print('Occupancy: {}'.format(occupancy))
        urllib.request.urlopen('{}?api_key={}&field1={}'.format(THINGSPEAKURL, THINGSPEAKKEY, occupancy))
        pir_2.wait_for_no_motion()
        pir_1.wait_for_no_motion()
