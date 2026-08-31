from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .sitemaps import PortfolioSitemap
from .views import home, robots_txt


sitemaps = {
    "portfolio": PortfolioSitemap,
}

urlpatterns = [
    path("", home, name="home"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
]
