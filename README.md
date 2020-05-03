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
