import requests
from urllib.parse import urljoin

from db import DatabaseManager
from .ParserBase import ParserBase

class GoodWineParser(ParserBase):
    name = "GoodWine"
    url = "https://goodwine.com.ua/ua"
    api_url = "https://goodwine.com.ua/graphql"


    def __init__(self, db: DatabaseManager):
        super().__init__(db)


    def parse_page(self, page: int):
        query = """
            query category(
                $id: Int!
                $pageSize: Int!
                $currentPage: Int!
                $onServer: Boolean!
                $filters: ProductAttributeFilterInput!
                $sort: ProductAttributeSortInput
            ) {
                category(id: $id) {
                    id
                    uid
                    description
                    name
                    product_count
                    title_h1
                    meta_title
                    meta_keywords
                    meta_description
                    cms_block {
                        identifier
                        __typename
                    }
                    url_path
                    banner_url
                    url_key
                    breadcrumbs {
                        category_id
                        category_name
                        __typename
                    }
                    __typename
                }
                products(
                    pageSize: $pageSize
                    currentPage: $currentPage
                    filter: $filters
                    sort: $sort
                ) {
                    items {
                        __typename
                        description {
                            html
                            __typename
                        }
                        categories {
                            id
                            name
                            url_path
                            __typename
                        }
                        id
                        special_price
                        swatch_image
                        custom_attributes {
                            author_info
                            producer
                            color
                            sweet
                            country
                            country_flag
                            region
                            producer_filter_url
                            country_filter_url
                            region_filter_url
                            stock_sales_qty
                            max_sale_qty
                            multi_country
                            qty
                            vintage
                            filter_data {
                                kLabel
                                kValue
                                label
                                value
                                attr
                                label_length
                                attr_value
                                index
                                __typename
                            }
                            __typename
                        }
                        capacity
                        image_big
                        media_gallery {
                            disabled
                            label
                            position
                            url
                            __typename
                        }
                        meta_title @include(if: $onServer)
                        meta_keyword @include(if: $onServer)
                        meta_description
                        name
                        price {
                            regularPrice {
                                amount {
                                    currency
                                    value
                                    __typename
                                }
                                __typename
                            }
                            __typename
                        }
                        stock_status
                        sku
                        special_price
                        special_from_date
                        special_to_date
                        small_image {
                            url
                            __typename
                        }
                        rating_summary
                        review_count
                        alt_ratings_count
                        alt_ratings_value
                        reviews {
                            items {
                                nickname
                                average_rating
                                summary
                                created_at
                                ratings_breakdown {
                                    name
                                    value
                                    __typename
                                }
                                __typename
                            }
                            __typename
                        }
                        url_key
                        ... on ConfigurableProduct {
                            configurable_options {
                                attribute_code
                                attribute_id
                                id
                                label
                                values {
                                    default_label
                                    label
                                    store_label
                                    use_default_value
                                    value_index
                                    __typename
                                }
                                __typename
                            }
                            variants {
                                attributes {
                                    code
                                    value_index
                                    __typename
                                }
                                product {
                                    id
                                    media_gallery_entries {
                                        id
                                        disabled
                                        file
                                        label
                                        position
                                        __typename
                                    }
                                    sku
                                    stock_status
                                    __typename
                                }
                                __typename
                            }
                            __typename
                        }
                        price_tiers {
                            final_price {
                                value
                                __typename
                            }
                            discount {
                                amount_off
                                percent_off
                                __typename
                            }
                            quantity
                            __typename
                        }
                        special_price
                    }
                    aggregations {
                        label
                        count
                        attribute_code
                        options {
                            label
                            value
                            count
                            __typename
                        }
                        __typename
                    }
                    page_info {
                        total_pages
                        __typename
                    }
                    total_count
                    __typename
                }
            }
        """
        
        response = requests.post(
            self.api_url,
            json={
                "query": query,
                "operationName": "category",
                "variables": {
                    "currentPage": page,
                    "id": 6,
                    "filters": {"category_id": {"eq": "6"}},
                    "onServer": False,
                    "pageSize": 30,
                    "sort": {"quantity_and_stock_status": "DESC"}
                }
            }, 
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            }
        )
        if not response.ok:
            raise Exception(f"Failed to fetch whisky list: {response.status_code} {response.text}")
        else:
            json = response.json()
            product_list = json.get("data", {}).get("products", {}).get("items", [])
            return [{
                "source": self.name,
                "external_id": item.get("id", ""),
                "title": item.get("name", ''),
                "url": urljoin(self.url, item.get("url_key", '')),
                "price": item.get("price_tiers", [])[0].get("final_price", 0).get("value", 0) 
                    if item.get("price_tiers") and len(item.get("price_tiers", [])) > 0 
                    else 0,
                "old_price": item.get("price", {}).get("regularPrice", {}).get("amount", {}).get("value", 0)
                    if len(item.get("price_tiers", [])) > 0 and item.get("price_tiers", [])[0].get("discount", {}).get("amount_off", 0) > 0 
                    else 0
            } for item in product_list]