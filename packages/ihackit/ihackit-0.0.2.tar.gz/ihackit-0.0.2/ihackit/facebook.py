import os
import re
import json
import uuid
import random
import string
import requests

from datetime import datetime

class Facebook:
    
    base = 'https://web.facebook.com'
    
    def __init__(self, cookie: str = None):
        self.cookies = cookie
        self.session = requests.Session()
        self.session.headers.update(self.get_headers())
        self.user_id = self.extract_user_id(self.cookies) if self.cookies else None
        self.fbtoken = self.get_token() if self.cookies else {}

    @staticmethod
    def extract_data(pattern: str, text: str, default='') -> str:
        match = re.search(pattern, text)
        return match.group(1) if match else default

    @staticmethod
    def extract_user_id(cookie: str) -> str | None:
        user = re.search(r'c_user=(\d+)', cookie)
        return user.group(1) if user else None

    def get_id(self, link_or_username: str) -> str | None:
        link = (
            link_or_username.replace('m.facebook','web.facebook')
            .replace('www.facebook','web.facebook')
            if link_or_username.startswith('https')
            else os.path.join(self.base, link_or_username)
        )
        response = self.session.get(link, allow_redirects=True)
        response.raise_for_status()
        html = response.text.replace('\\','')
        for pattern in [r'"userID"\s*:\s*"(.*?)"', r'"actor_id"\s*:\s*"(.*?)"']:
            if match := re.search(pattern, html):
                return match.group(1)
        raise Exception(f'failed to get user id from {link_or_username}')

    def get_link(self, user: str, path: str = '') -> str:
        fbid = self.get_id(user) if user.startswith('https') else user
        return f'{self.base}/{fbid}{"/" + path if path else ""}'
    
    @staticmethod
    def get_data(response: str) -> dict:
        try:
            return {
                'av':(av := Facebook.extract_data(r'"actorID":"(.*?)"', response)),
                '__user':av,
                '__a':str(random.randrange(1, 6)),
                '__hs':Facebook.extract_data(r'"haste_session":"(.*?)"', response),
                'dpr':'1.5',
                '__ccg':Facebook.extract_data(r'"connectionClass":"(.*?)"', response),
                '__rev':(__rev := Facebook.extract_data(r'"__spin_r":(.*?),', response)),
                '__spin_r':__rev,
                '__spin_b':Facebook.extract_data(r'"__spin_b":"(.*?)"', response),
                '__spin_t':Facebook.extract_data(r'"__spin_t":(.*?),', response),
                '__hsi':Facebook.extract_data(r'"hsi":"(.*?)"', response),
                '__comet_req':'15',
                'fb_dtsg':Facebook.extract_data(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', response),
                'jazoest':Facebook.extract_data(r'jazoest=(.*?)"', response),
                'lsd':Facebook.extract_data(r'"LSD",\[\],{"token":"(.*?)"}', response),
            }
        except Exception:
            return {}
    
    def get_token(self) -> dict:
        try:
            return {
                'business':re.search(
                    r'(\["EAAG\w+)', self.session.get('https://business.facebook.com/business_locations').text.replace('\\','')).group(1).replace('["',''),
                'adsmanager':re.search(
                    r'accessToken="(.*?)"', self.session.get('https://adsmanager.facebook.com/adsmanager/manage/campaigns?act={}&breakdown_regrouping=1&nav_source=no_referrer'.format(
                        re.search(r'act=(\d+)', self.session.get(f'{self.base}/adsmanager/manage/campaigns', cookies={'cookie':self.cookies}).text.replace('\\','')).group(1)
                        )).text.replace('\\','')).group(1)
            }
        except Exception:
            return {}
    
    def get_headers(self, method: str = 'get') -> dict:
        headers = {
            'authority':'web.facebook.com',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US;q=0.8,en;q=0.7',
            'sec-ch-prefers-color-scheme':'dark',
            'sec-ch-ua':'"Not/A)Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        headers.update({
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'cache-control':'max-age=0',
            'pragma':'no-cache',
            'dpr':'1',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':'1'
        } if method.lower() == 'get' else {
            'accept':'*/*',
            'content-length':str(random.randint(1000, 1890)),
            'content-type':'application/x-www-form-urlencoded',
            'origin':self.base,
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'x-asbd-id':'359341'
        })
        if self.cookies:
            headers['cookie'] = self.cookies
        return headers
    
    def login(self, username: str, password: str):
        facebook = 'https://m.prod.facebook.com'
        session = requests.Session()
        session.headers.update({
            'authority': facebook.split('/')[-1],
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US;q=0.8,en;q=0.7',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
            'dpr':'2.75',
            'sec-ch-prefers-color-scheme':'light',
            'sec-ch-ua':'"Not A(Brand";v="8", "Chromium";v="132"',
            'sec-ch-ua-full-version-list':'"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6961.0"',
            'sec-ch-ua-mobile':'?1',
            'sec-ch-ua-model':'"Redmi Note 9 Pro"',
            'sec-ch-ua-platform':'"Android"',
            'sec-ch-ua-platform-version':'"12.0.0"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'viewport-width':'980'
        })
        response = session.get(f'{facebook}/')
        response.raise_for_status()
        html = response.text.replace('\\','')
        find = re.findall(r'\(bk\.action\.array\.Make, "password", "(.*?)", "(.*?)"', html)
        username_text_input_id, password_text_input_id = (find[0] if find and isinstance(find[0], (tuple, list)) and len(find[0]) == 2 else ('j6k0p1:68', 'j6k0p1:69'))
        find = re.findall(r'"INTERNAL__latency_qpl_marker_id", "INTERNAL__latency_qpl_instance_id", "device_id", "family_device_id", "waterfall_id", "offline_experiment_group", "layered_homepage_experiment_group", "is_platform_login", "is_from_logged_in_switcher", "is_from_logged_out", "access_flow_version"\), \(bk.action.array.Make, "", (\d+), \(bk.action.i64.Const, (\d+)', html)
        INTERNAL__latency_qpl_marker_id, INTERNAL__latency_qpl_instance_id = ([str(item) for item in find[0]] if find and isinstance(find[0], (tuple, list)) and len(find[0]) == 2 and all(isinstance(item, (int, float, str)) for item in find[0])else ('36707139', '115986906100396'))
        print(username_text_input_id, password_text_input_id, INTERNAL__latency_qpl_marker_id,INTERNAL__latency_qpl_instance_id)
        data = {
            '__aaid':'0',
            '__user':'0',
            '__a':'1',
            '__req':'j',
            '__hs':self.extract_data(r'"haste_session":"(.*?)"', html),
            'dpr':'1',
            '__ccg':self.extract_data(r'"connectionClass":"(.*?)"', html),
            '__rev':self.extract_data(r'"__spin_r":(.*?),', html),
            '__hsi':self.extract_data(r'"hsi":"(.*?)"', html),
            '__dyn':'',
            '__csr':'',
            '__hsdp':'',
            '__hblp':'',
            'fb_dtsg':self.extract_data(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', html),
            'jazoest':self.extract_data(r'jazoest=(.*?)"', html),
            'lsd':self.extract_data(r'"LSD",\[\],{"token":"(.*?)"}', html),
            '__jssesw':'1',
            'params':json.dumps({
                "params":"{\"server_params\":{\"credential_type\":\"password\",\"username_text_input_id\":\""+username_text_input_id+"\",\"password_text_input_id\":\""+password_text_input_id+"\",\"login_source\":\"Login\",\"login_credential_type\":\"none\",\"server_login_source\":\"login\",\"ar_event_source\":\"login_home_page\",\"should_trigger_override_login_success_action\":0,\"should_trigger_override_login_2fa_action\":0,\"is_caa_perf_enabled\":0,\"reg_flow_source\":\"login_home_native_integration_point\",\"caller\":\"gslr\",\"is_from_landing_page\":0,\"is_from_empty_password\":0,\"is_from_password_entry_page\":0,\"is_from_assistive_id\":0,\"is_from_msplit_fallback\":0,\"INTERNAL__latency_qpl_marker_id\":"+INTERNAL__latency_qpl_marker_id+",\"INTERNAL__latency_qpl_instance_id\":\""+INTERNAL__latency_qpl_instance_id+"\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\""+str(uuid.uuid4())+"\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"pre_mt_behavior\"},\"client_input_params\":{\"machine_id\":\"\",\"contact_point\":\""+username+"\",\"password\":\"#PWD_BROWSER:0:"+str(datetime.now().timestamp())[:10]+":"+password+"\",\"accounts_list\":[],\"fb_ig_device_id\":[],\"secure_family_device_id\":\"\",\"encrypted_msisdn\":\"\",\"headers_infra_flow_id\":\"\",\"try_num\":1,\"login_attempt_count\":1,\"event_flow\":\"login_manual\",\"event_step\":\"home_page\",\"openid_tokens\":{},\"auth_secure_device_id\":\"\",\"client_known_key_hash\":\"\",\"has_whatsapp_installed\":0,\"sso_token_map_json_string\":\"\",\"should_show_nested_nta_from_aymh\":0,\"password_contains_non_ascii\":\"false\",\"has_granted_read_contacts_permissions\":0,\"has_granted_read_phone_permissions\":0,\"app_manager_id\":\"\",\"lois_settings\":{\"lois_token\":\"\"}}}"
            })
        }
        session.headers.update({
            'accept':'*/*',
            'content-length':str(len(data)),
            'origin':f'https://{facebook}',
            'referer':f'https://{facebook}/',
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
        })
        session.headers.pop('cache-control')
        session.headers.pop('viewport-width')
        session.headers.pop('upgrade-insecure-requests')
        find = re.search('versioningID:"(.*?)"', html)
        blok = find.group(1) if find else '2238fef536737a6cadcc343ca637ae897c1be7af47bd6ce31c6fa5621cb1c887'
        post = session.post(f'{facebook}/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.login.async.send_login_request&type=action&__bkv={blok}', data=data, allow_redirects=True)
        print(post.text)
        if 'c_user' in post.cookies.get_dict():
            cookie = '; '.join([key+'='+value for key, value in post.cookies.get_dict().items()])
            cookie = f'dpr=2.6036243438720703; {cookie};  ps_l=1; ps_n=1; locale=id_ID; wd=457x861; m_pixel_ratio=2.3638083934783936'
            return {'status':True, 'message':'login success','cookie':cookie}
        elif 'two_step' in post.text:
            return {'status':False,'message':'two factor required please turn off two factor login (2FA)'}
        elif 'checkpoint' in post.text:
            return {'status':False,'message':'checkpoint required please verify your accounts'}
        else:
            if 'bk.components.dialog.Dialog' in post.text:
                message = re.search('"message":"(.*?)","primary_button"', post.text)
                return {'status':False,'message':str(message.group(1)).lower() if message else None}
            return {'status':False,'message':'login failed incorrect username or password'}
    
    def friends(self, user: str) -> dict:
        response = self.session.get(self.get_link(user))
        response.raise_for_status()
        html = response.text.replace('\\', '')
        tab_key = self.extract_data(r'{"tab_key":"friends_all","id":"(.*?)"}', html)
        if not tab_key:
            return {}
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'ProfileCometAppCollectionListRendererPaginationQuery',
                    'variables':json.dumps({
                        "count":8,
                        "cursor":end_cursor,
                        "scale":3,
                        "search":None,
                        "id":tab_key
                    }),
                    'server_timestamps':True,
                    'doc_id':'9394039170688660'
                })
                post = self.session.post(f'{self.base}/api/graphql', headers=self.get_headers('post'), data=data).json()
                page_info = post['data']['node']['pageItems']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['node']['pageItems']['edges']:
                    yield {
                        'id':edge['node']['node']['id'],
                        'name':edge['node']['title'],
                        'link':edge['node']['node']['url']
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except Exception:
                break
    
    def account(self) -> dict:
        response = self.session.get('https://accountscenter.facebook.com/personal_info')
        response.raise_for_status()
        html = response.text.replace('\\','')
        info = {}
        info['id'] = self.extract_data(r'"USER_ID":"(.*?)"', html)
        find = self.extract_data(r'"navigation_row_subtitle":"(.*?)","node_id":"CONTACT_POINT",', html)
        if find:
            emails = [item.replace('u0040','@') for item in find.split(',') if '.com' in item]
            phones = [item.strip() for item in find.split(',') if '+' in item]
            info['email'] = emails[0] if emails else ''
            info['phone'] = phones[0] if phones else ''
        if self.fbtoken:
            find = self.session.get(f'https://graph.facebook.com/me/friends?limit=0&access_token={self.fbtoken["adsmanager"]}', cookies={'cookie':self.cookies}).json()
            info['friends'] = str(find.get('summary','').get('total_count',''))
        find = self.extract_data(r'"navigation_row_subtitle":"(.*?)"\s*,\s*"node_id":"BIRTHDAY"', html)
        if find:
            info['birthday'] = find.split('"')[-1]
        info['fullname'] = self.extract_data(r'"NAME":"(.*?)"', html)
        info['username'] = self.extract_data(r'"username":"(.*?)"', html)
        if self.fbtoken:
            find = self.session.get(f'https://graph.facebook.com/me?fields=subscribers.fields(id).limit(0)&access_token={self.fbtoken["business"]}', cookies={'cookie':self.cookies}).json()
            info['followers'] = str(find.get('subscribers','').get('summary','').get('total_count',''))
        info['pictures'] = self.extract_data(r'"profilePicLarge":{"uri":"(.*?)"}', self.session.get(self.get_link(info['id'])).text.replace('\\',''))
        return info if info['id'] and info['id'] != '0' else {}
    
    def followers(self, user: str) -> dict:
        response = self.session.get(self.get_link(user))
        response.raise_for_status()
        html = response.text.replace('\\', '')
        tab_key = self.extract_data(r'{"tab_key":"followers","id":"(.*?)"}', html)
        if not tab_key:
            return {}
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'ProfileCometAppCollectionListRendererPaginationQuery',
                    'variables':json.dumps({
                        "count":8,
                        "cursor":end_cursor,
                        "scale":3,
                        "search":None,
                        "id":tab_key
                    }),
                    'server_timestamps':True,
                    'doc_id':'9394039170688660'
                })
                post = self.session.post(f'{self.base}/api/graphql', headers=self.get_headers('post'), data=data).json()
                page_info = post['data']['node']['pageItems']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['node']['pageItems']['edges']:
                    yield {
                        'id':edge['node']['node']['id'],
                        'name':edge['node']['title']['text'],
                        'link':edge['node']['node']['url']
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except Exception:
                break
    
    def following(self, user: str) -> dict:
        response = self.session.get(self.get_link(user))
        response.raise_for_status()
        html = response.text.replace('\\', '')
        tab_key = self.extract_data(r'{"tab_key":"following","id":"(.*?)"}', html)
        if not tab_key:
            return {}
        data = self.get_data(html)
        end_cursor = None
        has_next_page = True
        while has_next_page:
            try:
                data.update({
                    'fb_api_caller_class':'RelayModern',
                    'fb_api_req_friendly_name':'ProfileCometAppCollectionListRendererPaginationQuery',
                    'variables':json.dumps({
                        "count":8,
                        "cursor":end_cursor,
                        "scale":3,
                        "search":None,
                        "id":tab_key
                    }),
                    'server_timestamps':True,
                    'doc_id':'9394039170688660'
                })
                post = self.session.post(f'{self.base}/api/graphql', headers=self.get_headers('post'), data=data).json()
                page_info = post['data']['node']['pageItems']['page_info']
                has_next_page = page_info.get('has_next_page', False)
                for edge in post['data']['node']['pageItems']['edges']:
                    yield {
                        'id':edge['node']['node']['id'],
                        'name':edge['node']['title']['text'],
                        'link':edge['node']['node']['url']
                    }
                if has_next_page:
                    end_cursor = page_info.get('end_cursor')
            except Exception:
                break
    
    def application(self) -> list:
        response = self.session.post(f'{self.base}/setting')
        response.raise_for_status()
        html = response.text.replace('\\', '')
        data = self.get_data(html)
        apps = []
        apps_list_data = [
            {'node': 'activeApps', 'query': 'ApplicationAndWebsitePaginatedSettingAppGridListActiveQuery', 'doc_id': '28619574884357662'},
            {'node': 'expiredApps', 'query': 'ApplicationAndWebsitePaginatedSettingAppGridListExpiredQuery', 'doc_id': '28698012099813736'}
        ]
        for base in apps_list_data:
            node = base['node']
            body = data.copy()
            body.update({'fb_api_req_friendly_name': base['query'], 'doc_id': base['doc_id']})
            end_cursor = None
            has_next_page = True
            while has_next_page:
                try:
                    body['variables'] = json.dumps({'after': end_cursor, 'first': 6, 'id': body['__user']})
                    response = self.session.post(f'{self.base}/api/graphql', headers=self.get_headers('post'), data=body).json()
                    page_info = response['data']['node'][node]['page_info']
                    has_next_page = page_info.get('has_next_page', False)
                    for edge in response['data']['node'][node]['edges']:
                        item = edge['node']['apps_and_websites_view']['detailView']
                        app_info = {
                            'id': item['app_id'],
                            'name': item['app_name'],
                            'since': datetime.fromtimestamp(int(item['install_timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                            'status': item['app_status'].lower(),
                            'picture': item['logo_url']
                        }
                        apps.append(app_info)
                    end_cursor = page_info.get('end_cursor')
                except Exception:
                    break
        return apps