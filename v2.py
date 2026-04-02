try:
    from requests.exceptions import RequestException
    import requests, re, json, time, os, sys
    from rich.console import Console
    from rich.panel import Panel
    from rich import print as printf
    from requests.exceptions import SSLError
except (ModuleNotFoundError) as e:
    __import__('sys').exit(f"[Error] {str(e).capitalize()}!")

SUCCESS, FAILED, FOLLOWERS, STATUS, BAD, CHECKPOINT, LOGIN_FAILED, RETRY = [], [], {
    "COUNT": 0
}, [], [], [], [], []

class SENDER:

    def __init__(self) -> None:
        pass

    def SEND_FOLLOWERS(self, session, username, password, host, target_username):
        global SUCCESS, FAILED, STATUS, LOGIN_FAILED, BAD, CHECKPOINT
        session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Sec-Fetch-Mode': 'navigate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Host': '{}'.format(host),
            'Sec-Fetch-Dest': 'document',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Connection': 'keep-alive'
        })
        response = session.get('https://{}/login'.format(host))
        self.ANTI_FORGERY_TOKEN = re.search(r'"&antiForgeryToken=(.*?)";', str(response.text))
        if self.ANTI_FORGERY_TOKEN != None:
            self.TOKEN = self.ANTI_FORGERY_TOKEN.group(1)
            session.headers.update({
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Sec-Fetch-Site': 'same-origin',
                'Referer': 'https://{}/login'.format(host),
                'Sec-Fetch-Mode': 'cors',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Sec-Fetch-Dest': 'empty',
                'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()]),
                'Origin': 'https://{}'.format(host)
            })
            data = {
                'username': f'{username}',
                'antiForgeryToken': f'{self.TOKEN}',
                'userid': '',
                'password': f'{password}'
            }
            response2 = session.post('https://{}/login?'.format(host), data = data)
            self.JSON_RESPONSE = json.loads(response2.text)
            if '\'status\': \'success\'' in str(self.JSON_RESPONSE):
                session.headers.update({
                    'Referer': 'https://{}/tools/send-follower'.format(host),
                    'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()])
                })
                data = {
                    'username': f'{target_username}',
                }
                response3 = session.post('https://{}/tools/send-follower?formType=findUserID'.format(host), data = data)
                if 'name="userID"' in str(response3.text):
                    self.USER_ID = re.search(r'name="userID" value="(\d+)">', str(response3.text)).group(1)
                    session.headers.update({
                        'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()])
                    })
                    data = {
                        'userName': f'{target_username}',
                        'adet': '500',
                        'userID': f'{self.USER_ID}',
                    }
                    response4 = session.post('https://{}/tools/send-follower/{}?formType=send'.format(host, self.USER_ID), data = data)
                    self.JSON_RESPONSE4 = json.loads(response4.text)
                    if '\'status\': \'success\'' in str(self.JSON_RESPONSE4):
                        SUCCESS.append(f'{self.JSON_RESPONSE4}')
                        STATUS.append(f'{self.JSON_RESPONSE4}')
                        printf(f"[bold bright_black]   ──>[bold green] FINISH FROM {str(host).split('.')[0].upper()} SERVICE!           ", end='\r')
                        time.sleep(5.0)
                        return (True, f"Success from {host}")
                    elif '\'code\': \'nocreditleft\'' in str(self.JSON_RESPONSE4):
                        printf(f"[bold bright_black]   ──>[bold red] YOUR CREDITS HAVE RAN OUT!          ", end='\r')
                        time.sleep(4.5)
                        return (False, "Your credits have ran out!")
                    elif '\'code\': \'nouserleft\'' in str(self.JSON_RESPONSE4):
                        printf(f"[bold bright_black]   ──>[bold red] NO USERS FOUND!                     ", end='\r')
                        time.sleep(4.5)
                        return (False, "No users found!")
                    elif 'istek engellendi.' in str(self.JSON_RESPONSE4):
                        RETRY.append(f'{self.JSON_RESPONSE4}')
                        if len(RETRY) >= 3:
                            RETRY.clear()
                            printf(f"[bold bright_black]   ──>[bold red] REQUEST TO SEND FOLLOWERS BLOCKED!  ", end='\r')
                            time.sleep(4.5)
                            return (False, "Request to send followers blocked!")
                        else:
                            return self.SEND_FOLLOWERS(session, username, password, host, target_username)
                    else:
                        FAILED.append(f'{self.JSON_RESPONSE4}')
                        printf(f"[bold bright_black]   ──>[bold red] ERROR WHILE SENDING FOLLOWERS!      ", end='\r')
                        time.sleep(4.5)
                        return (False, "Error while sending followers!")
                else:
                    printf(f"[bold bright_black]   ──>[bold red] TARGET USERNAME NOT FOUND!           ", end='\r')
                    time.sleep(4.5)
                    return (False, "Target username not found!")
            elif 'Güvenliksiz giriş tespit edildi.' in str(self.JSON_RESPONSE):
                CHECKPOINT.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] YOUR ACCOUNT IS CHECKPOINT!          ", end='\r')
                time.sleep(4.5)
                return (False, "Your account is checkpoint!")
            elif 'Üzgünüz, şifren yanlıştı.' in str(self.JSON_RESPONSE):
                BAD.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] YOUR PASSWORD IS WRONG!              ", end='\r')
                time.sleep(4.5)
                return (False, "Your password is wrong!")
            else:
                LOGIN_FAILED.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] LOGIN ERROR!                          ", end='\r')
                time.sleep(4.5)
                return (False, "Login error!")
        else:
            printf(f"[bold bright_black]   ──>[bold red] FORGERY TOKEN NOT FOUND!          ", end='\r')
            time.sleep(2.5)
            return (False, "Forgery token not found!")

