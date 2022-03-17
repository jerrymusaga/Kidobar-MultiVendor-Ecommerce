from django.urls import path
from .views import CreateProductList, ImageUploadView, CategoryView

urlpatterns = [
    path('', CreateProductList.as_view(), name='create_list_products'),
    path('<int:id>/', CreateProductList.as_view(), name='get_vendor_products'),
    path('<slug:product_slug>/image/', ImageUploadView.as_view(), name='upload_image'),
    path('categories/', CategoryView.as_view(), name='categories')

]