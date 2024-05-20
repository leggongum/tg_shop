from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    title = models.CharField(max_length=128, null=False, db_index=True)

    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'


class Subcategory(models.Model):
    title = models.CharField(max_length=128, null=False, db_index=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Subcategories'


class Product(models.Model):
    title = models.CharField(max_length=128, null=False, db_index=True)
    description = models.CharField(max_length=1024, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image = models.ImageField(upload_to='staticfiles/images/', default='staticfiles/images/no_photo.JPG')
    amount = models.IntegerField(default=0)
    subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def image_tag(self):
            return mark_safe('<img src="/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title


class Basket(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    products = models.ManyToManyField(Product, through="ProductInBasket")


class ProductInBasket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'basket'], name='unique_product_basket_combination'
            )
        ]