class INFO:

    def __init__(self) -> None:
        pass

    def GET_FOLLOWERS(self, target_username, updated):
        global FOLLOWERS
        with requests.Session() as session:
            session.headers.update({
                'User-Agent': 'Instagram 317.0.0.0.3 Android (27/8.1.0; 360dpi; 720x1280; LAVA; Z60s; Z60s; mt6739; en_IN; 559698990)',
                'Host': 'i.instagram.com',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            })
            response = session.get('https://i.instagram.com/api/v1/users/web_profile_info/?username={}'.format(target_username))
            if '"status":"ok"' in str(response.text):
                self.EDGE_FOLLOWED_BY = json.loads(response.text)['data']['user']['edge_followed_by']['count']
                if bool(updated) == True:
                    FOLLOWERS.update({
                        "COUNT": int(self.EDGE_FOLLOWED_BY)
                    })
                    return (True)
                else:
                    self.TOTAL_GAIN = (int(self.EDGE_FOLLOWED_BY) - int(FOLLOWERS['COUNT']))
                    return (f'+{self.TOTAL_GAIN} > {self.EDGE_FOLLOWED_BY}')
            else:
                if bool(updated) == True:
                    FOLLOWERS.update({
                        "COUNT": 0
                    })
                    return (False)
                else:
                    return ('-+500')

