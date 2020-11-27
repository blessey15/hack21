"""hack21 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

# from user import views 
from accounts import views
from profiles import views as profileviews
from application import views as application_views
urlpatterns = [
    # path('', TemplateView.as_view(template_name="login.html")),
    path('admin/', admin.site.urls),
    path('', views.landing_page_view,  name='landing_page'),
    path('sponsor', views.sponsor_view,  name='sponsors'),
    path('dashboard', views.home, name='home'),
    path('register/', views.registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('account/', views.account_view, name='account'),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),

# Password Reset Password Forgot ...
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

# PROFILE
    path('profile/<int:id>', profileviews.participant_profile_view, name='profile'),

    path('profile/', profileviews.own_profile_view, name='own_profile'),

    path('profile-update/', profileviews.participant_profile_creation_view, name='profile-update'),
    
    path('profile_done/', profileviews.participant_profile_updated_view, name='profile_created'),

# TEAM DEATAILS
    path('teams/<uuid:team_id>', application_views.team_detail_view, name='team_detail'),

    path('teams/<uuid:team_id>/join', application_views.join_team_view, name='join_team'),

    path('teams/<uuid:team_id>/leave', application_views.leave_team_view, name='leave_team'),

# ACCEPT| DECLINE | WAITINGLIST
    path('teams/<uuid:team_id>/accept', application_views.accept_team_view, name='accept_team'),

    path('teams/<uuid:team_id>/decline', application_views.decline_team_view, name='decline_team'),

    path('teams/<uuid:team_id>/waitinglist', application_views.waitinglist_team_view, name='waitinglist_team'),

# MASS MAILING ROUTES
    path('mail/accepted', application_views.send_accepted_email, name='mail_accepted'),

    path('mail/declined', application_views.send_declined_email, name='mail_declined'),

    path('mail/waitinglist', application_views.send_wtlst_email, name='mail_wtlst'),

    path('mail/nosub', application_views.send_not_submitted_email, name='mail_not_submitted'),

    path('submit', application_views.submit_aplication_view, name='submit_application'),

    path('orgdb', application_views.organizer_dashboard, name='organizer_dashboard'),

# TEMPORARY VIEWS
    path('base', views.base_view, name='base'),

    path('temp2', views.temp_view, name='home2'),

    path('mail', views.email_view, name='mail'),

# FILE EXPORT VIEWS
    # path('export/users/csv', views.export_csv, name='export_user_csv'),

    # path('export/users/xls', views.export_xls, name='export_user_xls'),

    path('export/profile/csv', profileviews.export_csv, name='export_profile_csv'),

    path('export/profile/xls', profileviews.export_xls, name='export_profile_xls'),

    # path('test', views.test_view,  name='test_home'),
]
