#!/usr/bin/python
#.------..------..------..------..------.
#|S.--. ||L.--. ||3.--. ||4.--. ||K.--. |
#| :/\: || :/\: || :(): || :/\: || :/\: |
#| :\/: || (__) || ()() || :\/: || :\/: |
#| '--'S|| '--'L|| '--'3|| '--'4|| '--'K|
#`------'`------'`------'`------'`------'
#https://twitter.com/SL34K
#https://github.com/SL34K
#00110001 00111001
#00110000 00110011
#00110001 00111000 
#########################################
import requests, datetime, json, time, string, names
from bs4 import BeautifulSoup
from random import getrandbits,choice,randint
x = 0
def solution(apikey,sitekey,form):
    now = datetime.datetime.now()
    print (now.strftime("%H:%M:%S:%f: Getting captcha solution"))
    url="http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(apikey,sitekey,form)
    resp = requests.get(url) 
    if resp.text[0:2] != 'OK':
        quit('Error. Captcha is not received')
    captcha_id = resp.text[3:]
    fetch_url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(apikey,captcha_id)
    for i in range(1, 20):	
        time.sleep(5) # wait 5 sec.
        resp = requests.get(fetch_url)
        if resp.text[0:2] == 'OK':
                break
    captchasolution = resp.text[3:]
    return captchasolution
def session():
    sesh = requests.session()
    sesh.headers = {
        'Origin':'https://www.subtypestore.com',
        'Referer':'https://www.subtypestore.com/sean/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    sesh.headers.update()
    return sesh
def proxysession(proxy):
    ip,port,username,password = proxy.split(":")
    formattedProxy = (username+':'+password+'@'+ip+':'+port)
    proxies = {'http': 'http://'+formattedProxy}
    proxies = {'https': 'https://'+formattedProxy}
    sesh = requests.Session()
    sesh.proxies = proxies
    sesh.headers = {
        'Origin':'https://www.subtypestore.com',
        'Referer':'https://www.subtypestore.com/sean/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    sesh.headers.update()
    return sesh
def main():
    global x
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    catchalldomain = data['settings']['catchalldomain']
    randomnames = data['settings']['randomnames']
    setname = data['settings']['setname']
    signupdelay = int(data['settings']['signupdelay'])
    randomsizes = data['settings']['randomsizes']
    size = data['settings']['size']
    postcode = data['settings']['postcode']
    phone = data['settings']['phone']
    sitekey = data['settings']['sitekey']
    apikey = data['settings']['2captchaapikey']
    proxyuse = data['settings']['useproxy']
    proxy = data['settings']['proxy']
    form = data['settings']['form']
    now = datetime.datetime.now()
    print (now.strftime("%H:%M:%S:%f: @SL34K's Subtype Raffle BOT V1.1"))
    print (now.strftime("%H:%M:%S:%f: Starting bot"))
    entries = str(input (now.strftime("%H:%M:%S:%f: How many times do you wish to enter?: ")))
    x = int(x)
    while int(entries) > x:
        x = run(catchalldomain,randomnames,setname,randomsizes,size,postcode,phone,sitekey,apikey,proxyuse,proxy,form)
        time.sleep(signupdelay)
def run(catchalldomain,randomnames,setname,randomsizes,size,postcode,phone,sitekey,apikey,proxyuse,proxy,form):
    if proxyuse == 'True':
        now = datetime.datetime.now()
        print (now.strftime("%H:%M:%S:%f: Proxy use: True"))
        print (now.strftime("%H:%M:%S:%f: Proxy "+proxy))
        sesh = proxysession(proxy)
    else:
        now = datetime.datetime.now()
        print (now.strftime("%H:%M:%S:%f: Proxy use: False"))
        sesh = session()
    if randomnames == 'True':
        first = names.get_first_name()
        last = names.get_last_name()
        name = first+' '+last
        now = datetime.datetime.now()
        print (now.strftime("%H:%M:%S:%f: Using random names"))
        randomletters = "".join(choice(string.ascii_letters) for x in range(randint(1, 4)))
        username = randomletters+first+randomletters
        email = username+'@'+catchalldomain
    else:
        now = datetime.datetime.now()
        print (now.strftime("%H:%M:%S:%f: Using setname: "+setname))
        randomletters = "".join(choice(string.ascii_letters) for x in range(randint(1, 4)))
        username = randomletters+name
        email = username+'@'+catchalldomain
    if randomsizes == 'True':
        size = (randint(8, 28))/2
    x = signup(sesh,form,apikey,sitekey,phone,postcode,size,name,email)
    return x
    
def signup(sesh,form,apikey,sitekey,phone,postcode,size,name,email):
    global x
    x = int(x)
    capsolution = solution(apikey,sitekey,form)
    token = sesh.get(form)
    soup = BeautifulSoup(token.content,'html.parser')
    token = soup.find('input', {'name': 'state_3'}).get('value')
    data = {
        "input_9":name,
        "input_4":email,
        "input_3":phone,
        "input_6":size,
        "input_7":postcode,
        "g-recaptcha-response":capsolution,
        "is_submit_3":"1",
        "gform_submit":"3",
        "gform_unique_id":"",
        "state_3":token,
        "gform_target_page_number_3":"0",
        "gform_source_page_number_3":"1",
        "gform_field_values":"",
    }
    signup = sesh.post(form,data=data)
    soup = BeautifulSoup(signup.content,'html.parser')
    test = soup.find('h1', class_='entry-title center spacelarge').text
    if 'Thank You' in test:
        now = datetime.datetime.now()
        print (now.strftime("%H:%M:%S:%f: Entered: "+email))
        x = x+1
        return x
    else:
        print("Error entering")
        return x
main()
