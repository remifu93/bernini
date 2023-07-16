from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, is_superuser, is_staff, is_active, **extra_fields):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name, last_name, password, False, False, True, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name, last_name, password, True, True, True, **extra_fields)
