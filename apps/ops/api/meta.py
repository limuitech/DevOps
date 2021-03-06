# -*- coding:utf-8 -*-
from .. import models, serializers, filter
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import meta as MetaPermission
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination

__all__ = [
    'MetaPagination', 'OpsMetaListAPI', 'OpsMetaListByPageAPI',
    'OpsMetaCreateAPI', 'OpsMetaDeleteAPI',
    'OpsMetaUpdateAPI',
]


class MetaPagination(PageNumberPagination):
    page_size = 10


class OpsMetaListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaListRequiredMixin, IsAuthenticated]
    filter_class = filter.MetaFilter

    def get_queryset(self):
        user = self.request.user
        groups = models.Group.objects.filter(users=user)
        queryset = models.META.objects.filter(group_id__in=groups)
        return queryset


class OpsMetaListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaListRequiredMixin, IsAuthenticated]
    pagination_class = MetaPagination
    filter_class = filter.MetaFilter
    # 所有運維工程師有如下特點
    # 1、僅能查看自己所管理的應用組
    # 2、可以增删改自己所管理的应用组的所有Meta操作

    def get_queryset(self):
        user = self.request.user
        groups = models.Group.objects.filter(users=user)
        queryset = models.META.objects.filter(group_id__in=groups)
        return queryset


class OpsMetaCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaCreateRequiredMixin, IsAuthenticated]

    # 校验用户QR-Code
    def create(self, request, *args, **kwargs):
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            return super(OpsMetaCreateAPI, self).create(request, *args, **kwargs)
        else:
            return Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class OpsMetaUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    queryset = models.META.objects.all()
    permission_classes = [MetaPermission.MetaUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            return super(OpsMetaUpdateAPI, self).update(request, *args, **kwargs)
        else:
            return Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class OpsMetaDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    queryset = models.META.objects.all()
    permission_classes = [MetaPermission.MetaDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            return super(OpsMetaDeleteAPI, self).delete(request, *args, **kwargs)
        else:
            return Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)