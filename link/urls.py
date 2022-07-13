from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from link.views import CreateLinkView, AllUserLinks, GetLinkView

urlpatterns = [


    path('create_link/', CreateLinkView.as_view()),
    path('get_link/<int:pk>', GetLinkView.as_view()),
    path('get_all_links', AllUserLinks.as_view()),
]