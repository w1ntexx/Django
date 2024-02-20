from django.contrib.sitemaps import Sitemap

from cats.models import Cat, Species


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    
    def items(self):
        return Cat.published.all()
    
    def lastmod(self, obj):
        return obj.time_update
    
    
class SpecSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    
    def items(self):
        return Species.objects.all()
    