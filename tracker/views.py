import boto3
from botocore.exceptions import ClientError
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from .serializers import TrackSerializer, CreateTransactionSerializer
from .models import Track


class FetchTransactionView(generics.GenericAPIView):
    '''
    FetchTransactionView handles GET requests to retrieve transaction data filtered by month and year.
    It requires authentication and uses the TrackSerializer class to serialize the data returned from the Track model.
    '''
    
    permission_classes = [IsAuthenticated]
    serializer_class = TrackSerializer

    def get_object(self):
        # get_object method retrieves the data based on the provided month and year parameters.
        query = Track.objects.filter(user=self.request.user)

        if "month" in self.request.GET:
            # If month is provided in the request parameters, validate it and filter the query accordingly.
            month = self.request.GET["month"]
            if not month.isdigit():
                raise Http404("Invalid Month")

            month = int(month)
            if month < 1 or month > 12:
                raise Http404("Invalid Month")

            query = query.filter(date__month=month)

        if "year" in self.request.GET:
            # If year is provided in the request parameters, validate it and filter the query accordingly.
            year = self.request.GET["year"]
            if not year.isdigit():
                raise Http404("Invalid Year")

            year = int(year)
            curr_year = datetime.now().year
            if year < curr_year - 20 or year > curr_year:
                raise Http404("Invalid Year")

            query = query.filter(date__year=year)

        return query

    def get(self, request):
        # get method retrieves the filtered data using get_object and returns it as a Response object.
        query = self.get_object()

        serializer = self.get_serializer(many=True, instance=query)

        data = dict()

        for filter, category in Track.categories:
            # Group the data by category and return the total amount spent for each category.
            data[category] = 0
            for amount in query.filter(category=filter).values_list("amount"):
                data[category] += amount[0]

        data["detail"] = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class AddTransactionView(generics.CreateAPIView):
    '''
    AddTransactionView handles POST requests to add new transaction data.
    It requires authentication and uses the CreateTransactionSerializer class to serialize the data sent in the request body.
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = CreateTransactionSerializer


class ListCategoriesView(generics.ListAPIView):
    '''
    ListCategoriesView handles GET requests to retrieve a list of transaction categories.
    It requires authentication and returns a list of categories defined in the Track model.
    '''

    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = []
        for category, _ in Track.categories:
            categories += (category,)

        return Response(categories)

