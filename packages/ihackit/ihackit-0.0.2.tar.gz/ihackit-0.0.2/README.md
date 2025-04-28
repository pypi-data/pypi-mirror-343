# ihackit  
**Instagram Private Api, Device Customization, User-Agent Generator & Identifier Generator Library**  

ihackit is a powerful and flexible python library for automating instagram accounts with private api from apk pinning, generate device configuration and customizing user-agent strings to avoid suspicious login, built to provide full control over account management, media posts scraping, and etc.

> i made this library for instagram hacking tools :)
> https://github.com/termuxhackers-id/instahack

## Requirements
| Library       | Installation                  | 
|---------------|-------------------------------|
| Requests      | `pip install requests`        |
| Pycryptodomex | `pip install pycryptodomex`   |

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Customize](#customize)
- [Hackers](#hackers)
- [Authors](#authors)

## Installation
install with pip
```bash  
pip install ihackit
```  
install with clone repository
```bash
git clone https://github.com/iqbalmh18/ihackit
cd ihackit
pip install .
```

## Quick Start
example usage of `ihackit`
```python
from ihackit import Instagram

# set new instagram session
ig = Instagram(cookie='YOUR INSTAGRAM COOKIE')

# get account info
print(ig.account())

# get username info
print(ig.username_info('username')

# get location info from username
print(ig.location_info('username')

# get followers from target username
foll = ig.followers('username')
for user in foll:
    print(user)

# get following from username
foll = ig.following('username')
for user in foll:
    print(user)

# get mediapost from username
media = ig.mediapost('username')
for post in media:
    print(post)

# get media info from media id or url
url = 'https://www.instagram.com/p/XXXX'
print(ig.media_info(url))
```

## Customize
Check Available Device
```python
from ihackit import DEVICE, DEVICE_LIST

print(DEVICE)
print(DEVICE_LIST)
```
Check Available Country
```python
from ihackit import COUNTRY, COUNTRY_LIST

print(COUNTRY)
print(COUNTRY_LIST)
```
Device Customization  
```python  
from ihackit import Device  

device = Device(device_brand='Samsung', device_model='SM-A125F', device_country='ID')  
info = device.info()  
print(info)  
```  
User Agent Customization
```python
from ihackit import Device, UserAgent

device = Device(device_brand='Samsung', device_model='SM-A125F', device_country='ID')  
useragent = UserAgent(device)

print(useragent.dalvik())
print(useragent.threads())
print(useragent.facebook())
print(useragent.instagram())
```

## Hackers
example usage of `ihackit` for hackers
```python  
from ihackit import (
    Device,
    UserAgent,
    Generator,
    Instagram
)

cookies = 'YOUR INSTAGRAM COOKIE'  
proxies = {'http': 'protocol:ip:port', 'https': 'protocol:ip:port'}
devices = Device('Samsung').info()

useragent = UserAgent(devices)
generator = Generator()
device_id = generator.device_id()

ig = Instagram(cookie=cookies, device=devices, device_id=device_id, proxies=proxies)

info = ig.account()
if info:
    print(info)
    print(ig.session.headers)
else:
    print('cookie is not valid or have been expired')
```  
example usage to generate `identifier` for hackers
```python  
from ihackit import Identifier  

identify = Identifier(firstname='john', last_name='doe', domain=['gmail.com','yahoo.com'], result=10)  

emails = identify.email()  
for email in emails:  
    print(email)  
    
usernames = identify.username()
for username in usernames:
    print(username)

fullname = identify.fullname()
print(fullname)

wordlist = identify.wordlist()
print(wordlist)
```  

## Authors
<p align="center">
  <img src="https://2.gravatar.com/avatar/883c7ebdf4f802eeeaafad5c229372afdb625e67de197c88272fa2fcf12256fb?size=512" width="150" style="border-radius: 50%;">
  <br>
  <b>Iqbalmh18</b>
  <br>
  <a href="https://github.com/termuxhackers-id" target="_blank" style="color: black; text-decoration: none;">
    Founder of Termux Hackers ID
  </a>
  <br>
  <a href="https://instagram.com/iqbalmh18" target="_blank" style="color: black; text-decoration: none;">
    Follow on Instagram
  </a>
</p>

[*back to top*](#ihackit)