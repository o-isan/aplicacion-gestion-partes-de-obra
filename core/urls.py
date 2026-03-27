from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'parts', views.PartViewSet, basename='part')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # Template-based views
    path('parts/', views.PartListView.as_view(), name='part_list'),
    path('parts/add/', views.PartCreateView.as_view(), name='part_add'),
    path('parts/<int:pk>/edit/', views.PartUpdateView.as_view(), name='part_edit'),
    path('parts/<int:pk>/delete/', views.PartDeleteView.as_view(), name='part_delete'),
]
