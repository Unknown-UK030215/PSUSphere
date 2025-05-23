"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from studentorg.views import (HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView, OrgMemberCreateView, OrgMemberDeleteView, OrgMemberUpdateView, OrgMemberList,
                              StudentCreateView, StudentDeleteView, StudentList, StudentUpdateView, CollegeCreateView, CollegeDeleteView, CollegeList, CollegeUpdateView, ProgramCreateView, ProgramDeleteView, ProgramList, ProgramUpdateView)
from django.contrib.auth import views as auth_views
from studentorg import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home-page'),
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-edit'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-del'),
    re_path(r'^login/$', auth_views.LoginView.as_view(
        template_name = 'login.html'), name = 'login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(),{'next_page': 'login'}, name = 'logout'),


    # OrgMember URLs
    path('orgmembers/', OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmembers/add/', OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmembers/edit/<int:pk>/', OrgMemberUpdateView.as_view(), name='orgmember-edit'),
    path('orgmembers/delete/<int:pk>/', OrgMemberDeleteView.as_view(), name='orgmember-del'),

    # Student URLs
    
    path('students/', StudentList.as_view(), name='student-list'),
    path('students/add/', StudentCreateView.as_view(), name='student-add'),
    path('students/edit/<int:pk>/', StudentUpdateView.as_view(), name='student-edit'),
    path('students/delete/<int:pk>/', StudentDeleteView.as_view(), name='student-del'),

    # College URLs
    path('colleges/', CollegeList.as_view(), name='college-list'),
    path('colleges/add/', CollegeCreateView.as_view(), name='college-add'),
    path('colleges/edit/<int:pk>/', CollegeUpdateView.as_view(), name='college-edit'),
    path('colleges/delete/<int:pk>/', CollegeDeleteView.as_view(), name='college-del'),

    # Program URLs
    path('programs/', ProgramList.as_view(), name='program-list'),
    path('programs/add/', ProgramCreateView.as_view(), name='program-add'),
    path('programs/edit/<int:pk>/', ProgramUpdateView.as_view(), name='program-edit'),
    path('programs/delete/<int:pk>/', ProgramDeleteView.as_view(), name='program-del'),

]
