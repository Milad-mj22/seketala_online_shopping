from django.db import models



class Complaint(models.Model):
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('in_progress', 'در حال بررسی'),
        ('resolved', 'حل شده'),
        ('rejected', 'رد شده'),
    ]

    SUBJECT_CHOICES = [
        ('payment', 'مشکل در پرداخت'),
        ('delivery', 'مشکل در ارسال'),
        ('product', 'مشکل در کیفیت غذا'),
        ('support', 'مشکل با پشتیبانی'),
        ('other', 'سایر'),
    ]

    name        = models.CharField(max_length=100, verbose_name='نام')
    phone       = models.CharField(max_length=20, verbose_name='شماره تماس')
    email       = models.EmailField(blank=True, verbose_name='ایمیل')
    order_id    = models.CharField(max_length=100, blank=True, verbose_name='شماره سفارش')
    subject     = models.CharField(max_length=30, choices=SUBJECT_CHOICES, verbose_name='موضوع')
    message     = models.TextField(verbose_name='متن شکایت')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='وضعیت')
    ip_address  = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')
    user_agent  = models.TextField(blank=True, verbose_name='User Agent')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'شکایت'
        verbose_name_plural = 'شکایات'
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.id} — {self.name} ({self.phone})'