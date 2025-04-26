from django.urls import include, path
from rest_framework_nested.routers import NestedDefaultRouter

from huscy.project_consents.urls import project_router
from mpi_cbs.huscy.mpicbs_project_consents.views import (
    ListSubjectsWithSignedConsentView,
    MPICBSProjectConsentTokenViewSet,
)


consent_router = NestedDefaultRouter(project_router, 'consents', lookup='consent')
consent_router.register('wrapped_token', MPICBSProjectConsentTokenViewSet)


urlpatterns = [
    path('api/', include(consent_router.urls)),
    path(
        'projects/<project_pk>/signedconsents/',
        ListSubjectsWithSignedConsentView.as_view(),
        name='signed-project-consents',
    ),
]
