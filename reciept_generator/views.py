from rest_framework.response import Response
from rest_framework import generics, status


class HealthCheckView(generics.GenericAPIView):

    '''
    HealthCheckView handles GET requests returns 200 on every response to test server health
    Does not require authentication
    '''

    def get(self, request):
        # returns json of status:ok on every request
        return Response({"Status": "Ok"}, status=status.HTTP_200_OK)