class MAIN:

    def __init__(self):
        global CHECKPOINT, BAD, LOGIN_FAILED
        try:
            self.LOGO()
            printf(Panel(f"[bold white]Please fill in your Instagram account details such as username and password, use `[bold red]:[bold white]` as a separator.\n[bold green]Example: [bold white]Username[bold black]:[bold white]Password\n[underline bold red]RECOMMENDED TO USE FAKE ACCOUNT TO LOGIN!", width=59, style="bold bright_black", title="[bold bright_black][Login Fake Account]", subtitle="[bold bright_black]╭──────", subtitle_align="left"))
            self.ACCOUNTS = Console().input("[bold bright_black]   ╰─> ")
            if ':' in str(self.ACCOUNTS):
                self.USERNAME, self.PASSWORD = self.ACCOUNTS.split(':')[0], self.ACCOUNTS.split(':')[1]
                printf(Panel(f"[bold white]Please fill in your Instagram account username, make sure the account is not locked and the\nusername is correct. Example:[bold green] @akhirro_qxzi", width=59, style="bold bright_black", title="[bold bright_black][Target's Username]", subtitle="[bold bright_black]╭──────", subtitle_align="left"))
                self.TARGET_USERNAME = Console().input("[bold bright_black]   ╰─> ").replace('@', '')
                if len(self.TARGET_USERNAME) != 0:
                    printf(Panel(f"[bold white]While sending followers, you can use[bold yellow] CTRL + C[bold white] if stuck and[bold red] CTRL + Z[bold white] if you want to stop,\nif an error occurs check the service and account!", width=59, style="bold bright_black", title="[bold bright_black][Note!]"))
                    while (True):
                        try:
                            INFO().GET_FOLLOWERS(target_username=self.TARGET_USERNAME, updated=True)
                            CHECKPOINT.clear();BAD.clear();LOGIN_FAILED.clear()
                            for HOST in ['instamoda.org', 'takipcitime.com', 'takipcikrali.com', 'bigtakip.net', 'takipcimx.net', 'fastfollow.in','anatakip.com', 'bayitakipci.com', 'takipcisatinal.com.tr', 'takipmax.com', 'takipgo.com', 'takipcizen.com', 'sosyora.com.tr', 'takipcikutusu.com', 'takipcibase.com', 'takipcigir.com', 'platintakipci.com', 'Instahile.co', 'Seritakipci.com']:
                                try:
                                    with requests.Session() as session:
                                        SENDER().SEND_FOLLOWERS(session, self.USERNAME, self.PASSWORD, HOST, self.TARGET_USERNAME)
                                        continue
                                except (SSLError):
                                    LOGIN_FAILED.append(f'{HOST}')
                                    BAD.append(f'{HOST}')
                                    CHECKPOINT.append(f'{HOST}')
                                    printf(f"[bold bright_black]   ──>[bold red] UNABLE TO CONNECT TO {str(HOST).split('.')[0].upper()} SERVICE!          ", end='\r')
                                    time.sleep(2.5)
                                    continue
                            if len(CHECKPOINT) >= 5:
                                printf(Panel(f"[bold red]Your Instagram account is hit by a checkpoint, please approve the login on another\ndevice, then try logging in again on this Program!", width=59, style="bold bright_black", title="[bold bright_black][Login Checkpoint]"))
                                sys.exit()
                            elif len(BAD) >= 5:
                                printf(Panel(f"[bold red]Your Instagram account password is incorrect, remember not all accounts can log in here,\nwe do not recommend newly created accounts!", width=59, style="bold bright_black", title="[bold bright_black][Login Failed]"))
                                sys.exit()
                            elif len(LOGIN_FAILED) >= 5:
                                printf(Panel(f"[bold red]An unknown error occurred while logging in, maybe the service is under maintenance\nor there is a problem with your Instagram account!", width=59, style="bold bright_black", title="[bold bright_black][Login Error]"))
                                sys.exit()
                            else:
                                if len(STATUS) != 0:
                                    try:
                                        self.DELAY(0, 300, self.TARGET_USERNAME)
                                        self.TOTAL = INFO().GET_FOLLOWERS(target_username=self.TARGET_USERNAME, updated=False)
                                    except (Exception):
                                        self.TOTAL = ('null')
                                    printf(Panel(f"""[bold white]Status :[bold green] Successfully sending followers![/]
[bold white]Link :[bold red] https://www.instagram.com/{str(self.TARGET_USERNAME)[:20]}
[bold white]Total :[bold yellow] {self.TOTAL}""", width=59, style="bold bright_black", title="[bold bright_black][Success]"))
                                    self.DELAY(0, 600, self.TARGET_USERNAME)
                                    STATUS.clear()
                                    continue
                                else:
                                    self.DELAY(0, 600, self.TARGET_USERNAME)
                                    continue
                        except (RequestException):
                            printf(f"[bold bright_black]   ──>[bold red] YOUR CONNECTION IS HAVING A PROBLEM!          ", end='\r')
                            time.sleep(9.5)
                            continue
                        except (KeyboardInterrupt):
                            printf(f"                               ", end='\r')
                            time.sleep(2.5)
                            continue
                        except (Exception) as e:
                            printf(f"[bold bright_black]   ──>[bold red] {str(e).upper()}!", end='\r')
                            time.sleep(5.5)
                            continue
                else:
                    printf(Panel(f"[bold red]You entered the wrong Instagram username, please check the username again,\nalso make sure the account is not locked!", width=59, style="bold bright_black", title="[bold bright_black][Username Error]"))
                    sys.exit()
            else:
                printf(Panel(f"[bold red]You did not fill in the account data correctly, make sure the username and password\nseparator is a colon, please try again!", width=59, style="bold bright_black", title="[bold bright_black][Wrong Credentials]"))
                sys.exit()
        except (Exception) as e:
            printf(Panel(f"[bold red]{str(e).capitalize()}!", width=59, style="bold bright_black", title="[bold bright_black][Error]"))
            sys.exit()

    def LOGO(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        printf(Panel(r"""             [bold red] __________   _________________
             /  _/ ____/  / ____/ ____/ ___/
             / // / __   / /_  / /_   \__ \ 
           [bold white]_/ // /_/ /  / __/ / __/  ___/ / 
          /___/\____/  /_/   /_/    /____/  
          [bold red]Instagram Followers [bold white]- [bold black]by Gueverro""", width=59, style="bold bright_black"))
        return (True)

    def DELAY(self, minutes, seconds, target_username):
        self.TOTAL = (minutes * 60 + seconds)
        while (self.TOTAL):
            MINUTES, SECONDS = divmod(self.TOTAL, 60)
            printf(f"[bold bright_black]   ──>[bold green] @{str(target_username)[:20].upper()}[bold white]/[bold green]{MINUTES:02d}:{SECONDS:02d}[bold white] SUCCESS:-[bold green]{len(SUCCESS)}[bold white] FAILED:-[bold red]{len(FAILED)}     ", end='\r')
            time.sleep(1)
            self.TOTAL -= 1
        return (True)

if __name__ == '__main__':
    try:
        # 🚀 NO PENYIMPANAN CHECK - DIRECT START! 🚀
        os.system('git pull')
        MAIN()
    except (Exception) as e:
        printf(Panel(f"[bold red]{str(e).capitalize()}!", width=59, style="bold bright_black", title="[bold bright_black][Error]"))
        sys.exit()
    except (KeyboardInterrupt):
        sys.exit()