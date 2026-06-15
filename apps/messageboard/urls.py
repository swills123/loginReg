from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:username>/', views.user_profile_view, name='user_profile'),
    path('board/', views.board_view, name='board'),
    path('board/delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
    path('board/comment/<int:post_id>/', views.add_comment_view, name='add_comment'),
    path('board/comment/delete/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),
    path('board/like/<int:post_id>/', views.toggle_like_view, name='toggle_like'),
    path('board/follow/<int:user_id>/', views.toggle_follow_view, name='toggle_follow'),
    path('board/follow_list/<int:user_id>/', views.follow_list_view, name='follow_list'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark_read/<int:notif_id>/', views.mark_read_view, name='mark_notification_read'),
    path('notifications/mark_all_read/', views.mark_all_read_view, name='mark_all_notifications_read'),
]
