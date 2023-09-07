from django.contrib.auth.models import BaseUserManager, Group

from user.api.utils import get_random_password


class CustomUserManager(BaseUserManager):
    user_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        admins = Group.objects.get(name="admins")
        authors = Group.objects.get(name="authors")
        users = Group.objects.get(name="users")
        if extra_fields.get("role") == "Admin":
            if password is None:
                admin_password = "1234"
                user.password = admin_password
            else:
                user.password = password
            user.raw_password = user.password
            user.set_password(user.password)
            user.save(using=self._db)
            admins.user_set.add(user)
        elif extra_fields.get("role") == "Author":
            user.password = get_random_password()
            user.raw_password = user.password
            user.set_password(user.password)
            user.save(using=self._db)
            authors.user_set.add(user)
        elif extra_fields.get("role") == "User":
            user.password = get_random_password()
            user.raw_password = user.password
            user.set_password(user.password)
            user.save(using=self._db)
            users.user_set.add(user)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "Admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)
