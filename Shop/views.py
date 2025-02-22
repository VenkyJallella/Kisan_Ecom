from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from .forms import CheckoutForm
import razorpay
from django.conf import settings
from .models import Order
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

def Product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products':products})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()
    
    return redirect("cart")

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    
    return render(request, "cart.html", {"cart_items": cart_items, "total": total})


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            # Clear Cart After Checkout
            cart_items.delete()

            return redirect("payment", order_id=order.id)  # Redirect to Payment Page

    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {"form": form, "total": total_price})

def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create Razorpay Order
    razorpay_order = client.order.create({
        "amount": int(order.total_price * 100),  # Razorpay accepts amount in paise
        "currency": "INR",
        "payment_capture": "1"
    })
    
    context = {
        "order": order,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID
    }

    return render(request, "payment.html", context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_paid = True
    order.save()
    
    return HttpResponse("Payment successful! Your order has been placed.")

def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    template_path = "invoice_template.html"
    context = {"order": order}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Invoice_{order.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response

@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove if quantity is 0

    return redirect("cart")

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect("cart")
