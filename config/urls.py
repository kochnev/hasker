"""hasker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from hasker.qa import views as qa_views
from hasker.account import views as acc_views

urlpatterns = [
    url(r'^$', qa_views.index, name='index'),
    url(r'^signup/', acc_views.signup, name='signup'),
    url(r'^login/', acc_views.user_login, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^settings/$', acc_views.settings, name='settings'),
    url(r'^ask/$', qa_views.add_question, name='add_question'),
    url(r'^question/(?P<slug>[\w\-]+)/$', qa_views.question_detail, name='question_detail'),
    url(r'^mark-answer/(?P<slug>[\w\-]+)/(?P<pk>\d+)/$', qa_views.mark_answer, name='mark_answer'),
    url(r'^vote-question/(?P<slug>[\w\-]+)/(?P<type_vote>[\w\-]+)/$', qa_views.vote_question, name='vote_question'),
    url(r'^vote-answer/(?P<slug>[\w\-]+)/(?P<pk>\d+)/(?P<type_vote>[\w\-]+)/$', qa_views.vote_answer, name='vote_answer'),
    url(r'^admin/', admin.site.urls),
]
