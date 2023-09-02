from django.contrib.auth.models import BaseUserManager

#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, name, password=None, password2=None):
        if not email:
            raise ValueError('User must have an email address')

        if not phone_number:
            raise ValueError('User must have an phone number')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, name, password=None):
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user
