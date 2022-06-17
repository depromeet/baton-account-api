# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
# from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

TEST = False


class User(models.Model):
    # id = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
    #                           db_column='id', related_name='app_user', help_text='User ID(integer)')
    id = models.IntegerField(primary_key=True, )
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)
    account = models.OneToOneField('Account', blank=True, null=True, on_delete=models.CASCADE)  # TODO has_account 추가?
    point = models.PointField(srid=4326)
    address = models.CharField(max_length=255)
    detailed_address = models.CharField(max_length=255, blank=True)
    check_terms_of_service = models.BooleanField()
    check_privacy_policy = models.BooleanField()  # TODO model_schema.sql

    class Meta:
        managed = TEST
        db_table = 'User'


class Account(models.Model):
    holder = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

    class Meta:
        managed = TEST
        db_table = 'Account'


class Bookmark(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='bookmarks')
    ticket = models.ForeignKey('Ticket', models.DO_NOTHING, related_name='bookmarks')

    class Meta:
        managed = TEST
        db_table = 'Bookmark'
        unique_together = (('user', 'ticket'),)


class Buy(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='buys')
    ticket = models.OneToOneField('Ticket', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(blank=True, null=True, help_text='구매일시')

    class Meta:
        managed = TEST
        db_table = 'Buy'
        ordering = ['-date']


class Ticket(models.Model):
    seller = models.ForeignKey('User', models.DO_NOTHING, related_name='sell_tickets')
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField()
    state = models.IntegerField(help_text='양도권 상태 (0: 판매중, 1: 예약중, 2: 판매완료)')
    tag_hash = models.BigIntegerField()
    is_membership = models.BooleanField()
    is_holding = models.BooleanField()
    remaining_number = models.IntegerField(blank=True, null=True)
    type = models.IntegerField()
    can_nego = models.BooleanField()
    trade_type = models.IntegerField()
    has_shower = models.BooleanField()
    has_locker = models.BooleanField()
    has_clothes = models.BooleanField()
    has_gx = models.BooleanField()
    can_resell = models.BooleanField()
    can_refund = models.BooleanField()
    description = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    transfer_fee = models.IntegerField()
    point = models.PointField(srid=4326)
    address = models.CharField(max_length=255)
    main_image = models.CharField(max_length=255, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    bookmark_count = models.IntegerField()
    view_count = models.IntegerField()

    # buyer = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='buy_tickets')
    bookmark_users = models.ManyToManyField('User', through='Bookmark', related_name='bookmark_tickets')
    tags = models.ManyToManyField('Tag', through='TicketTag', related_name='tickets')

    class Meta:
        managed = TEST
        db_table = 'Ticket'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.location = Point(self.point.x, self.point.y, srid=4326)
        super().save()


class TicketImage(models.Model):
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING, related_name='images')
    url = models.CharField(max_length=255)
    is_main = models.BooleanField()
    thumbnail_url = models.CharField(max_length=255)

    class Meta:
        managed = TEST
        db_table = 'TicketImage'


class Tag(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        managed = TEST
        db_table = 'Tag'


class TicketTag(models.Model):
    ticket = models.ForeignKey('Ticket', models.DO_NOTHING)
    tag = models.ForeignKey('Tag', models.DO_NOTHING)

    class Meta:
        managed = TEST
        db_table = 'TicketTag'
