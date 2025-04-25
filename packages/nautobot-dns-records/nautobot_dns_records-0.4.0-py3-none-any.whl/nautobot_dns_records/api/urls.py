"""API urls for nautobot_dns_records."""

from rest_framework import routers
from nautobot_dns_records.api.views import (
    AddressRecordViewSet,
    CNameRecordViewSet,
    TxtRecordViewSet,
    LocRecordViewSet,
    PtrRecordViewSet,
    SshfpRecordViewSet,
    SrvRecordViewSet,
)

router = routers.DefaultRouter()
router.register("address-records", AddressRecordViewSet, basename="addressrecord")
router.register("cname-records", CNameRecordViewSet, basename="cnamerecord")
router.register("txt-records", TxtRecordViewSet, basename="txtrecord")
router.register("loc-records", LocRecordViewSet, basename="locrecord")
router.register("ptr-records", PtrRecordViewSet, basename="ptrrecord")
router.register("sshfp-records", SshfpRecordViewSet, basename="sshfprecord")
router.register("srv-records", SrvRecordViewSet, basename="srvrecord")
urlpatterns = router.urls
