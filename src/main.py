import requests
import time
from scratch import Scratch


if __name__ == "__main__":
    username = "kairisky"
    password = "s1722108"

    sc = Scratch('kairisky','s1722108')
    users = sc.get_followers('kairisky')
    users.sort()

    for user in users:
        sc.invite_curator(user,35841742)
        time.sleep(2)
        print('test')