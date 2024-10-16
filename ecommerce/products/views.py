from django.core.cache import cache
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .models import Product, Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .serializer import ProductSerializer, CategorySerializer

import logging

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        page_number = request.query_params.get('page', 1)

        # Create a unique cache key per page
        cache_key = f'product_list_page_{page_number}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # If not cached, fetch and paginate the queryset
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            cache.set(cache_key, paginated_response.data, timeout=60 * 15)  # Cache for 15 minutes

            return paginated_response

        # If pagination is not needed, return the full list (fallback)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
