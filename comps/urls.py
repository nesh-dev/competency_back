from django.urls import path, include
urlpatterns = [

    path('users/', include(('comps.authentication.urls',
                                    'authentication'), namespace='authentication')),

]