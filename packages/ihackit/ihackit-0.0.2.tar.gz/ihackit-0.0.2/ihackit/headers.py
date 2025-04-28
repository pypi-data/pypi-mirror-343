import re
import random

class ApiHeaders:
    
    @staticmethod
    def get(host: str, data: dict, user_agent: str, authorization: str = None):
        headers = {
            'host': 'i.instagram.com',
            'accept-encoding': 'gzip, deflate',
            'accept-language': '{}, en-US'.format(data['ig_app_locale'].replace('_','-')),
            'x-ig-app-id': data['ig_app_id'],
            'x-ig-device-id': data['ig_device_id'],
            'x-ig-family-device-id': data['ig_family_device_id'],
            'x-ig-android-id': data['ig_android_id'],
            'x-ig-connection-type': 'MOBILE(LTE)',
            'x-fb-connection-type': 'MOBILE.LTE',
            'x-fb-http-engine': 'Liger',
            'x-mid': data['mid'],
            'user-agent': user_agent
        }
        if authorization is not None:
            headers.update({'authorization': authorization})
        return headers
    
    @staticmethod
    def post(host: str, data: dict, user_agent: str):
        headers = {
            'host': 'i.instagram.com',
            'x-ig-app-locale': data['ig_app_locale'],
            'x-ig-device-locale': data['ig_app_locale'],
            'x-ig-mapped-locale': data['ig_app_locale'],
            'x-pigeon-session-id': data['pigeon_session_id'],
            'x-pigeon-rawclienttime': data['pigeon_rawclienttime'],
            'x-ig-bandwidth-speed-kbps': '{}.000'.format(str(random.randint(1200,1418))),
            'x-ig-bandwidth-totalbytes-b': str(random.randint(1320000,1323526)),
            'x-ig-bandwidth-totaltime-ms': str(random.randint(888,999)),
            'x-bloks-version-id': data['bloks_version_id'],
            'x-ig-www-claim': '0',
            'x-bloks-is-prism-enabled': 'false',
            'x-bloks-is-layout-rtl': 'false',
            'x-ig-device-id': data['ig_device_id'],
            'x-ig-family-device-id': data['ig_family_device_id'],
            'x-ig-android-id': data['ig_android_id'],
            'x-ig-timezone-offset': data['ig_timezone_offset'],
            'x-ig-connection-type': 'MOBILE(LTE)',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-app-id': data['ig_app_id'],
            'priority': 'u=3',
            'user-agent': user_agent,
            'accept-language': '{}, en-US'.format(data['ig_app_locale'].replace('_','-')),
            'x-mid': data['mid'],
            'ig-intended-user-id': '0',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'content-length': str(random.randint(2345,3456)),
            'accept-encoding': 'gzip, deflate',
            'x-fb-connection-type': 'MOBILE.LTE',
            'x-fb-http-engine': 'Liger',
            'x-fb-client-ip': 'True',
            'x-fb-server-cluster': 'True'
        }
        if host == 'threads':
            headers.update({'x-tigon-is-retry': 'True, True'})
        return headers

class WebHeaders:
    
    @staticmethod
    def get_chrome_version(user_agent: str):
        pattern = r'(?:Chrome|CriOS)/(\d+\.\d+\.\d+\.\d+)'
        match = re.search(pattern, user_agent)
        return match.group(1) if match else '122.0.6261.77'

    @staticmethod
    def get_platform_type(user_agent: str):
        if 'iPhone' in user_agent:
            return '"iOS"', '?1'
        elif 'Macintosh' in user_agent:
            return '"macOS"', '?0'
        elif 'Windows' in user_agent:
            return '"Windows"', '?0'
        elif 'X11' in user_agent:
            return '"Linux"', '?0'
        elif 'Android' in user_agent:
            return '"Android"', '?1'
        return '"Unknown"', '?0'

    @staticmethod
    def get(host: str, user_agent: str):
        version = WebHeaders.get_chrome_version(user_agent)
        platform, mobile = WebHeaders.get_platform_type(user_agent)
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'dpr': '2.75',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'viewport-width': '980',
            'sec-ch-prefers-color-scheme': random.choice(['dark', 'light']),
            'sec-ch-ua': f'"Not/A)Brand";v="8", "Chromium";v="{version.split(".")[0]}", "Google Chrome";v="{version.split(".")[0]}"',
            'sec-ch-ua-full-version-list': f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not/A)Brand";v="8"',
            'sec-ch-ua-mobile': mobile,
            'sec-ch-ua-platform': platform,
            'user-agent': user_agent,
        }
        if host == 'threads':
            headers.update({'referer': 'https://www.threads.net'})
        else:
            headers.update({'referer': 'https://www.instagram.com'})
        return headers

    @staticmethod
    def post(host: str, user_agent: str):
        version = WebHeaders.get_chrome_version(user_agent)
        platform, mobile = WebHeaders.get_platform_type(user_agent)
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '305',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'sec-ch-prefers-color-scheme': random.choice(['dark', 'light']),
            'sec-ch-ua': f'"Not/A)Brand";v="8", "Chromium";v="{version.split(".")[0]}", "Google Chrome";v="{version.split(".")[0]}"',
            'sec-ch-ua-full-version-list': f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not/A)Brand";v="8"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-ch-ua-mobile': mobile,
            'sec-ch-ua-platform': platform,
            'user-agent': user_agent,
        }
        if host == 'threads':
            headers.update({
                'origin': 'https://www.threads.net/',
                'referer': 'https://www.threads.net/login?hl=id',
                'x-asbd-id': '359341',
                'x-bloks-version-id': '057c41cc15ea08e8f8a4a55ff49ae274dff45f744ad7d173aa98c6668f53e53f',
                'x-csrftoken': '-4HP8rwFMgpBFjXEGsd06s',
                'x-instagram-ajax': '0',
                'x-ig-app-id': '1412234116260832' if 'iPhone' in user_agent or 'Android' in user_agent else '238260118697367',
            })
        else:
            headers.update({
                'origin': 'https://www.instagram.com/',
                'referer': 'https://www.instagram.com/accounts/login/',
                'x-asbd-id': '359341',
                'x-csrftoken': 'sG8kvnWLy7BpiY7HbiBjHcMoGZW80fGL',
                'x-ig-www-claim': '0',
                'x-instagram-ajax': '1020718735',
                'x-requested-with': 'XMLHttpRequest',
                'x-web-session-id': '45ulcj:lnr4de:ibkk03',
                'x-ig-app-id': '1217981644879628' if 'iPhone' in user_agent or 'Android' in user_agent else '936619743392459',
            })
        return headers