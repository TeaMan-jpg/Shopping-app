from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView,DetailView,CreateView,DeleteView,TemplateView,UpdateView
import stripe
from .models import BasketItems, Product,Basket,Review
from .forms import ProductForm, ReviewForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = 'sk_test_51Q3xqaL8H6bkmPi1a0EWnNWN8YfMxeCdj1NEZkEeKfNKxSbmTUxCsvg7L8LCbE7vQhR2vZII6rwatFrt72keD2oM00PojR6WMa'

endpoint_secret = 'whsec_b2d5e59a334006103e831f438f71b380b277ca48a3d811b2deffdf7e1bad277e'
class ProductView(DetailView):
    model = Product
    template_name = "shopping/productPage.html"
    context_object_name = "product"


    def get_queryset(self,querySet=None):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        return context

class CreateSessionCheckout(View):
    
    
    def post(self, request, *args, **kwargs):

        basket = Basket.objects.get(user=self.request.user)

        basketItems = BasketItems.objects.get(basket=basket)
        
        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[ {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(basketItems.product.price) * 100,
                        "product_data": {
                            "name": basketItems.product.name,
                            "description": basketItems.product.desc,
                            
                        },
                    },
                    "quantity": 1,
                }],
        mode='payment',
        success_url='http://127.0.0.1:8000/shopping/success',
        cancel_url='http://127.0.0.1:8000/shopping/cancel',
    )

        return redirect(session.url, code=303)

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhook(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            print('Error parsing payload: {}'.format(str(e)))
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print('Error verifying webhook signature: {}'.format(str(e)))
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object # contains a stripe.PaymentIntent
            print('PaymentIntent was successful!')
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object # contains a stripe.PaymentMethod
            print('PaymentMethod was attached to a Customer!')
        # ... handle other event types
        elif event.type == 'checkout.session.completed':
            print("Session completed")
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)
            
class paymentSuccess(View):
    template_name = "shopping/payment_success.html"

    def get(self, request, *args, **kwargs):
        # check_out_session_id = request.GET.get('session_id',None)
        # session = stripe.checkout.Session.retrieve(check_out_session_id)
        # customer = stripe.Customer.retrieve(session.customer)
        return render(request,self.template_name,{})
    def post(self, request, *args, **kwargs):
        basket = Basket.objects.get(user=self.request.user)

        basketItems = BasketItems.objects.get(basket=basket)


        if basketItems.quantity > 0:
            basketItems.quantity -= 1
            basketItems.save()
        else:
            print("quantity is empty")


        return render(request,self.template_name,{})



class paymentCancel(View):
    template_name = "shopping/payment_cancelled.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{})
class ProductsTemplateView(TemplateView):
    template_name = "shopping/productsPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products'] = Product.objects.all()
        return context
    

# class ProductsView(ListView):
#     model = Product
#     template_name = "shopping/productsPage.html"
#     context_object_name = "context"

    
#     def get_queryset(self):
#         return Product.objects.all()

class SignUp(View):
    template_name = "shopping/signUp.html"

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{})
    
    def post(self,request,*args,**kwargs):
        
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']


            if (username and email and password):

                if (User.objects.filter(username=username,email=email).exists()):
                    messages.error(request,"User already exists")
                    return redirect("/shopping/login")

                user = User.objects.create_user(username=username,password=password,email=email)
            

                user = authenticate(request,username=username,password=password)

                if user is not None:
                    messages.success(request,"Login successful")
                    login(request,user)
                    return redirect("/shopping/product/add/")
                else:
                    messages.error(request,"Login Failed")
                    return render(request,self.template_name,{})

class Logouts(View):
    template_name = "shopping/logout.html"

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{})
    
    def post(self,request,*args,**kwargs):
            
           logout(request)
           return redirect("/shopping/signUp")


