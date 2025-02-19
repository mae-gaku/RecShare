# RecShare
A service to share shop recommendations with various people.

![image](https://github.com/user-attachments/assets/d9758762-1bb5-4969-97bc-45d7f2f772b4)



# Setup

1. git clone
```
git clone https://github.com/mae-gaku/RecShare.git
cd RecShare
```

2. install
```
pip install -r requirements.txt
```

3. migrate
```
python3 manage.py makemigrations
python3 manage.py migrate

```

4. run
```
python3 manage.py runserver 8000
```

5. access
```
http://127.0.0.1:8000/
```


※ create superuser
```
python3 manage.py createsuperuser
```
