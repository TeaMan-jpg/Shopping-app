from django.urls import path
from .views import AddBasket, AddReviews, Logins, Logouts, ShowBasket, DeleteBasket,AddProductView,ProductView,ProductsTemplateView, ShowReviews, SignUp,UpdateProductView,UpdateReviewView,DeleteProduct,DeleteReview,CreateSessionCheckout,paymentCancel,paymentSuccess,StripeWebhook
from django.conf import settings
from django.conf.urls.static import static
# urlpatterns = [
#     path("catalogue/",views.ProductView.as_view(),name="catalogue"),
#     # path("item/<int:itemID>",views.ItemView.as_view(),name="catalogue"),
#     # path("paymentSuccess/",views.ItemView.as_view(),name="catalogue"),
#     # path("paymentFail/",views.ItemView.as_view(),name="catalogue")
    
# ]
app_name = "shopping"


urlpatterns = [
    path('product/<int:pk>/', ProductView.as_view(), name='product-detail'),
    path('product/add/', AddProductView.as_view(), name='add-product'),
     path('add-to-basket/<int:pk>/', AddBasket.as_view(), name='add-to-basket'),
    path('basket/show/', ShowBasket.as_view(), name='show-basket'),
    path("",ProductsTemplateView.as_view(),name="show-products"),
    path("create_review/<int:pk>",AddReviews.as_view(),name="add-review"),
    path("login/",Logins.as_view(),name="login"),
    path("signUp/",SignUp.as_view(),name="signUp"),
    path("logout/",Logouts.as_view(),name="show-logout"),
    path("product/<int:pk>/update/",UpdateProductView.as_view(),name="update-product"),
    path("create_review/<int:pk>/update/",UpdateReviewView.as_view(),name="update-reviews"),
    path("product/<int:pk>/delete/",DeleteProduct.as_view(),name="delete-product"),
    path("create_review/<int:pk>/delete/",DeleteReview.as_view(),name="delete-review"),
    path("basket/product/<int:pk>/delete/",DeleteBasket.as_view(),name="delete-product-basket"),
    path("create-checkout-session/<int:pk>",CreateSessionCheckout.as_view(),name="create-checkout-session"),
    path("success/",paymentSuccess.as_view(),name="success"),
    path("cancel/",paymentCancel.as_view(),name="cancel"),
    path("webhooks/stripe/", StripeWebhook.as_view(), name="stripe-webhook")

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)