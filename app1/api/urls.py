
from django.contrib import admin
from django.urls import path, include
from app1.views import *
urlpatterns = [
    path('auth/login/', loginAPI),
    path('auth/signup/', signupAPI),
    # JOIN requests
    path('join_requests/', getJoinRequestsAPI),
    path('join_requests/', createJoinRequestAPI),
    path('join_requests/group', joinRequestsGroupAPI),
    path('join_requests/accept/', joinRequestsAcceptAPI),
    # CONNECTION requests
    path('connection_requests/', connectionRequestGetAPI),
    path('connection_requests/', connectionRequestPostAPI),
    path('connection_requests/accept', connectionRequestAcceptAPI),
    
    # GROUP requests
    path('groups/', getAllGroupsAPI),
    path('groups/my/', myGroupsAPI),
    
    # CHATS requests
    path('chats/', getChatsAPI),
    path('chats/<user_id>/', getMessagesAPI),
    path('chats/<user_id>/', sendMessageAPI),
    
    
    # TODO: remove after test
    path('auth/test/', protected_view),
]
