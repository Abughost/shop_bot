from datetime import datetime
from email.policy import default
from enum import Enum as Pyenum

from sqlalchemy import create_engine, ForeignKey, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/shop_db")

class Base(DeclarativeBase):
    pass

class OrderStatus(Pyenum):
    pending = "pending"
    completed = "finished"
    rejected = "rejected"

class Category(Base):
    __tablename__ = "categories"
    category_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_en:Mapped[str]
    name_ru:Mapped[str]
    name_uz:Mapped[str]
    icon:Mapped[str] = mapped_column(nullable=True)

    subcategories: Mapped[list["SubCategory"]] = relationship("SubCategory", back_populates="category", cascade="all, delete")

class SubCategory(Base):
    __tablename__ = "subcategories"
    subcategory_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_en:Mapped[str]
    name_ru:Mapped[str]
    name_uz:Mapped[str]
    icon:Mapped[str] = mapped_column(nullable=True)
    category_id:Mapped[int] = mapped_column(ForeignKey("categories.category_id",ondelete='cascade'))
    category: Mapped["Category"] = relationship("Category", back_populates="subcategories")

    products: Mapped[list["Product"]] = relationship("Product", back_populates="subcategory", cascade="all, delete")

class Product(Base):
    __tablename__ = "products"
    product_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_en:Mapped[str]
    name_ru:Mapped[str]
    name_uz:Mapped[str]
    brand_name:Mapped[str]
    model:Mapped[str]
    price:Mapped[float] = mapped_column(DECIMAL(12,2))
    currency:Mapped[str]
    subcategory_id:Mapped[int] = mapped_column(ForeignKey("subcategories.subcategory_id",ondelete='cascade'))
    subcategory: Mapped["SubCategory"] = relationship("SubCategory", back_populates="products")
    photo:Mapped[str] = mapped_column(nullable=True)

    available_items: Mapped[list["Available"]] = relationship("Available", back_populates="product", cascade="all, delete")
    order_items:Mapped[list['OrderItem']] = relationship('OrderItem',back_populates='products',cascade='all,delete')

class Available(Base):
    __tablename__ = "availables"
    available_product_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.product_id",ondelete='cascade'))
    size:Mapped[str] = mapped_column(nullable=True)
    configuration:Mapped[str] = mapped_column(nullable=True)
    color:Mapped[str]
    extra_price:Mapped[int] = mapped_column(DECIMAL(12,2),default=0.00)
    quantity:Mapped[int]

    product: Mapped["Product"] = relationship("Product", back_populates="available_items")

class Order(Base):
    __tablename__ = 'orders'
    order_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[str]
    amount:Mapped[float] = mapped_column(DECIMAL(12,2),nullable=True)
    status:Mapped[str] = mapped_column(Enum(OrderStatus, values_colable = lambda x: [x.value for i in x],default=OrderStatus.pending))
    created_at:Mapped[int] = mapped_column(TIMESTAMP,default = datetime.now())
    order_items:Mapped[list["OrderItem"]] = relationship('OrderItem',cascade='all, delete')

class OrderItem(Base):
    __tablename__ = "orderitems"
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id:Mapped[int] =  mapped_column(ForeignKey("products.product_id",ondelete='cascade'))
    order_id:Mapped[int] =  mapped_column(ForeignKey("orders.order_id",ondelete='cascade'))
    quantity:Mapped[int]

    orders:Mapped['Order'] = relationship('Order',back_populates='order_items')
    products:Mapped['Product'] = relationship('Product' , back_populates='order_items')




metadata = Base.metadata









