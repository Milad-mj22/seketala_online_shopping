from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        # لیست نام URLهایی که می‌خواهید در نقشه سایت باشند
        return ['landing:home', 'landing:menu'] 

    def location(self, item):
        return reverse(item)