import datetime
import os
import requests,uuid,time,json
from colorama import Fore,init
import ast
from moviepy.editor import VideoFileClip
from PIL import Image
class Main:
    def __init__(self) -> None:
        init(autoreset=True)
        self.targets = []
        self.cookies = {}
        self.shared = 0
        self.errors = 0
        self.loops = 0
        self.caption = ""
        self.uid = str(uuid.uuid4())
        self.blacklist = []

        self.login()

        # MAX 5 targets !!

    def login(self):

        x = int(input("[ 1 ] Login\n[ 2 ] Use Cookies\n==> "))
        if x == 1:
            user = str(input(Fore.LIGHTCYAN_EX +"[ + ] Username : "))
            pasw = str(input(Fore.LIGHTCYAN_EX +"[ + ] Password : "))
            headers = {
            'User-Agent':
                    'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
            "Accept-Language" : "Accept-Language",
            'Host':'i.instagram.com',
            "X-IG-Connection-Type": "WIFI",
            "X-IG-Capabilities": "3brTvw==",
            'accept-encoding': 'gzip, deflate',
            "Accept": "*/*"
            }
            data = {
                "jazoest": "22452",
                "phone_id": self.uid,
                "enc_password": "#PWD_INSTAGRAM:0:0:"+pasw,
                "username": user,
                "adid": self.uid,
                "guid": self.uid,
                "device_id": self.uid,
                "google_tokens": "[]",
                "login_attempt_count": "0"
            }
            req = requests.post('https://i.instagram.com/api/v1/accounts/login/',headers=headers,data=data)
            if req.text.__contains__("logged_in_user"):
                self.cookies = req.cookies.get_dict()
                print(Fore.LIGHTGREEN_EX + u"[ \u2713 ] Logged in successfuly")
                with open("cookies.txt",'w') as w:
                     w.write(str(self.cookies))
            elif req.text.__contains__("challenge_required") or "challenge_required" in req.text or 'challenge required' in req.text:
                self.cookies = req.cookies.get_dict()
                path = req.json()['challenge']['api_path']
                        
                info = requests.get(f"https://i.instagram.com/api/v1{path}",
                                        headers=headers, cookies=self.cookies)
                step_data = info.json()["step_data"]
                text = ""
                if "email" in step_data and "phone_number" in step_data:
                            text = text.join("[ 0 ] email \n")
                            text = text.join("[ 1 ] phone \n")
                            
                elif  "email" in step_data and not "phone_number" in step_data:
                            text = text.join("[ 0 ] email \n")
                            
                elif "phone_number" in step_data and not "email" in step_data:
                            text = text.join("[ 1 ] phone \n") 
                print(Fore.LIGHTYELLOW_EX + text)
                x = int(input(Fore.LIGHTYELLOW_EX + "[ + ] select : "))
                call = ""
                if x == 0:
                    call = "email"
                else:
                    call = "phone"
                data = {}
                if call == "phone":
                    data['choice'] = str(0)
                    data['_uuid'] = self.uid
                    data['_uid'] = self.uid
                    data['_csrftoken'] = 'massing'
                else:
                    data['choice'] = str(1)
                    data['_uuid'] = self.uid
                    data['_uid'] = self.uid
                    data['_csrftoken'] = 'massing'
                challnge = req.json()['challenge']['api_path']
                send = requests.post(f"https://i.instagram.com/api/v1{challnge}",headers=headers, data=data, cookies=self.cookies)
                contact_point = send.json()["step_data"]["contact_point"]
                print(Fore.LIGHTBLUE_EX + f'[+] code sent to : {contact_point}')
                code = str(input(Fore.LIGHTYELLOW_EX + "[ ? ] Code : "))
                data = {}
                data['security_code'] = code,
                data['_uuid'] = self.uid,
                data['_uid'] = self.uid,
                data['_csrftoken'] = 'massing'
                send_code = requests.post(f"https://i.instagram.com/api/v1{path}", headers=headers, data=data,
                                cookies=self.cookies)
                if "logged_in_user" in send_code.text:
                    self.cookies = req.cookies.get_dict()
                    print(Fore.LIGHTGREEN_EX + u"[ \u2713 ] Logged in successfuly")
                    with open("cookies.txt",'w') as w:
                        w.write(str(self.cookies))
                else:
                    print(Fore.RED+ f"[ X ] Error Logging in")
                    input()
                    exit()
            else:
                print(Fore.RED+ f"[ X ] User or password is incorrect!")
                input()
                exit()
        else:
            try:
                f = open('cookies.txt','r')
                s = f.read()
                s = s.replace('\t','')
                s = s.replace('\n','')
                s = s.replace(',}','}')
                s = s.replace(',]',']')
                s = s.replace('\'','\"')
                data = json.loads(s)
                self.cookies = data
            except Exception as w:
                print(w)
                print(Fore.RED+"[ X ] No Cookies found !")
                input()
                exit()
        self.load_targets()

    def load_targets(self):

        self.caption = open('caption.txt','r',encoding="utf-8").read()
        
        for target in open("targets.txt",'r').read().splitlines():
             
            if len(self.targets) <= 5 :

                 self.targets.append(target)

        self.sleep = int(input(Fore.LIGHTMAGENTA_EX +  "[ + ] Sleep ( 60 - 250 ) : "))     
        
        self.get_targets_last()

    def get_targets_last(self):

        print(Fore.LIGHTWHITE_EX + "[ \ ] Getting targets info please wait ..." )
         
        for target in self.targets:

            url = f'https://www.instagram.com/api/v1/feed/user/{target}/username/?count=6'

            headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
            # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',

            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'viewport-width': '1177',
            'x-asbd-id': '198387',
            'x-csrftoken': self.cookies['csrftoken'],
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
            'x-requested-with': 'XMLHttpRequest',
            }
            req = requests.get(url,headers=headers,cookies=self.cookies)

            try:
                last_media = req.json()['items'][0]['id']
                self.blacklist.append(last_media)
            except:
                 print(Fore.RED+f"[ X ] Error getting {target} post")


            time.sleep(2)
            
        if len(self.blacklist) <= 0:
             input("[ X ] Enter to exit")
             exit()
        else:
             print(Fore.LIGHTGREEN_EX + f"[ + ] Grabbed {len(self.blacklist)} info. ")
             os.system("clear || cls")
             self.start_check()

    def start_check(self):
         
        while True:
            self.loops += 1
            for target in self.targets:
                url = f'https://www.instagram.com/api/v1/feed/user/{target}/username/?count=6'

                headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',

                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'viewport-width': '1177',
                'x-asbd-id': '198387',
                'x-csrftoken': self.cookies['csrftoken'],
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                'x-requested-with': 'XMLHttpRequest',
                }
                req = requests.get(url,headers=headers,cookies=self.cookies)
                try:
                    last_media = req.json()['items'][0]['id']
                    last_media_pk = req.json()['items'][0]['pk']
                    code = req.json()['items'][0]['code']
                    media_type = int(req.json()['items'][0]['media_type'])   
                    if last_media in self.blacklist:
                        pass
                    else:
                        if media_type != 2:
                            headers = {
                            'authority': 'www.instagram.com',
                            'accept': '*/*',
                            'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                            # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',

                            'sec-ch-prefers-color-scheme': 'dark',
                            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                            'viewport-width': '1177',
                            'x-asbd-id': '198387',
                            'x-csrftoken': self.cookies['csrftoken'],
                            'x-ig-app-id': '936619743392459',
                            'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                            'x-requested-with': 'XMLHttpRequest',
                            'referer':f'https://www.instagram.com/p/{code}/',
                            'cookie':f'sessionid={self.cookies["sessionid"]}; mid={self.cookies["mid"]}'
                            }
                        else:
                             headers = {
                            'authority': 'www.instagram.com',
                            'accept': '*/*',
                            'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                            # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',

                            'sec-ch-prefers-color-scheme': 'dark',
                            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                            'viewport-width': '1177',
                            'x-asbd-id': '198387',
                            'x-csrftoken': self.cookies['csrftoken'],
                            'x-ig-app-id': '936619743392459',
                            'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                            'x-requested-with': 'XMLHttpRequest',
                            'referer':f'https://www.instagram.com/reel/{code}/',
                            'cookie':f'sessionid={self.cookies["sessionid"]}; mid={self.cookies["mid"]}'
                            }

                        url_2 = f'https://www.instagram.com/api/v1/media/{last_media_pk}/info/'
                        req_2 = requests.get(url_2,headers=headers,cookies=self.cookies)
                        media_type = int(req_2.json()['items'][0]['media_type'])   
                        
                        if media_type == 1: # PHOTOS
                            isb = self.media_1(req_2.json()['items'][0])
                            if isb:
                                self.shared += 1
                            else:
                                self.errors += 1
                            self.blacklist.append(last_media)
                            
                        if media_type == 2: # REELS AND VIDEOS
                            isb = self.media_2(req_2.json()['items'][0])
                            if isb:
                                self.shared += 1
                            else:
                                self.errors += 1
                            self.blacklist.append(last_media)
                            
                        if media_type == 8: # ALBums
                            isb = self.media_8(req_2.json()['items'][0])
                            if isb:
                                self.shared += 1
                            else:
                                self.errors += 1
                            self.blacklist.append(last_media)
                            
                except Exception as w:
                     print(w)
                     print(Fore.RED+f"[ X ] Error getting {target} post")

                print(f" {Fore.LIGHTCYAN_EX}[ {Fore.LIGHTWHITE_EX}Loops : {Fore.LIGHTCYAN_EX}{self.loops} {Fore.LIGHTWHITE_EX}, {Fore.LIGHTWHITE_EX}Shared : {Fore.LIGHTGREEN_EX}{self.shared} {Fore.LIGHTWHITE_EX}, {Fore.LIGHTWHITE_EX}Errors : {Fore.RED}{self.shared} {Fore.LIGHTCYAN_EX}]", end='\r')

                time.sleep(5)
            time.sleep(self.sleep)

    def generate_upload_id(self,somefile):
        upload_id = str(int(time.time()))  # e.g : 1524115561404
        milieu = '_0_'
        hashcode = str(hash(os.path.basename(somefile))) # e.g : 363954952
        final = upload_id + milieu + str(hashcode)  # e.g : # 1524115561404_0_363954952
        return upload_id, hashcode, final
    
    def media_8(self,jsinfo) -> bool:
        headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'viewport-width': '1177',
                'x-asbd-id': '198387',
                'x-csrftoken': self.cookies['csrftoken'],
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                'x-requested-with': 'XMLHttpRequest',
        }

        items = []
        upload_ids = []

        for item in jsinfo['carousel_media']:
             items.append(item)
        print(len(items))
        i = 0
        
        while i < len(items):
            
            media_type = items[i]['media_type']
            if media_type == 1:
                upload_id = int(time.time())
                upload_ids.append({"upload_id":f"{upload_id}"})
                # upload_ids.append({"upload_id":str(upload_id),"source_type":"4","scene_type":'null',"scene_capture_type":"","date_time_digitalized":"2023:04:09 18:19:51","camera_make":"Google","camera_model":"sdk_gphone_x86","timezone_offset":"10800","nav_chain":"SelfFragment:self_profile:9:main_profile:1681053584.951::,ProfileMediaTabFragment:self_profile:10:button:1681053585.441::,UniversalCreationMenuFragment:universal_creation_menu:11:button:1681053586.170::,ProfileMediaTabFragment:self_profile:12:button:1681053587.781::,MediaCaptureFragment:tabbed_gallery_camera:13:button:1681053587.858::,MediaCaptureFragment:tabbed_gallery_camera:15:button:1681053596.208::,AlbumEditFragment:carousel_gallery:17:button:1681053613.73::","edits":"{\"crop_original_size\":[1280.0,960.0],\"crop_center\":[0.0,-0.0],\"crop_zoom\":1.3333334}","extra":"{\"source_width\":1280,\"source_height\":960}","device":"{\"manufacturer\":\"Google\",\"model\":\"sdk_gphone_x86\",\"android_version\":30,\"android_release\":\"11\"}"})
                image_url = items[i]['image_versions2']['candidates'][0]['url']
                width = items[i]['image_versions2']['candidates'][0]['width']
                height = items[i]['image_versions2']['candidates'][0]['height']
                
                image_data = requests.get(image_url,headers=headers,cookies=self.cookies).content
                content_length = len(image_data)
                rupload = json.dumps({"media_type":1,"upload_id":f"{upload_id}","upload_media_height":width,"upload_media_width":height})
                headers = {
                    'authority': 'i.instagram.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                    'content-type': 'image/jpeg',
                    # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYfsj22L3q_3UzcQ8OVxzFIpd0lQsIktZz7A10Dx4aw; rur="LDC\\05458089752643\\0541712482505:01f7e8bbb3314f20702bea66f8077fa5752845ecefc534a418dbdcf961aaf0e98abdbf91"',
                    'offset': '0',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/',
                    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                    'x-asbd-id': '198387',
                    'x-entity-length': str(content_length),
                    'x-entity-name': f'fb_uploader_{upload_id}',
                    'x-entity-type': 'image/jpeg',
                    'x-ig-app-id': '936619743392459',
                    'x-instagram-ajax': '1007275066',
                    'x-instagram-rupload-params': rupload,
                }

                first_req = requests.post(f'https://www.instagram.com/rupload_igphoto/fb_uploader_{upload_id}',headers=headers,data=image_data,cookies=self.cookies)
                
               
            i+=1
        
        if len(upload_ids) > 0 :

            url = 'https://www.instagram.com/api/v1/media/configure_sidecar/'
            headers = {
                    'authority': 'www.instagram.com',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                    # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                    'viewport-width': '1177',
                    'x-asbd-id': '198387',
                    'x-csrftoken': self.cookies['csrftoken'],
                    'x-ig-app-id': '936619743392459',
                    'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                    'x-requested-with': 'XMLHttpRequest',
                    'content-type': 'application/json'

            }

            data = json.dumps({"source_type":"library","caption":f"{self.caption}","disable_comments":"0","like_and_view_counts_disabled":0,"children_metadata":upload_ids,"client_sidecar_id":str(int(time.   time()))})
        

            response = requests.post(
                url,
                                cookies=self.cookies,
                                headers=headers,
                                data=data,
                            )
            
            if response.text.__contains__('"status":"ok"'):
                return True
            else:
                return False
        
        else:
             
             return False


    def media_2(self,jsinfo) -> bool:
        headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'viewport-width': '1177',
                'x-asbd-id': '198387',
                'x-csrftoken': self.cookies['csrftoken'],
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                'x-requested-with': 'XMLHttpRequest',
        }

        video_url = jsinfo['video_versions'][0]['url']
        req_video = requests.get(video_url,headers=headers,cookies=self.cookies)
        with open(f'temp.mp4','wb') as w:
            w.write(req_video.content)
        upload_idonly, hashcode, upload_idforurl = self.generate_upload_id('temp.mp4')
        filesize = str(os.path.getsize('temp.mp4'))
        clip = VideoFileClip('temp.mp4')
        videoduration =int(clip.duration*1000)
        arrayn = clip.get_frame((videoduration/1000)-1)
        image = Image.fromarray(arrayn)
        p = os.path.join("ss.jpeg")
        image.save(p)
        bytesi = image.tobytes()

        url = f"https://i.instagram.com/rupload_igvideo/{upload_idforurl}"
        XInstagramRuploadParams = json.dumps({"upload_media_height":"1280","xsharing_user_ids":"[]","upload_media_width":"720","is_clips_video":"1","upload_media_duration_ms":str(videoduration),"content_tags":"use_default_cover","upload_id":str(upload_idonly),"retry_context":"{\"num_reupload\":0,\"num_step_auto_retry\":0,\"num_step_manual_retry\":0}","media_type":"2"
                                    })
        headers = {
            "X-Entity-Length": filesize,
            "X-Entity-Name": upload_idforurl,
            "X-Instagram-Rupload-Params":XInstagramRuploadParams,
            'X-Entity-Type': 'video/mp4',
            'Segment-Start-Offset':'0',
            'User-Agent': 'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(filesize),
            'X_FB_VIDEO_WATERFALL_ID': str(uuid.uuid4()),
            "Offset": '0'
        }

        file_bytes = open('temp.mp4', 'rb').read()

        req = requests.post(url,headers=headers,data=file_bytes,cookies=self.cookies)


        byte_image = open("ss.jpeg","rb").read()

        url = f"https://i.instagram.com/rupload_igphoto/{upload_idforurl}"
        Ruploadparams2 = json.dumps({"upload_id":str(upload_idonly),"media_type":"2","retry_context":"{\"num_reupload\":0,\"num_step_auto_retry\":0,\"num_step_manual_retry\":0}","image_compression":"{\"lib_name\":\"moz\",\"lib_version\":\"3.1.m\",\"quality\":\"0\",\"original_width\":720,\"original_height\":1280}","xsharing_user_ids":"[]"}
                                            )
        headers = {
            "x_fb_photo_waterfall_id":str(uuid.uuid4()),
            'X-Instagram-Rupload-Params':Ruploadparams2,
            'X-Entity-Type': 'image/jpeg',
            'X-Entity-Length': str(len(byte_image)),
            'X-Entity-Name':upload_idforurl,
            'Content-Length' : str(len(byte_image)),
            'Connection': 'keep-alive',
 
            'X-IG-App-ID': "936619743392459",
 
            'Offset': '0',                            
            'X-CSRFToken':'missing',
 
            'Accept': '*/*',
            'User-Agent': 'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'Accept-Language': 'en-US',
        }
        req = requests.post(url,headers=headers,data=byte_image,cookies=self.cookies)

        clip = VideoFileClip('temp.mp4')
        duration = clip.duration
        videoduration =int(clip.duration*1000)
        
        url="https://i.instagram.com/api/v1/media/configure_to_clips/?video=1"
        headers = {
            'Host': 'i.instagram.com',
            'X-Ig-App-Locale': 'en_US',
            'X-Ig-Device-Locale': 'en_US',
            'X-Ig-Mapped-Locale': 'en_US',
            'X-Pigeon-Session-Id': 'UFS-972db085-f1be-4614-9e32-77bc451fc68e-0',
            'X-Pigeon-Rawclienttime': '1680967642.506',
            'X-Ig-Bandwidth-Speed-Kbps': '4330.000',
            'X-Ig-Bandwidth-Totalbytes-B': '2809082',
            'X-Ig-Bandwidth-Totaltime-Ms': '443',
            'X-Ig-App-Startup-Country': 'IQ',
            'X-Bloks-Version-Id': '0ee04a4a6556c5bb584487d649442209a3ae880ae5c6380b16235b870fcc4052',
            'X-Ig-Www-Claim': 'hmac.AR1aWEsDw6WfWexHDkfbg_-temKojpBG0NZXzjGWwnoWoqev',
            'X-Bloks-Is-Layout-Rtl': 'false',
            'X-Ig-Device-Id': '3c2bc696-a663-4ba9-b79b-9edfbd1ddda6',
            'X-Ig-Family-Device-Id': 'e213d380-6ece-4c19-817f-9dc0afe83b21',
            'X-Ig-Android-Id': 'android-2586199b6b109939',
            'X-Ig-Timezone-Offset': '10800',
            'X-Ig-Nav-Chain': 'SelfFragment:self_profile:2:main_profile:1680967603.121::,UniversalCreationMenuFragment:universal_creation_menu:3:button:1680967604.743::,ProfileMediaTabFragment:self_profile:4:button:1680967606.64::,TRUNCATEDx2,ClipsCameraFragment:clips_precapture_camera:7:button:1680967611.548::,VideoViewController:clips_postcapture_camera:8:button:1680967622.407::,ClipsShareHomeFragment:clips_share_sheet:9:button:1680967634.713::,ClipsShareSheetFragment:clips_share_sheet:10:button:1680967634.806::,OptimizedNuxFragment:ig_camera_clips_optimized_nux:11:button:1680967638.972::,IgCameraViewController:reel_composer_camera:12:button:1680967640.420::,ClipsViewerFragment:clips_viewer_clips_tab:13:clips_tab:1680967641.370::',
            'X-Ig-Salt-Ids': '51052545',
            'Is_clips_video': '1',
            'Retry_context': '{"num_reupload":0,"num_step_auto_retry":0,"num_step_manual_retry":0}',
            'X-Fb-Connection-Type': 'WIFI',
            'X-Ig-Connection-Type': 'WIFI',
            'X-Ig-Capabilities': '3brTv10=',
            'X-Ig-App-Id': '567067343352427',
            'Priority': 'u=3',
            'User-Agent': 'Instagram 265.0.0.19.301 Android (30/11; 420dpi; 1080x1794; Google/google; sdk_gphone_x86; generic_x86_arm; ranchu; en_US; 436384447)',
            'Accept-Language': 'en-US',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Fb-Http-Engine': 'Liger',
            'X-Fb-Client-Ip': 'True',
            'X-Fb-Server-Cluster': 'True',
        }


        #data = 'signed_body=SIGNATURE.{"app_attribution_android_namespace":"","clips_share_preview_to_feed":"1","is_clips_edited":"0","camera_entry_point":"71","is_created_with_sound_sync":"0","filter_type":"0","camera_session_id":"c751e789-1008-46bf-89c2-91dea8046fc3","timezone_offset":"10800","usertags":"{\"in\":[]}","source_type":"4","video_result":"","_uid":"54057313079","device_id":"android-dc6785c6964b3dbe","_uuid":"ed0e63e9-1663-4c54-b150-40d726c30a87","caption":"'+self.caption+'","date_time_original":"19040101T000000.000Z","capture_type":"clips_v2","upload_id":"'+upload_idonly+'","additional_audio_info":{"has_voiceover_attribution":"0"},"device":{"manufacturer":"samsung","model":"SM-G780F","android_version":30,"android_release":"11"},"length":'+str(duration)+',"clips":[{"length":'+str(duration)+',"source_type":"4","camera_position":"back"}],"extra":{"source_width":720,"source_height":1280},"audio_muted":false,"poster_frame_index":0,"clips_segments_metadata":{"num_segments":1,"clips_segments":[{"index":0,"face_effect_id":null,"speed":100,"source":"library","duration_ms":'+str(videoduration)+',"audio_type":"music_selection","from_draft":"0","camera_position":-1,"media_folder":null,"media_type":"video","original_media_type":"video"}]},"clips_audio_metadata":{"original":{"volume_level":0.0},"song":{"volume_level":1.0,"is_saved":"0","artist_name":"'+self.artict+'","audio_asset_id":"'+self.audio_id+'","audio_cluster_id":"'+self.arid+'","track_name":"'+self.title+'"}},"music_params":{"is_picked_precaptureaudio_asset_id":"'+self.audio_id+'","audio_cluster_id":"'+self.arid+'","audio_asset_start_time_in_ms":15000,"derived_content_start_time_in_ms":0,"overlap_duration_in_ms":15000,"browse_session_id":"8f45066a-ce2c-41f1-9bf4-75434d0cf741","product":"story_camera_clips_v2","song_name":"'+self.title+'","artist_name":"'+self.artict+'"}}'
        data = 'signed_body=SIGNATURE.{"clips_share_preview_to_feed":"1","is_shared_to_fb":"0","is_clips_edited":"0","like_and_view_counts_disabled":"0","camera_entry_point":"71","is_created_with_sound_sync":"0","filter_type":"0","camera_session_id":"5879bbec-d41a-4dd5-95b4-a651cc5b18f1","disable_comments":"0","clips_creation_entry_point":"clips","timezone_offset":"10800","source_type":"3","camera_position":"unknown","video_result":"","is_created_with_contextual_music_recs":"0","_uid":"58089752643","device_id":"android-2586199b6b109939","_uuid":"3c2bc696-a663-4ba9-b79b-9edfbd1ddda6","nav_chain":"SelfFragment:self_profile:2:main_profile:1680967603.121::,UniversalCreationMenuFragment:universal_creation_menu:3:button:1680967604.743::,ProfileMediaTabFragment:self_profile:4:button:1680967606.64::,ProfileMediaTabFragment:self_profile:5:button:1680967606.562::,ClipsCameraFragment:clips_precapture_camera:6:button:1680967607.8::,ClipsCameraFragment:clips_precapture_camera:7:button:1680967611.548::,VideoViewController:clips_postcapture_camera:8:button:1680967622.407::,ClipsShareHomeFragment:clips_share_sheet:9:button:1680967634.713::","caption":"'+self.caption+'","video_subtitles_enabled":"1","capture_type":"clips_v2","enable_smart_thumbnail":"0","audience":"default","upload_id":"'+upload_idonly+'","template_clips_media_id":"null","is_creator_requesting_mashup":"0","is_template_disabled":"0","additional_audio_info":{"has_voiceover_attribution":"0"},"device":{"manufacturer":"Google","model":"sdk_gphone_x86","android_version":30,"android_release":"11"},"length":'+str(duration)+',"clips":[{"length":'+str(duration)+',"source_type":"3","camera_position":"back"}],"extra":{"source_width":1080,"source_height":1920},"audio_muted":false,"poster_frame_index":0,"clips_segments_metadata":{"num_segments":1,"clips_segments":[{"index":0,"face_effect_id":null,"speed":100,"source_type":"1","duration_ms":'+str(videoduration)+',"audio_type":"original","from_draft":"0","camera_position":1,"media_folder":null,"media_type":"video","original_media_type":2}]},"clips_audio_metadata":{"original":{"volume_level":1.0}}}'

        req = requests.post(url,headers=headers,data=data,cookies=self.cookies)
        if req.text.__contains__('"status":"ok"'):
             os.remove('temp.mp4')
             os.remove('ss.jpeg')
             return True
        else:
             os.remove('temp.mp4')
             os.remove('ss.jpeg')
             return False
        
    

    def media_1(self,jsinfo) -> bool:
        headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'viewport-width': '1177',
                'x-asbd-id': '198387',
                'x-csrftoken': self.cookies['csrftoken'],
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                'x-requested-with': 'XMLHttpRequest',
        }
        image_url = jsinfo['image_versions2']['candidates'][0]['url']


        image_data = requests.get(image_url,headers=headers,cookies=self.cookies).content

        upload_id = int(time.time())

        content_length = len(image_data)


        rupload = json.dumps({"media_type":1,"upload_id":f"{upload_id}","upload_media_height":1280,"upload_media_width":1280})

        headers = {
            'authority': 'i.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
            'content-type': 'image/jpeg',
            # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYfsj22L3q_3UzcQ8OVxzFIpd0lQsIktZz7A10Dx4aw; rur="LDC\\05458089752643\\0541712482505:01f7e8bbb3314f20702bea66f8077fa5752845ecefc534a418dbdcf961aaf0e98abdbf91"',
            'offset': '0',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'x-asbd-id': '198387',
            'x-entity-length': str(content_length),
            'x-entity-name': f'fb_uploader_{upload_id}',
            'x-entity-type': 'image/jpeg',
            'x-ig-app-id': '936619743392459',
            'x-instagram-ajax': '1007275066',
            'x-instagram-rupload-params': rupload,
        }

        first_req = requests.post(f'https://i.instagram.com/rupload_igphoto/fb_uploader_{upload_id}',headers=headers,data=image_data,cookies=self.cookies)
        if 'upload_id' in first_req.text:
            data = {
                'source_type': 'library',
                'caption': self.caption,
                'upload_id': str(upload_id),
                'disable_comments': '0',
                'like_and_view_counts_disabled': '0',
                'igtv_share_preview_to_feed': '1',
                'is_unified_video': '1',
                'video_subtitles_enabled': '0',
                'disable_oa_reuse': 'false',
            }
            headers = {
                'authority': 'www.instagram.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
                # 'cookie': 'ig_nrcb=1; ig_did=0E5AC6D4-F61A-44B1-8166-321323BCB56A; mid=Y2kaBgALAAEAf8q8wYiNxSk9N6bT; datr=ARxpY-vIL8kl-C461hRI3gon; fbm_124024574287414=base_domain=.instagram.com; csrftoken=cGhsy16ZVcgwH3l6HOsFG5Ui9PIIQ9as; ds_user_id=58089752643; sessionid=58089752643%3AHMqbzH6yURcQ3K%3A5%3AAYcenJ0tgg7krlydleKL4yHXz3zVkIwzgMXnlsVWcTM; rur="NAO\\05458089752643\\0541712436727:01f76d5412f13baea95303666331f02d54c42603d0de66961771c50ed2d3db5d36b0ff87"',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent':  'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'viewport-width': '1177',
                'x-asbd-id': '198387',
                'x-csrftoken': self.cookies['csrftoken'],
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR2PZD5QJYSgEIps_RpaIL6mkNrlYQaIZc3Nb25H4Wdn-VjN',
                'x-requested-with': 'XMLHttpRequest',
                'content-type': 'application/x-www-form-urlencoded',
                'viewport-width': '1196',
                'x-asbd-id': '198387',
                'x-instagram-ajax': '1007275066',
            }
            req_2 = requests.post('https://www.instagram.com/api/v1/media/configure/',headers=headers,data=data,cookies=self.cookies)
            if '"status":"ok"' in req_2.text:
                 return True
            else:
                 return False
        else:
             return False
        


             

        

