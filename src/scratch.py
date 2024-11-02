import requests
import time

class Scratch:
    def __init__(self,user,password):
        session = requests.Session()

        response = session.get('https://scratch.mit.edu/accounts/login/')
        csrf_token = response.cookies['scratchcsrftoken']

        headers = {
            'Accept' : 'application/json',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf_token,
            'Referer': 'https://scratch.mit.edu'
        }

        payloads = {
            "username": user,
            "password":password,
            "useMessages": True
        }

        response =  session.post('https://scratch.mit.edu/accounts/login/',headers=headers,json=payloads)
        id = session.cookies.get('scratchsessionsid')


        self.id = id.replace('"','')
        self.token = csrf_token

        if response.status_code == 200:
            print("ログイン成功")
        else:
            print("ログイン失敗")

    def invite_curator(self,user, studio_id):
        url = f'https://scratch.mit.edu/site-api/users/curators-in/{studio_id}/invite_curator/?usernames={user}'

        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': self.token,
            'Referer': 'https://scratch.mit.edu'
        }

        cookies = {
           'scratchcsrftoken': self.token, 
            'scratchsessionsid': self.id
        }

        try:
            response = requests.put(url=url, cookies=cookies, headers=headers)
            response.raise_for_status()  

            print(f"Status Code: {response.status_code}")
            print(f"Status Message: {response.text}")
            if 'is already a curator of this studio' in response.text:
                print('このユーザーはすでに招待されています。')
            else:
                print(f'{user}の招待に成功しました！')
        
            return response.json() 
        except requests.RequestException as e:
            print(f"エラーが発生しました: {e}")
            return None

    def get_followers(self,username):
        base_url = f"https://api.scratch.mit.edu/users/{username}/followers"
        all_usernames = []
        offset = 0
        limit = 40  # Scratch APIは1回のリクエストで最大40件まで返します

        while True:
            url = f"{base_url}?limit={limit}&offset={offset}"
            response = requests.get(url)
        
            if response.status_code != 200:
                print(f"エラー: ステータスコード {response.status_code}")
                break

            followers = response.json()
            if not followers:
                break

        # フォロワーのusernameだけを抽出
            usernames = [follower['username'] for follower in followers]
            all_usernames.extend(usernames)
        
            offset += limit

        return all_usernames