class Logins(View):
    template_name = "shopping/login.html"

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{})
    
    def post(self,request,*args,**kwargs):
        
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request,username=username,password=password)

            if user is not None:
                messages.success(request,"Login successful")
                login(request,user)
                return redirect("/shopping/product/add/")
            else:
                messages.error(request,"Login Failed")
                return render(request,self.template_name,{})

class AddProductView(CreateView):
    model = Product
    # fields = ['name','price','seller','desc','quantity','basket']
    template_name = "shopping/product_create.html"
    form_class = ProductForm

    def form_valid(self, form):
       print(form.cleaned_data)
       form.instance.author = self.request.user
       print(form.instance.author)
   
       return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("shopping:show-products")
    

class UpdateProductView(UpdateView):
    model = Product
    # fields = ['name','price','seller','desc','quantity','basket']
    template_name = "shopping/product_create.html"
    form_class = ProductForm

    def form_valid(self, form):
       print(form.cleaned_data)
       form.instance.author = self.request.user
       print(form.instance.author)
   
       return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("shopping:show-products")



class DeleteProduct(DeleteView):
    model = Product
    template_name = "shopping/deleteProduct.html"

    def get_success_url(self):
        return reverse("shopping:show-products")
    
class AddReviews(CreateView):
    model = Review
    fields = ['title','rating','desc']
    
    # form_class = ReviewForm

    template_name = "shopping/review_create.html"



    def get_success_url(self):
        return reverse("shopping:product-detail",kwargs={"pk":self.kwargs["pk"]})
    
    def form_valid(self, form):

        product = get_object_or_404(Product,pk=self.kwargs['pk'])

   
        form.instance.author = self.request.user
        form.instance.product = product
        return super().form_valid(form)
    
class UpdateReviewView(UpdateView):
    model = Review
    fields = ['title','rating','desc']
    template_name = "shopping/review_create.html"


    def get_success_url(self):
        return reverse("shopping:show-products")
    
    def form_valid(self, form):

      

   
        form.instance.author = self.request.user
     
        return super().form_valid(form)



    
    

class ShowReviews(ListView):
    model = Review
    template_name = "shopping/ProductPage.html"
    context_object_name = "reviews"

    
    def get_queryset(self):
        return Review.objects.all()

class AddBasket(View):
    template_name = "shopping/BasketAddPage.html"

    def get(self, request, *args, **kwargs):
        # Handle GET request (for example, showing products or basket)
        return render(request,self.template_name,{})  # Ensure 'shopping:show-products' exists
    
    def post(self, request, *args, **kwargs):
        # Get the product being added from the URL
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        # Get or create the user's basket
        basket, created = Basket.objects.get_or_create(user=request.user)

        basket_item,created = BasketItems.objects.get_or_create(basket=basket,product=product)


        if not created:
            basket_item.quantity += 1
            basket_item.save()
        # Add the product to the basket
        # basket.products.add(product)
        # print(basket.products.all())

        # Redirect to the product detail page after adding to basket
        return redirect('shopping:product-detail', pk=product.pk)

class ShowBasket(ListView):
    model = Basket
    template_name = "shopping/showBasket.html"
    context_object_name = 'basket_items'  # Use this in your template to reference items

    def get_queryset(self):
        # Fetch the user's basket
        basket = Basket.objects.get(user=self.request.user)
        print(basket)  # Get the basket for the logged-in user

        basketItem = BasketItems.objects.filter(basket=basket)

        # if basket:
        #     return basket.products.all()  # Return all products in the user's basket
        # return []

        return basketItem
class DeleteBasket(DeleteView):
    model = Product
    template_name = "shopping/BasketDeletePage.html"
    

    def get_success_url(self):
        return reverse("shopping:show-products")

class DeleteReview(DeleteView):
    model = Review
    template_name = "shopping/ReviewDeletePage.html"


    def get_success_url(self):
        return reverse("shopping:show-products")

class ShowOneReview(DetailView):
    model = Review
    template_name = "shopping/reviewPage.html"



class Checkout(View):
    template_name = "shopping/productPage.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{})
    
    