from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import smtplib
import subprocess
import beepy

url = "https://www.walgreens.com/findcare/vaccination/covid-19/location-screening"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1680x1050")


def watchZipCode(zips):
    hasBeenSeen = {}
    for zipCode in zips:
        hasBeenSeen[zipCode] = False

    # driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome()
    driver.get("https://www.walgreens.com/findcare/vaccination/covid-19")
    btn = driver.find_element_by_css_selector("span.btn.btn__blue")
    btn.click()
    driver.get(url)
    while True:

        for zipCode in zips:
            # driver.get(
            #     "https://www.walgreens.com/findcare/vaccination/covid-19/location-screening"
            # )
            time.sleep(0.75)
            driver.get_screenshot_as_file("capture.png")
            element = driver.find_element_by_id("inputLocation")
            element.clear()
            element.send_keys(zipCode)
            button = driver.find_element_by_css_selector("button.btn")
            print(time.ctime(), "\n")
            button.click()

            time.sleep(0.75)
            alertElement = getAlertElement(driver)
            aptFound = alertElement.text == "Appointments available!"

            if aptFound and not hasBeenSeen[zipCode]:
                beepy.beep(sound="ready")
                message = "WALGREENS APPOINTMENT FOUND! ZIP CODE: " + zipCode
                print(message)
                subprocess.Popen(["open", url])
                # sendText(number, carrier, fromEmail, fromEmailPass, message)
                hasBeenSeen[zipCode] = True
            elif not aptFound:
                hasBeenSeen[zipCode] = False

            time.sleep(60)


def getAlertElement(driver):
    while True:
        try:
            alertElement = driver.find_element_by_css_selector("p.fs16")
            return alertElement
        except NoSuchElementException:
            time.sleep(0.5)


# def sendText(number, carrier, fromEmail, fromEmailPass, message):
#     carriers = {
#         'att': '@mms.att.net',
#         'tmobile': ' @tmomail.net',
#         'verizon': '@vtext.com',
#         'sprint': '@page.nextel.com'
#     }

#     to_number = number+'{}'.format(carriers[carrier])
#     Subject = 'Subject: Covid Vaccine:\n\n'
#     footer = '- Test'  # add test footer
#     conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
#     conn.ehlo()
#     conn.login(fromEmail, fromEmailPass)
#     conn.sendmail(fromEmail, to_number, Subject + message)
#     conn.quit()


if __name__ == "__main__":
    zips = ["60640"]
    watchZipCode(zips)
