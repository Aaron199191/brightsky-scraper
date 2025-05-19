import scrapy
import json
from brightsky.items import ProductItem

class BrightskySpider(scrapy.Spider):
    name = "brightsky"
    allowed_domains = ["brightsky.com.au"]
    start_urls = ["https://brightsky.com.au/shop/"]

    def parse(self, response):
        # 1) Extract each product summary from the listing
        for product in response.css("ul.products li.product"):
            detail_url = product.css(
                "a.woocommerce-LoopProduct-link::attr(href)"
            ).get()
            summary = {
                "name": product.css(
                            "h2.woocommerce-loop-product__title::text"
                        ).get(),
                "url": detail_url,
                # Grab the inner amount span for the listing price
                "price": product.css(
                             "span.woocommerce-Price-amount.amount::text"
                         ).get(),
                "image_url": product.css(
                                 "img.attachment-woocommerce_thumbnail::attr(src)"
                             ).get(),
            }
            yield response.follow(
                detail_url,
                callback=self.parse_detail,
                meta={"summary": summary}
            )

        # 2) Follow pagination
        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_detail(self, response):
        summary = response.meta["summary"]
        item = ProductItem()

        # Carry over listing-summary fields
        item["name"]      = summary.get("name")
        item["url"]       = summary.get("url")
        item["price"]     = summary.get("price")
        item["image_url"] = summary.get("image_url")

        # Detail-page fields
        item["sku"]           = response.css("span.sku::text").get()
        item["availability"]  = response.css("p.stock::text").get()
        # Regular and sale prices via the inner amount span
        item["regular_price"] = response.css(
                                     "del span.woocommerce-Price-amount.amount::text"
                                 ).get()
        item["sale_price"]    = response.css(
                                     "ins span.woocommerce-Price-amount.amount::text"
                                 ).get()
        item["categories"]    = response.css(
                                     "span.posted_in a::text"
                                 ).getall()

        # Short description
        short_desc_parts = response.css(
            ".woocommerce-product-details__short-description *::text"
        ).getall()
        item["short_description"] = " ".join(
            part.strip() for part in short_desc_parts if part.strip()
        )

        # Full description
        full_desc_parts = response.css("#tab-description *::text").getall()
        item["description"] = " ".join(
            part.strip() for part in full_desc_parts if part.strip()
        )

        # Gallery images (exclude main thumbnail)
        gallery_urls = response.css(
            "figure.woocommerce-product-gallery__wrapper img::attr(src)"
        ).getall()
        item["gallery_images"] = [
            url for url in gallery_urls if url != item["image_url"]
        ]

        # Attributes table → dict → JSON
        attrs = {}
        for row in response.css("table.woocommerce-product-attributes tr"):
            key = row.css("th::text").get(default="").strip().rstrip(":")
            values = row.css("td *::text").getall()
            clean_val = " | ".join(v.strip() for v in values if v.strip())
            attrs[key] = clean_val
        item["attributes"] = json.dumps(attrs, ensure_ascii=False)

        yield item
