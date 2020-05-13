# import necessary libraries and set variables

import requests, bs4, smtplib, email
nilCount = 0
loCount = 0
midCount = 0
hiCount = 0

# create a connection to gmail and prompt for a username and password

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login('youruser@gmail.com', input("Please enter the password: "))

# request the weather.gc website information

website = requests.get('https://weather.gc.ca/forecast/hourly/bc-74_metric_e.html')
try:
    website.raise_for_status()
except Excetion as exc:
    print("There was a problem: %s" % (exc))

# scrape the html of the website to retrieve just the chances of rain within the next few days

weather_data = bs4.BeautifulSoup(website.text, "html.parser")
chance_of_rain = weather_data.select('td[headers="header4"]')
for i in range(0, len(chance_of_rain)):
    chance_of_rain[i] = chance_of_rain[i].getText()

# retrieve rain fall data for the next 12 hours
    
for x in range(13):

    if chance_of_rain[x] =='Nil':
        nilCount += 1

    elif chance_of_rain[x] == 'Low':
        loCount += 1

    elif chance_of_rain[x] == 'Medium':
        midCount += 1

    elif chance_of_rain[x] == 'High':
        hiCount += 1

# send out an email to the input email address letting the user know what the chances of rain are, depending on data        

if hiCount > 0:
    smtpObj.sendmail('youruser@gmail.com', 'sendinguser@gmail.com',
    'Subject: Daily Rain Report. \nIt looks very likely to rain today. You should grab an umbrella and a jacket.')

elif hiCount == 0 and midCount > 0:
    smtpObj.sendmail('youruser@gmail.com', 'sendinguser@gmail.com',
    'Subject: Daily Rain Report. \nIt looks likekly to rain today. You should grab an umbrella.')

elif hiCount == 0 and midCount == 0 and loCount > 0:
    smtpObj.sendmail('youruser@gmail.com', 'sendinguser@gmail.com',
    'Subject: Daily Rain Report. \nIt looks like there is a pretty low chance of rain today. A jacket or umbrella is not needed')

else:
    smtpObj.sendmail('youruser@gmail.com', 'sendinguser@gmail.com',
    'Subject: Daily Rain Report. \nIt probably will not rain today. Enjoy the weather!')

smtpObj.quit()
