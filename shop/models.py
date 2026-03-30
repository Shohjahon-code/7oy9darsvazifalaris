from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import CustomUser



class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.TextField(verbose_name="Ikona (SVG yoki emoji)")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Tavsifi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so'm)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Eski narxi")
    stock = models.PositiveIntegerField(default=0, verbose_name="Omborda soni")
    is_available = models.BooleanField(default=True, verbose_name="Mavjudmi")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Kategoriyasi"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_main_image(self):
        img = self.images.first()
        if img:
            return img.image.url
        return "https://placehold.co/600x600/1a1a2e/ffffff?text=Rasm+yo%27q"

    def get_discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('processing', 'Jarayonda'),
        ('shipped', 'Yetkazilmoqda'),
        ('delivered', "Yetkazib berildi"),
        ('cancelled', 'Bekor qilindi'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Naqd pul'),
        ('card', 'Plastik karta'),
        ('online', 'Online to\'lov'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='orders', verbose_name="Mijoz")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holati")
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash', verbose_name="To'lov turi")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Jami narx")
    note = models.TextField(blank=True, verbose_name="Izoh")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created']

    def __str__(self):
        return f"Buyurtma #{self.pk} — {self.user.username}"

    def calculate_total(self):
        total = sum(item.get_subtotal() for item in self.items.all())
        self.total_price = total
        self.save()


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Buyurtma")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdori")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_subtotal(self):
        return self.price * self.quantity


class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses', verbose_name="Mijoz")
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    city = models.CharField(max_length=100, default="Toshkent", verbose_name="Shahar")
    address = models.CharField(max_length=300, verbose_name="Manzil")
    zip_code = models.CharField(max_length=20, blank=True, verbose_name="Pochta indeksi")
    is_default = models.BooleanField(default=False, verbose_name="Asosiy manzil")

    class Meta:
        verbose_name = "Yetkazish manzili"
        verbose_name_plural = "Yetkazish manzillari"

    def __str__(self):
        return f"{self.full_name} — {self.city}, {self.address}"
