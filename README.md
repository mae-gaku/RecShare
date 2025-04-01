<h1 align="center">RecShare</h1>


<p align="center">A service to share shop recommendations with various people.</p>

<p align="center">
  <a href="https://github.com/mae-gaku/RecShare/releases"><img src="https://img.shields.io/github/v/release/mae-gaku/RecShare?style=flat-square" alt="Version"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square" alt="License"></a>

</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/d9758762-1bb5-4969-97bc-45d7f2f772b4" alt="Recshare Logo" width="700">
</p>

---

## ToDo
- [ ] LLMによるレコメンド機能
- [ ] お店詳細ページのUI修正
- [ ] RecShareロゴ画像作成

      
---

## Setup

### 1. Clone Repository
```
git clone https://github.com/mae-gaku/RecShare.git
cd RecShare
```

### 2. Install
```
pip install -r requirements.txt
```

### 3. migrate

```
python3 manage.py makemigrations
python3 manage.py migrate
```

### 4. Run

```
python3 manage.py runserver 8000
```

### 5. Access
```
http://127.0.0.1:8000/
```

※ create superuser
```
python3 manage.py createsuperuser
```
