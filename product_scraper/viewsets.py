from rest_framework import viewsets, serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import Scraper,ProductService
from .serializers import inline_serializer
from .utils.mixins import CustomResponseMixin
import asyncio


class ScraperViewSet(CustomResponseMixin, viewsets.ViewSet):

    @action(detail=False, methods=["post","get"], url_path="scrape_website")
    def scrape_website(self, request):
        serialized_data = inline_serializer(
            fields={
                "product_data": serializers.CharField(max_length=512, required=False),
            },
            data=request.data,
        )
        errors = self.validate_serializer(serialized_data)
        if errors:
            return errors

        #response = Scraper.scrape_product()
        scraper_instance = Scraper()

        # Call the scrape_product function
        result = asyncio.run(scraper_instance.scrape_product())
        return self.response(result)
    
    
    @action(detail=False, methods=["get"], url_path="fetch_products")
    def fetch_products(self, request):

        response = ProductService.fetch_products()
        return self.response(response)
    

