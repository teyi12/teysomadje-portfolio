from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from portfolio.sitemaps import PortfolioSitemap
from portfolio.views import robots_txt


sitemaps = {
    "portfolio": PortfolioSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", robots_txt, name="robots_txt"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
]

urlpatterns += i18n_patterns(
    path("", include("portfolio.urls")),
    prefix_default_language=True,
)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
