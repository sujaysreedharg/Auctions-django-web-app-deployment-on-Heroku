from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisitng", views.createlisting, name="createlisting"),
    path("activelisting", views.activelisting, name="activelisting"),
    path("viewlisting/<int:product_id>", views.viewlisting, name="viewlisting"),
    path("addcomment/<int:product_id>", views.comment, name="addcomment"),
    path("addtowatchlist/<int:product_id>",views.addtowatchlist, name="addtowatchlist"),
    path("mywatchlist",views.mywatchlist, name="mywatchlist"),
    path("category/<str:categ>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),


]
from <app> import settings
urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
