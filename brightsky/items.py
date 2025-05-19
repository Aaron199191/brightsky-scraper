import scrapy

class ProductItem(scrapy.Item):
    sku               = scrapy.Field()
    name              = scrapy.Field()
    url               = scrapy.Field()
    price             = scrapy.Field()        # displayed price (could be sale or regular)
    regular_price     = scrapy.Field()
    sale_price        = scrapy.Field()
    availability      = scrapy.Field()        # e.g. “In stock” / “Out of stock”
    categories        = scrapy.Field()        # list of category names
    short_description = scrapy.Field()
    description       = scrapy.Field()
    image_url         = scrapy.Field()        # main thumbnail
    gallery_images    = scrapy.Field()        # list of additional image URLs
    attributes        = scrapy.Field()        # JSON-dumped dict of all attribute rows
