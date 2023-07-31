from urllib.request import Request, urlopen
from re import search
from time import sleep
import traceback
import smtplib

url = "https://blog.bestbuy.ca/best-buy/nvidia"
agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/94.0.4606.76 Mobile/15E148 Safari/604.1"
gdate = 'test'


def create_request(url):
    headers = {'User-Agent': agent}
    req = Request(url, data=None, headers=headers)
    return req


def getDate(data):
    date = search(
        '<strong style="color: #055499">(.*?)<sup>th</sup> during local store operating hours</strong>', str(data))
    date = date.group(1)
    return str(date)


def isChanged(date):
    gmail_user = 'Redacted'  # Add email
    gmail_pw = 'Redacted'  # Add password
    if date != gdate:
        sent_from = gmail_user
        to = ["Redacted"]  # Receiving email address
        subject = 'Best Buy Graphic Card Update'
        body = 'The new date for restocking is ' + date

        email_text = 'From: {0}\nTo: {1}\nSubject: {2}\n\n{3}'.format(
            sent_from, to, subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_pw)
            server.sendmail(sent_from, to, email_text)
            server.close()
            # print('Email sent!')
            return True
        except:
            print(traceback.format_exc())

    else:
        return False


while True:
    sleep(21600)
    try:
        response = urlopen(create_request(url), timeout=10)
        if response.getcode() == 200:
            data = response.read()
            date = getDate(data)
            if isChanged(date):
                gdate = date
            # print(gdate)
        else:
            print('Server returned non-200 status.')
    except:
        print(traceback.format_exc())