if __name__ == "__main__":
    init(autoreset=True)
    os.system('color')
    os.system("cls||clear")
    text= f"""
{Fore.LIGHTCYAN_EX}  .d8888b.  888                             8888888b.                   888                               
{Fore.LIGHTCYAN_EX} d88P  Y88b 888                             888   Y88b                  888                               
{Fore.LIGHTCYAN_EX} 888    888 888                             888    888                  888                               
{Fore.LIGHTCYAN_EX} Y88b. d888 88888b.   .d88b.   8888b.       888   d88P .d88b.  .d8888b  88888b.   8888b.  888d888 .d88b.  
{Fore.LIGHTCYAN_EX}  "Y888P888 888 "88b d8P  Y8b     "88b      8888888P" d8P  Y8b 88K      888 "88b     "88b 888P"  d8P  Y8b 
{Fore.LIGHTCYAN_EX}        888 888  888 88888888 .d888888      888 T88b  88888888 "Y8888b. 888  888 .d888888 888    88888888 
{Fore.LIGHTCYAN_EX} Y88b  d88P 888  888 Y8b.     888  888      888  T88b Y8b.          X88 888  888 888  888 888    Y8b.     
{Fore.LIGHTCYAN_EX}  "Y8888P"  888  888  "Y8888  "Y888888      888   T88b "Y8888   88888P' 888  888 "Y888888 888     "Y8888  
                                                                                       
{Fore.LIGHTRED_EX}                | Instagram Reshare bot by @9hea.
{Fore.LIGHTRED_EX}                | Auto resharing Reels, Posts , Stories.
{Fore.LIGHTRED_EX}                | Using multiple targets.
{Fore.LIGHTRED_EX}                | Automatic Sleep.
{Fore.LIGHTRED_EX}                | Telegram Channel t.me/XMurder                                                                                         
        """
    print(text)
    Main()
