from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from db.models import engine, Category, SubCategory, Product, Available, Order, OrderItem

app = Starlette()

admin = Admin(engine, title="Example: SQLAlchemy")


class CustomCategoryModelView(ModelView):
    exclude_fields_from_create = ('subcategories',)

class CustomSubCategoryModelView(ModelView):
    exclude_fields_from_create = ("products",)

class CustomProductModelView(ModelView):
    exclude_fields_from_create = ("availables",)






admin.add_view(CustomCategoryModelView(Category))
admin.add_view(CustomSubCategoryModelView(SubCategory))
admin.add_view(CustomProductModelView(Product))
admin.add_view(ModelView(Available))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(OrderItem))

admin.mount_to(app)