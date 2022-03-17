from django.shortcuts import get_object_or_404, render

from rest_framework import generics
from vendors.models import Vendor
from vendor.permissions import IsVendor

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Category, Product, Review, Image
from .serializers import ProductSerializer, CategorySerializer, ImageSerializer

from rest_framework import status

class CategoryView(generics.ListCreateAPIView):
    permission_classes = ()
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CreateProductList(generics.ListCreateAPIView):
    permission_classes = ()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, vendor_id=None):
        if vendor_id:
            vendor = get_object_or_404(Vendor, id=vendor_id)
            products = Product.objects.filter(vendor=vendor)
        else:
            products = Product.objects.all()

        data = ProductSerializer(products, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor = get_object_or_404(Vendor, user=request.user)
        product = Product.objects.create(vendor=vendor,
        name=serializer.data['name'],
        slug=serializer.data['slug'],
        price=serializer.data['price'],
        description=serializer.data['description'])

        slugs = [dict(x)['slug'] for x in serializer.data['categories']]

        categories = Category.objects.filter(slug__in=slugs)
        product.categories.set(categories)

        return Response(
            {"detail": "Product successfully created!"}, status=status.HTTP_201_CREATED
        )

class ImageUploadView(generics.CreateAPIView):
    permission_classes = (IsVendor,)
    queryset =  Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, product_slug):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, slug=product_slug)
    
        if request.user == product.vendor.creator:
            serializer.save(product=product)
            return Response(
                {"detail": f"{product.name}'s image successfully added!"}, status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"detail": "You don't have necessary permission(s) for this action"},
            status=status.HTTP_401_UNAUTHORIZED,
        )



@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    products = Product.objects.filter(
        name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user

    product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Producted Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')
