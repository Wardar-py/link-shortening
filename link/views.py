import re
from uuid import uuid1
from django.shortcuts import render, get_object_or_404, redirect
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from link.models import Link
from link.serializers import LinkSerializer, LinkResponseSerializer
import pyshorteners
from rest_framework.response import Response
from link.utils import BadURLException


class LinkView(viewsets.ViewSet):

    serializer_class = LinkSerializer
    permission_classes = (#IsAuthenticated,
                          AllowAny,)
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_object(self, **kwargs):
        return get_object_or_404(
            Link, id=self.kwargs["pk"]
        )

    @swagger_auto_schema(
        operation_description='post link',
        request_body=LinkSerializer,
        responses={200: LinkResponseSerializer()},
        security=[],
    )
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            link = serializer.validated_data['link']
            URL_RE = re.compile(
                r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.]"
                r"[a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)"
                r"))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()"
                r'\[\]{};:\'".,<>?«»“”‘’]))'
            )
            check = URL_RE.match(link)
            if not check:
                raise BadURLException(f"{link} is not valid")

            short_link = f"https://short_link/{uuid1()}"
            link_orm = Link.objects.create(full_link=link, short_link=short_link, user_id=1)
            link_orm.save()
            return Response(LinkResponseSerializer(link_orm).data, status=201)

        status_error = {
            "detail": "Файл не должен быть весить больше 5мб",
        }
        status_error.update(serializer.errors)

        return Response(status_error, status=422)


    @swagger_auto_schema(
        operation_description='get link by id',
        responses={200: LinkResponseSerializer()},
        security=[],
    )
    def retrieve(self, request, *args, **kwargs):

            pk = kwargs['pk']
            link_orm = self.get_object(pk=pk)

            return redirect(link_orm.full_link)


class AllUserLinks(generics.ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkResponseSerializer
    permission_classes = (#IsAuthenticated,
                          AllowAny,)

    @swagger_auto_schema(
        operation_description='get all user links',
        responses={200: LinkResponseSerializer(many=True)},
        security=[],
    )
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = LinkResponseSerializer(qs, many=True)
        return Response(serializer.data, status=201)




#{"link": "https://www.google.com/search?q=url+shortener+python&client=ubuntu&hs=Xzh&sxsrf=ALiCzsasdO-kjcW4-EXaOIHAWlzjLMs7cQ%3A1657645635123&ei=Q6rNYqWDB-i49u8PgpCdmAk&oq=pip+install+pyshorteners&gs_lcp=Cgdnd3Mtd2l6EAEYADIHCAAQRxCwAzIHCAAQRxCwAzIHCAAQRxCwAzIHCAAQRxCwA0oECEEYAEoECEYYAFAAWABgz98SaANwAXgAgAEAiAEAkgEAmAEAyAEEwAEB&sclient=gws-wiz"}