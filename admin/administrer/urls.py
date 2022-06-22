
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns =[

    path('index/', views.index, name='index'),
    path('statistique/', views.dashboard, name='dashboard'),

    path('add/personne', views.personne, name='person_add'),
    path('ajax/load-cities/', views.load_cities,name='ajax_load_cities'),  
    path('liste/personne', views.listePerson, name='person_changelist'),
    path('search/', views.search,name='search'),
    path('<int:id>/', views.ModiPers, name='person_change'),
    path('Supprimer/<int:id>', views.supPerson, name='supPerson'),
    path('details/<pk>', views.detail, name='details'),
    path('add/courrier', views.AddCour, name='AddCour'),
    path('liste/courrier', views.liste, name='liste'),
    path('modifier/courrier/<int:id>', views.Modif, name='Modif'),
    path('supprimer/courrier/<int:id>', views.suppression, name='suppression'),
    path('pdf/courrier/<pk>', views.pdf, name='pdf'),
    # path('statistique/courrier', views.listeDirec, name='listeDirec'),
    path('statistique/personnel', views.dash, name='dash'),














]
if settings.DEBUG:  # add this
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
