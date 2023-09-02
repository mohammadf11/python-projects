from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number , email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        if not phone_number:
            raise ValueError('Users must have an phone number')

        user = self.model(phone_number = phone_number , email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number , email, password=None):
        user = self.create_user(
            phone_number,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user