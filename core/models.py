from django.db import models
# from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
# from accounts.models import Profile


# def upload_location(self, filename, **kwargs):
#     file_path = 'app/assets/img/{title}-{filename}'.format(
#         title=str(self.title), filename=filename)
#     return file_path


CATEGORY_CHOICES = (
    ('shirts', 'Shirts'),
    ('sports_wears', 'Sports Wears'),
    ('out_wears', 'Out Wears')
)

LABEL_CHOICES = (
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger')
)

CART_STATUS = (
    ('closed', 'Closed'),
    ('opened', 'Opened')
)

class Item(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    price = models.FloatField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200, null=True, blank=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=200, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    discount = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    # date_ordered = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(choices=CART_STATUS, default='opened', max_length=25)

    def __str__(self):
        return self.item.title


class Order(models.Model):
    ref_number = models.CharField(null=True, blank=True, max_length=250)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    item = models.ManyToManyField(CartItem)
    # date_added = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.item.price for item in self.items.all()])