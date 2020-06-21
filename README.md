# tuky
.تاکی , سرویس کوتاه کننده لینک با قابلیت ایجاد لینک کوتاه با رمز عبور و آدرس دلخواه, حذف لینک, ویرایش لینک, و مشاهده آمار دقیق کلیک

![Alt text](https://img.techpowerup.org/200621/view.png "Main Page")

# how to run

Tested on python 3.6 and 3.7

1 - clone the repo:
```bash
git clone https://github.com/erfanhs/tuky.git
```
2 - install virtual environment and project requirements:
```bash
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
cd tuky
pip install -r requirements.txt
```
3 - configure settings.py (don't forget to config [reCAPTCHA](https://www.google.com/recaptcha/)):
```bash
nano urlShortner/settings.py
```
4 - make migrations and migrate:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
5 - run server:
```bash
python3 manage.py runserver
```

# API

- Authentication:

    Security Scheme Type: Api Token
    
    Header parameter name: Authorization
    
    get api token:<br/>
    1 - first login with your account: [login](http://tuky.ir/registration)<br/>
    2 - get api token from your account settings page: [settings](http://tuky.ir/settings)<br/>
    
    You must send this header with all your requests:
    ```javascript
    { "Authorization": "YOUR-API-TOKEN" }
    ```
  
- Links:

  Important: for POST & PUT methods, append slash to url is required. Otherwise, the GET request will be considered !

  - Create a short link:
  
      method: POST<br/>
      route: /api/v1/links/<br/>
      required fields: long_url<br/>
      optional fields: url_id, password, expiration_date<br/>
      **long_url**: String (starts with http:// or https://)<br/>
      **url_id**: String (max 65 char)<br/>
      **password**: String<br/>
      **expiration_date**: String (syntax: yy/mm/dd)<br/>
      you must send these fields as **form-data**
      
   - Get list of links
   
      method: GET<br/>
      route: /api/v1/links/<br/>
      required fields: -<br/>
      optional fields: search, limit, skip, all<br/>
      **search**: String (a keyword to search in url id and long urls)<br/>
      **limit**: String (numerical)<br/>
      **skip**: String (numerical)<br/>
      **all**: String ("false" or "0")<br/>
      you must send these fields as **GET Request parameters**<br/>
      **example**: http://tuky.ir/api/v1/links?limit=15&skip=20&all=false&search=instagram
      
      
    - Delete all links
    
      method: DELETE<br/>
      route: /api/v1/links/
      
    - Get link details
    
      method: GET<br/>
      route: /api/v1/links/[url_id]

    - delete a link
      
      method: DELETE<br/>
      route: /api/v1/links/[url_id]/
    
    - edit a link
      
      method: PUT<br/>
      route: /api/v1/links/[url_id]/<br/>
      optional fields: url_id, expiration_date, long_url<br/>
      **long_url**: String (starts with http:// or https://)<br/>
      **url_id**: String (max 65 char)<br/>
      **expiration_date**: String (syntax: yy/mm/dd)<br/>
      you must send these fields as **form-data**
    
    - get link stats
      
      method: GET<br/>
      route: /api/v1/links/[url_id]/stats

# License

[MIT](https://github.com/erfanhs/tuky/blob/master/LICENSE)
