from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, AppointmentViewSet,
    AddressViewSet, ContactViewSet, AnamnesisViewSet,
    CustomTokenObtainPairView,
)

router = DefaultRouter()
router.register(r"pacientes", PatientViewSet)
router.register(r"agendamentos", AppointmentViewSet)
router.register(r"enderecos", AddressViewSet)
router.register(r"contatos", ContactViewSet)
router.register(r"anamneses", AnamnesisViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair_custom"),
]
