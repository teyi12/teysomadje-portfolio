from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import translation


class PortfolioSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0
    protocol = "https"

    def items(self):
        return ["en", "de", "fr"]

    def location(self, language):
        with translation.override(language):
            return reverse("home")
