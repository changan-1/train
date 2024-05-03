"""pythondjago URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import path
from selectlocal.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('gettraveinfo/',gettraveinfo),
    path('getonetrave/',getonetrave),
    path('saveTable_name/',saveTable_name),
    path('searchTable_name/', searchTable_name),
    path('upDateTable_name/', upDateTable_name),
    path('saveAccoutinfo/', saveAccoutinfo),
    path('searchAccoutinfo/', searchAccoutinfo),
    path('upDateAccoutinfo/', upDateAccoutinfo),
    path('searchall/', searchall),
    path('saveCity/', saveCity),
    path('searchCityall/',searchCityall),
    path('saveHotel/',saveHotel),
    path('searchCityPonit/', searchCityPonit),
    path('savePointss/', savePointss),
    path('saveCityPonit/', saveCityPonit),
    path('savecityserc/', savecityserc),
    path('searchCityserc/', searchCityserc),
    path('saveuserhh/', saveuserhh),
    path('searchuserhh/', searchuserhh),
    path('docs/', include_docs_urls(title='旅游网站的api文档')),

]
