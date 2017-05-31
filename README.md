# Deploying_Django_To_Heroku_Tutorial

Deploying a Django App To Heroku Tutorial

* [線上 Demo 網站](https://ptt-beauty-images.herokuapp.com/)

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

***設定 ALLOWED_HOSTS***

[settings.py](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/ptt_beauty_images/settings.py)

```python
ALLOWED_HOSTS = ['*']
```

***設定 Static assets and file serving***

[settings.py](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/ptt_beauty_images/settings.py)

```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


```

更多說明請參考
[https://devcenter.heroku.com/articles/django-app-configuration#static-assets-and-file-serving](https://devcenter.heroku.com/articles/django-app-configuration#static-assets-and-file-serving)

***設定 Whitenoise***

[settings.py](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/ptt_beauty_images/settings.py)

```python
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

```

[wsgi.py](https://github.com/twtrubiks/Deploying_Django_To_Heroku_Tutorial/blob/master/ptt_beauty_images/wsgi.py)

```python
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

```

更多說明請參考 [https://devcenter.heroku.com/articles/django-app-configuration#whitenoise](https://devcenter.heroku.com/articles/django-app-configuration#whitenoise)

***設定 Collectstatic***

Disabling Collectstatic
> heroku config:set DISABLE_COLLECTSTATIC=1

更多說明請參考

[https://devcenter.heroku.com/articles/django-assets#collectstatic-during-builds](https://devcenter.heroku.com/articles/django-assets#collectstatic-during-builds)

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
    '': {
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

## 特色

* 使用 [lazyload](https://github.com/verlok/lazyload) 載入大量圖片。

* 圖片來源為爬蟲，可參考 [auto_crawler_ptt_beauty_image](https://github.com/twtrubiks/auto_crawler_ptt_beauty_image) 。

## 安裝套件

確定電腦有安裝 [Python](https://www.python.org/) 之後

請在  cmd  ( 命令提示字元 ) 輸入以下指令

```cmd
pip install -r requirements.txt
```

## 執行畫面

首頁

![](http://i.imgur.com/Ul9qrkN.png)

滑鼠游標移到圖片上，可刪除圖片

![](http://i.imgur.com/nSuslHP.png)

## 執行環境

* Python 3.6.0

## Reference

* [django-app-configuration](https://devcenter.heroku.com/articles/django-app-configuration)
* [heroku-django-template](https://github.com/heroku/heroku-django-template)
* [lazyload](https://github.com/verlok/lazyload)
* [bootstrap-sweetalert](https://github.com/lipis/bootstrap-sweetalert)

## License

MIT license
