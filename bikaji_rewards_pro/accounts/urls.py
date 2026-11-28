
from django.urls import path

from .views import AddUserView, AdminUserCountView


app_name = "accounts"


urlpatterns = [
    path(
        "users/",
        AddUserView.as_view(),
        name="add-user"
    ),

    path(
        "admin/user-count/",
        AdminUserCountView.as_view(),
        name="admin-user-count"
    )
]
