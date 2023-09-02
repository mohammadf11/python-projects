# installation
```
1. git clone git@github.com:mohammadfattahi11/blog_django.git

2. To login with Google, the following values ​​must be entered
    - SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
    - SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
    
3. Set the following values ​​for storage
       - DEFAULT_FILE_STORAGE = ''
       - AWS_S3_ACCESS_KEY_ID = ''
       - AWS_S3_SECRET_ACCESS_KEY = ''
       - AWS_STORAGE_BUCKET_NAME = ''
       - AWS_S3_ENDPOINT_URL = ''
       - AWS_S3_FILE_OVERWRITE = ''

4. cd blog_django/

5. docker-compose up -d

```

**Default Admin:**
```
username = admin
email =admin@gmail.com
password = admin
```

If you have done the steps correctly, you can see the project at [localhost](http://localhost)

