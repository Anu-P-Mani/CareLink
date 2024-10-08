from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseNotFound
from django.contrib import messages
from .models import Medcart, Medicine_inventory
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

# Create your views here.


@login_required
def add_to_cart(request, id):
    try:
        device = DeviceInformation.objects.get(id=id)
        print(device)
    except DeviceInformation.DoesNotExist:
        return HttpResponseNotFound("Device does not exist")

    user = request.user
    
    existing_cart_item = Divicecart.objects.filter(user=user, device=device).first()
    if existing_cart_item:
        
        existing_cart_item.quantity = 1
        existing_cart_item.save()
    else:
      
        cart = Divicecart.objects.create(user=user, device=device,quantity=1)
        cart.save()
    
    return redirect("cart_view")

def cart_view(request):
    user= request.user
    cart = Divicecart.objects.filter(user=user)
    total = 0
    for i in cart:
        total += i.quantity * i.device.price

    return render(request, "cart/add_to_cart.html", {'cart': cart, 'total': total})




def devremove_cart_item(request, id):
    cart_item = get_object_or_404(Divicecart, id=id)

    cart_item.delete()

    return redirect('cart_view')


def OrderForm(request):
    if(request.method=="POST"):
        address=request.POST['address']
        phone=request.POST['phone']
        user=request.user
        cart=Divicecart.objects.filter(user=user)
        total=0
        for i in cart:

            
            total=total+i.quantity*i.device.price
            obj=Order.objects.create(user=user,address=address,phone=phone,device_id = i.device,no_of_items=i.quantity,order_status="paid", total_price=total)
            obj.save()
        cart.delete()    
        return redirect("order_confirm_view")

    return render(request,"cart/order.html")


def order_confirm_view(request):
    return render(request, "cart/order_confirm.html")


@login_required
def medadd_to_cart(request, id):
    user = request.user

    medicine = get_object_or_404(Medicine_inventory, id=id)
    try:
        cart_item = Medcart.objects.get(user=user, medicine=medicine)
        if cart_item.quantity < medicine.quanity_availble:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, "Sorry, this product is out of stock.")
    except Medcart.DoesNotExist:
        if medicine.quanity_availble > 0:
            cart_item = Medcart.objects.create(user=user, medicine=medicine, quantity=1)
            cart_item.save()
        else:
            messages.error(request, "Sorry, this product is out of stock.")
    return redirect('med_cart_view')


def med_cart_view(request):
    total = 0
    user = request.user
    cart = Medcart.objects.filter(user=user)
    for item in cart:
        total += item.quantity * item.medicine.price
    return render(request, 'medicine_cart_view.html', {'cart': cart, 'total': total})

def medcart_view(request):
    user = request.user
    cart = Medcart.objects.filter(user=user)
    total = 0
    for item in cart:
        total += item.subtotal()

    return render(request, "cart/medicine_cart_view.html", {'cart': cart, 'total': total})

def remove_cart_item(request, id):
    cart_item = get_object_or_404(Medcart, id=id)

    cart_item.delete()

    return redirect('med_cart_view')



def MedorderForm(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        acc_number = request.POST.get('Acc_number')
        user = request.user
        cart = Medcart.objects.filter(user=user)
        total = 0
        for item in cart:
            total += item.quantity * item.medicine.price

        try:
            acct = Account.objects.get(accnumber=acc_number)
            if acct.balance > total:
                acct.balance -= total
                acct.save()
                for item in cart:
                    order = MedicineOrder.objects.create(
                        user=user,
                        address=address,
                        phone=phone,
                        medicine=item.medicine,
                        no_of_items=item.quantity,
                        order_status="paid",
                        total_price=total
                    )
                    order.save()
                    item.medicine.quanity_availble -= item.quantity
                    item.medicine.save()
                cart.delete()
                msg = 'Order placed successfully'
                return render(request, 'cart/medpayment.html', {'msg': msg})
            else:
                msg = "Insufficient balance. You can't place the order."
                return render(request, 'cart/medpayment.html', {'msg': msg})
        except Account.DoesNotExist:
            msg = "Account doesn't exist. Please enter a valid account number."
            return render(request, 'cart/medpayment.html', {'msg': msg})

    return render(request, "cart/orderform.html")




def medorder_confirm_view(request):
    return render(request, "cart/medpayment.html")


def itemcart_remove(request,id):
    try:
        med = Medicine_inventory.objects.get(id=id)
        print(med)
    except Medicine_inventory.DoesNotExist:
        raise Http404("Medicine inventory with id {} does not exist".format(id))
    user=request.user
    try:
        cart=Medcart.objects.get(user=user,medicine=med)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()

        else:
            cart.delete()

    except:
        pass
    return redirect('med_cart_view')


def order_view(request):
    user = request.user
    orders = MedicineOrder.objects.filter(user=user)
    return render(request, 'cart/order_view.html', {'orders': orders})

class order_details(DetailView):
    template_name = "cart/order_details.html"
    model = MedicineOrder
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
