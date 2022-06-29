# Deploying_Django_To_Heroku_Tutorial

Deploying a Django App To Heroku Tutorial

* [線上 Demo 網站](https://deploy-django-twtrubiks.herokuapp.com/api/images/)

後端有一個自動爬蟲的程式去抓圖片，可參考 [auto_crawler_ptt_beauty_image](https://github.com/twtrubiks/auto_crawler_ptt_beauty_image) 。

本專案將教大家如何將自己的 [Django](https://www.djangoproject.com/) 佈署到
[Heroku](https://dashboard.heroku.com/)

[Heroku](https://dashboard.heroku.com/) 免費版本

* 可以創造 5個 app。
* 24小時一定要休息6小時的規定。
* 支援很多種程式語言。
* 有SSL ( https ) 。

更多說明請參考 [Heroku](https://dashboard.heroku.com/)

詳細的步驟可參考 [Deploying-Flask-To-Heroku](https://github.com/twtrubiks/Deploying-Flask-To-Heroku) ，

下面將只介紹佈署 [Django](https://www.djangoproject.com/) 要注意的步驟。

## 教學

我的 project_name 為 ptt_beauty_images

***設定 [Procfile](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/Procfile)***

```python
web: gunicorn ptt_beauty_images.wsgi
```

更多說明請參考

[https://devcenter.heroku.com/articles/django-app-configuration#the-basics](https://devcenter.heroku.com/articles/django-app-configuration#the-basics)

## 建議使用 WhiteNoise 佈署

***設定 Collectstatic***

Disabling Collectstatic
> heroku config:set DISABLE_COLLECTSTATIC=1

可參考 [https://devcenter.heroku.com/articles/django-assets#collectstatic-during-builds](https://devcenter.heroku.com/articles/django-assets#collectstatic-during-builds)

```cmd
pip3 install whitenoise
```

這樣靜態檔案才會正常顯示.

詳細說明可參考 [Using WhiteNoise with Django](https://whitenoise.evans.io/en/stable/django.html)

在 [settings.py](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/ptt_beauty_images/settings.py) 中加入以下東西,

***設定 ALLOWED_HOSTS***

```python
ALLOWED_HOSTS = ['*']
```

記得把 DEBUG 修改為 `False`

```python
DEBUG = False
```

設定 STATIC_ROOT

```python
STATIC_ROOT = BASE_DIR / "staticfiles"
```

設定 WhiteNoise 到 MIDDLEWARE

```python
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

Add compression

```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

最後執行 `python3 manage.py collectstatic`

如果沒有任何錯誤, 再將產生出來的東西一起 push 到 Heroku 上.

***設定 DATABASE***

[settings.py](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/ptt_beauty_images/settings.py)

我使用 Heroku Postgres ，

詳細教學可參考 [如何在 heroku 上使用 database](https://github.com/twtrubiks/Deploying-Flask-To-Heroku#%E5%A6%82%E4%BD%95%E5%9C%A8-heroku-%E4%B8%8A%E4%BD%BF%E7%94%A8-database)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}
```

請在自己 [Heroku](https://dashboard.heroku.com/) 的 Config Variables 設定 DATABASE 連線字串

![](http://i.imgur.com/KsQyZ2f.png)

## Django multiple-databases

順便介紹在  [Django](https://www.djangoproject.com/) 中的 multiple-databases，

使用方法， 將 [settings.py](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/ptt_beauty_images/settings.py) 裡的 DATABASES 修改成如下

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    },
    'db2': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME_2'),
        'USER': os.environ.get('DATABASE_USER_2'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD_2'),
        'HOST': os.environ.get('DATABASE_HOST_2'),
        'PORT': os.environ.get('DATABASE_PORT_2'),
    }
}
```

這樣就代表你有兩個 DATABASES，更多資料可參考 [Django multi-db](https://docs.djangoproject.com/en/1.11/topics/db/multi-db/#defining-your-databases)

如果要指定 DATABASES 也非常容易，

假設我今天要用 'default' 這個 DB ，可以寫這樣

```python
Image.objects.using('default').all()
```

假設我今天要用 'db2' 這個 DB，可以寫這樣

```python
Image.objects.using('db2').all()
```

有沒有發現，其實就是 using('database name') 這樣，非常簡單

更多資料可參考 [Django manually-selecting-a-database](https://docs.djangoproject.com/en/1.11/topics/db/multi-db/#manually-selecting-a-database)

## 更新 heroku stack 指令

指令如下

```cmd
heroku stack:set heroku-22 -a <app name>
```

之後再 commit push 一次就會自動 migrate 到新的 stack.

## 執行環境

* Python 3.9

## Reference

* [django-app-configuration](https://devcenter.heroku.com/articles/django-app-configuration)
* [heroku-django-template](https://github.com/heroku/heroku-django-template)
* [lazyload](https://github.com/verlok/lazyload)
* [bootstrap-sweetalert](https://github.com/lipis/bootstrap-sweetalert)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡:laughing:

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## License

MIT license
