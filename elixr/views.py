from django.views import generic
from .forms import SignUpForm
from .models import Ship, Suit
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render, reverse
from .models import Suit, Ship, OrderedShip, OrderedSuit, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# from paystack.signals import payment_verified
from django.dispatch import receiver


class SignUp(generic.CreateView):
    form_class = SignUpForm
    template_name = 'elixr/signup.html'
    success_url = reverse_lazy('login')


# Ships
class ShipList(generic.ListView):
    model = Ship


class ShipDetail(generic.DetailView):
    model = Ship

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


# Suits
class SuitList(generic.ListView):
    model = Suit


class SuitDetail(generic.DetailView):
    model = Suit


################################################ The meat of it all ################################################

# adding to cart
@login_required
def add_suit_to_cart(request, slug):
    suit = get_object_or_404(Suit, slug=slug)
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.ord_suits.filter(suit__slug=suit.slug).exists():
            ord_suit = order.ord_suits.filter(suit__slug=suit.slug)[0]
            ord_suit.quantity += 1
            ord_suit.save()
            messages.success(request, 'Added {} of {} to cart'.format(
                ord_suit.quantity, ord_suit.suit.name))
            return redirect("suit_detail", slug=suit.slug)

        else:
            ordered_suit = OrderedSuit.objects.create(
                suit=suit,
                quantity=1
            )
            ordered_suit.save()
            order.ord_suits.add(ordered_suit)
            order.save()
            messages.success(request, "{} added to cart!".format(
                ordered_suit.suit.name))
            return redirect("suit_detail", slug=suit.slug)

    else:
        order = Order.objects.create(buyer=request.user, ordered=False)
        order.save()
        ordered_suit = OrderedSuit.objects.create(
            suit=suit,
            quantity=1
        )
        ordered_suit.save()
        order.ord_suits.add(ordered_suit)
        order.save()
        messages.success(request, "{} added to cart!".format(
            ordered_suit.suit.name))
        return redirect("suit_detail", slug=suit.slug)


@login_required
def add_ship_to_cart(request, slug):
    ship = get_object_or_404(Ship, slug=slug)
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.ord_ships.filter(ship__slug=ship.slug).exists():
            ord_ship = order.ord_ships.filter(ship__slug=ship.slug)[0]
            ord_ship.quantity += 1
            ord_ship.save()
            messages.success(request, 'Added {} of {} to cart'.format(
                ord_ship.quantity, ord_ship.ship.name))
            return redirect("ship_detail", slug=ship.slug)

        else:
            ordered_ship = OrderedShip.objects.create(
                ship=ship,
                quantity=1
            )
            ordered_ship.save()
            order.ord_ships.add(ordered_ship)
            order.save()
            messages.success(request, "{} added to cart!".format(
                ordered_ship.ship.name))
            return redirect("ship_detail", slug=ship.slug)

    else:
        order = Order.objects.create(buyer=request.user, ordered=False)
        order.save()
        ordered_ship = OrderedShip.objects.create(
            ship=ship,
            quantity=1
        )
        ordered_ship.save()
        order.ord_ships.add(ordered_ship)
        order.save()
        messages.success(request, "{} added to cart!".format(
            ordered_ship.ship.name))
        return redirect("ship_detail", slug=ship.slug)


def remove_ship_finally(request, slug):
    ship = get_object_or_404(Ship, slug=slug)
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.ord_ships.filter(ship__slug=ship.slug).exists():
            ord_ship = order.ord_ships.filter(ship__slug=ship.slug)[0]
            order.ord_ships.remove(ord_ship)
            order.save()
            messages.success(
                request, 'Removed {} from cart'.format(ord_ship.ship.name))
            return redirect("cart")
    else:
        messages.warning(request, "You do not have an order")


def remove_suit_finally(request, slug):
    suit = get_object_or_404(Suit, slug=slug)
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.ord_suits.filter(suit__slug=suit.slug).exists():
            ord_suit = order.ord_suits.filter(suit__slug=suit.slug)[0]
            order.ord_suits.remove(ord_suit)
            order.save()
            messages.success(
                request, 'Removed {} from cart'.format(ord_suit.suit.name))
            return redirect("cart")
    else:
        messages.warning(request, "You do not have an order")


def remove_suit_single(request, slug):
    suit = get_object_or_404(Suit, slug=slug)
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.ord_suits.filter(suit__slug=suit.slug).exists():
            ord_suit = order.ord_suits.filter(suit__slug=suit.slug)[0]
            ord_suit.quantity -= 1
            ord_suit.save()
            if ord_suit.quantity == 0:
                order.ord_suits.remove(ord_suit)
            order.save()
            return redirect("cart")
    else:
        messages.warning(request, "You do not have an order")


def remove_ship_single(request, slug):
    ship = get_object_or_404(Ship, slug=slug)
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.ord_ships.filter(ship__slug=ship.slug).exists():
            ord_ship = order.ord_ships.filter(ship__slug=ship.slug)[0]
            ord_ship.quantity -= 1
            ord_ship.save()
            if ord_ship.quantity == 0:
                order.ord_ships.remove(ord_ship)
            order.save()
            return redirect("cart")
    else:
        messages.warning(request, "You do not have an order")


@login_required
def order_view(request):
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    undelivered_order = Order.objects.filter(
        buyer=request.user, ordered=True, delivered=False)
    if undelivered_order.exists() and order_qs.exists():
        undelivered_order = undelivered_order[0]
        user_order = order_qs[0]
        return render(request, 'elixr/order.html', {'order': user_order, 'undelivered_order': undelivered_order})
    if order_qs.exists():
        user_order = order_qs[0]
        return render(request, 'elixr/order.html', {'order': user_order})
    if undelivered_order.exists():
        undelivered_order = undelivered_order[0]
        return render(request, 'elixr/order.html', {'undelivered_order': undelivered_order})


def customer_info(request):
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        user_order = order_qs[0]
        amount = user_order.total()
        amount = float(amount)
        email = user_order.buyer.email
    return render(request, 'elixr/payment.html', {'amount': amount, 'email': email})


# @receiver(payment_verified)
# def on_payment_received(request,sender,ref,amount,**kwargs):
#     order_qs = Order.objects.filter(buyer=request.user,ordered=False)
#     if order_qs.exists():
#         user_order = order_qs[0]
#         user_order.paystack_ref_code = ref
#         user_order.paystack_amount = amount
#         user_order.ordered = True
#         user_order.save()
#     messages.info(request,"Payment successful")
