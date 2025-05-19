# -*- coding: utf-8 -*-

BOT_NAME = "brightsky"
SPIDER_MODULES = ["brightsky.spiders"]
NEWSPIDER_MODULE = "brightsky.spiders"

# —— Performance tuning ——  
CONCURRENT_REQUESTS            = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 16
DOWNLOAD_DELAY                 = 0.2
COOKIES_ENABLED                = False
RETRY_ENABLED                  = False
LOG_LEVEL                      = "INFO"

# —— Feed export defaults ——  
FEED_FORMAT        = "csv"
FEED_URI           = "products.csv"
FEED_EXPORT_FIELDS = [
    "sku",
    "name",
    "url",
    "price",
    "regular_price",
    "sale_price",
    "availability",
    "categories",
    "short_description",
    "description",
    "image_url",
    "gallery_images",
    "attributes",
]
