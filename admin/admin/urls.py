from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from administrer import views
import authentication.views





urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include(('administrer.urls', 'adminstrer'), namespace='administrer')),
    path('index/', views.index, name='index'),
    path('inbox/notifications/',include(('notifications.urls', 'notifications'), namespace='notifications')),

    
    
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),


    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
