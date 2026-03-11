import math

from controllers.rest import ControllerRest, PaginationLinks, PaginationMeta, RestError, RestMeta, RestStatus


products = [
    {"id": 1 , "name": "Product 1 ", "price": 101.49 },
    {"id": 2 , "name": "Product 2 ", "price": 102.49 },
    {"id": 3 , "name": "Product 3 ", "price": 103.49 },
    {"id": 4 , "name": "Product 4 ", "price": 104.49 },
    {"id": 5 , "name": "Product 5 ", "price": 105.49 },
    {"id": 6 , "name": "Product 6 ", "price": 106.49 },
    {"id": 7 , "name": "Product 7 ", "price": 107.49 },
    {"id": 8 , "name": "Product 8 ", "price": 108.49 },
    {"id": 9 , "name": "Product 9 ", "price": 109.49 },
    {"id": 10, "name": "Product 10", "price": 110.49 },
    {"id": 11, "name": "Product 11", "price": 111.49 },
    {"id": 12, "name": "Product 12", "price": 112.49 },
]

class ProductController(ControllerRest) :
    def do_GET(self) :
        # Пагінація - розбиття на сторінки
        # Параметри (обов'язкові):
        # загальна кількість елементів  totalItems
        # загальна кількість сторінок   totalPages
        # поточна сторінка              page
        # місткість сторінки            perPage
        # Параметри (опціональні):
        # наявність попередньої сторінки
        # наявність наступної сторінки
        # url-посилання на різні сторінки (від сусідніх до повного пагінатора) або шаблон url
        #   
        self.rest_response.meta = RestMeta(
            service= "Back API service 'My shop': products",
            service_url= "http://localhost:88/product",
        )
        total_items = len(products)  # SELECT COUNT(*) FROM Products WHERE search...
        per_page_default = 5
        per_page_param = self.query_params.get('perpage', per_page_default)
        # всі прийняті дані слід валідувати
        if not isinstance(per_page_param, int) :
            try : per_page = int(per_page_param)
            except : per_page = 0
        else:
            per_page = per_page_param    
        if per_page <= 0 :
            raise RestError(status=RestStatus.bad_request_400,
                data=f"Invalid value for 'perpage'({per_page_param}): only positive integers accepted"
            ) 
        
        total_pages = math.ceil(total_items / per_page)

        page_param = self.query_params.get('page', 1)
        if not isinstance(page_param, int) :
            try : page = int(page_param)
            except : page = 0
        else:
            page = page_param    
        if page <= 0 or page > total_pages :
            raise RestError(status=RestStatus.bad_request_400,
                data=f"Invalid value for 'page'({page_param}): integers in range 1..{total_pages} accepted"
            )
        
        url_prefix = "/product?page=" if per_page == per_page_default else f"/product?perpage={per_page}&page="
        self.rest_response.meta.pagination = PaginationMeta(
            total_items=total_items,
            per_page=per_page,
            total_pages=total_pages,
            page=page,
            links=PaginationLinks(
                first_url = url_prefix[:-6],
                prev_url  = url_prefix + str(page - 1)    if page > 1 else None,
                next_url  = url_prefix + str(page + 1)    if page < total_pages else None,
                last_url  = url_prefix + str(total_pages) if total_pages > 1 else url_prefix[:-6],
            )
        )
