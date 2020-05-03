# tuky
.تاکی , سرویس کوتاه کننده لینک با قابلیت ایجاد لینک کوتاه با رمز عبور و آدرس دلخواه, حذف لینک, ویرایش لینک, و مشاهده آمار دقیق کلیک

# how to run
1 - clone the repo:
```bash
git clone https://github.com/erfanhs/tuky.git
cd tuky
```
2 - install virtual environment and project requirements:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3 - configure settings.py (don't forget to config [reCAPTCHA](https://www.google.com/recaptcha/)):
```bash
nano urlShortner/settings.py
```
4 - make migrations and migrate:
```bash
python manage.py makemigrations
python manage.py migrate
```
5 - run server:
```bash
python manage.py runserver
```

# API DOCS

- Authentication:

  Security Scheme Type: Api Token
  
  Header parameter name: Authorization
  
- Links:
  - Create a short link:
  
    method: POST 
    
    route: /api/v1/links/ 
    
    required fields: long_url
    
    optional fields: url_id, password, expiration_date
    
    example data: {"long_url": "https://google.com", "url_id": "google", "password": "123", "expiration_date": "2020/05/12"}


