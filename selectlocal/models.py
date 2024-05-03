# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class userhh(models.Model):
    Id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    accout = models.CharField(max_length=100, blank=True, null=True)
    passwords = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    userImg = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=100, blank=True, null=True)
    personaltypy = models.CharField(max_length=600, blank=True, null=True)
    rotue = models.CharField(max_length=100, blank=True, null=True)
    frinds = models.CharField(max_length=100, blank=True, null=True)
    coommit = models.CharField(max_length=100, blank=True, null=True)
    love = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'userhh'

class pointshh(models.Model):
    Id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    accout = models.CharField(max_length=100, blank=True, null=True)
    img1 = models.CharField(max_length=100, blank=True, null=True)
    img2 = models.CharField(max_length=100, blank=True, null=True)
    userImg = models.CharField(max_length=100, blank=True, null=True)
    img3 = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=600, blank=True, null=True)
    titledetail = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pointshh'

class Cityserc(models.Model):
    Id = models.BigAutoField(primary_key=True)
    cityName = models.CharField(max_length=100, blank=True, null=True)
    timess = models.CharField(max_length=600, blank=True, null=True)
    routerss = models.CharField(max_length=600, blank=True, null=True)
    routerdays = models.CharField(max_length=100, blank=True, null=True)
    routerdaysName = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Cityserc'

class Pointss(models.Model):
    Id = models.BigAutoField(primary_key=True)
    cityName = models.CharField(max_length=100, blank=True, null=True)
    reasons = models.CharField(max_length=1600, blank=True, null=True)
    score = models.CharField(max_length=100, blank=True, null=True)
    timers = models.CharField(max_length=600, blank=True, null=True)
    cityimg = models.CharField(max_length=600, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Pointss'

class CityTepyFour(models.Model):
    Id = models.BigAutoField(primary_key=True)
    cityName = models.CharField(max_length=100, blank=True, null=True)
    HotelPoints = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CityTepyFour'

class Hotel(models.Model):
    cityId = models.BigAutoField(primary_key=True)
    cityTip = models.CharField(max_length=160, blank=True, null=True)
    cityName = models.CharField(max_length=460)
    HotelName = models.CharField(max_length=60)
    Hotelslocal = models.CharField(max_length=160, blank=True, null=True)
    Hotelsscore = models.CharField(max_length=100, blank=True, null=True)
    Hotelsmoney = models.CharField(max_length=300, blank=True, null=True)
    Hotelsytype = models.CharField(max_length=300, blank=True, null=True)
    Hotelfherf = models.CharField(max_length=50, blank=True, null=True)
    Hotelfimg = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Hotal'

class City(models.Model):
    Id = models.BigAutoField(primary_key=True)
    imgUrl = models.CharField(max_length=160, blank=True, null=True)
    cityName = models.CharField(max_length=460, blank=True, null=True)
    selectId = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'City'

class wantGo(models.Model):
    cityId = models.BigAutoField(primary_key=True)
    imgUrl = models.CharField(max_length=60, blank=True, null=True)
    cityName = models.CharField(max_length=60   , blank=True, null=True)
    selectId = models.IntegerField(max_length=6, blank=True, null=True )
    class Meta:
        managed = False
        db_table = 'want_go'
class xxRuter(models.Model):
    cityId = models.BigAutoField(primary_key=True)
    daysun = models.IntegerField()
    daynumber = models.IntegerField()
    title = models.CharField(max_length=160)
    titledetail = models.CharField(max_length=460)
    suitpeople = models.CharField(max_length=60)
    suitmonth = models.CharField(max_length=60)
    roter = models.CharField(max_length=160)
    roterdetail = models.CharField(max_length=1000, blank=True, null=True)
    daynHref = models.CharField(max_length=300)
    roterImg = models.CharField(max_length=1000, blank=True, null=True)
    fooddetail = models.CharField(max_length=1000, blank=True, null=True)
    foodImg = models.CharField(max_length=200, blank=True, null=True)
    staydetail = models.CharField(max_length=1000, blank=True, null=True)
    stayImg = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xxruter'


class Accoutinfo(models.Model):
    name = models.CharField(max_length=20)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'accoutinfo'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TableName(models.Model):
    username = models.CharField(max_length=20)
    bornyear = models.CharField(max_length=10, blank=True, null=True)
    bornmonth = models.CharField(max_length=6, blank=True, null=True)
    bornday = models.CharField(max_length=6, blank=True, null=True)
    hobby = models.CharField(max_length=20, blank=True, null=True)
    sex = models.IntegerField()
    image = models.CharField(max_length=30)
    place = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'table_name'
