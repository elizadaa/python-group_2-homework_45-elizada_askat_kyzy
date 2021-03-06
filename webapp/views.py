from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from webapp.models import Order, Food, OrderFood
from webapp.forms import OrderFoodForm, FoodForm, OrderForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    permission_required = 'webapp.view_order'


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    permission_required = 'webapp.view_order'


class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_create.html'
    permission_required = 'webapp.add_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.operator = self.request.user
        return super().form_valid(form)



class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_update.html'
    permission_required = 'webapp.change_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['pk'])
        return super().form_valid(form)



class OrderRejectView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Order
    template_name = 'order_cancel.html'
    permission_required = 'webapp.delete_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = 'canceled'
        self.object.save()
        return HttpResponseRedirect(success_url)



class OrderDeliverView(PermissionRequiredMixin, View):
    permission_required = 'webapp.deliver_order'

    def get(self, *args, **kwargs):
        object = get_object_or_404(Order, pk=kwargs['pk'])
        success_url = reverse('webapp:order_detail', kwargs={'pk': object.pk})
        if object.status == 'preparing':
            object.status = 'on way'
            object.courier = self.request.user
            object.save()
        elif object.status == 'on way':
            if object.courier == self.request.user:
                object.status = 'delivered'
                object.save()
        return HttpResponseRedirect(success_url)




class OrderFoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'
    permission_required = 'webapp.add_orderfood'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})



class OrderFoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_update.html'
    permission_required = 'webapp.change_orderfood'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

    def form_valid(self, form):
        get_object_or_404(OrderFood, pk=self.kwargs['pk'])
        return super().form_valid(form)



class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_delete.html'
    permission_required = 'webapp.delete_orderfood'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})



class FoodListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Food
    template_name = 'food_list.html'
    permission_required = 'webapp.view_food'


class FoodDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Food
    template_name = 'food_detail.html'
    permission_required = 'webapp.view_food'





class FoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Food
    form_class = FoodForm
    template_name = 'food_create.html'
    permission_required = 'webapp.add_food'


    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})




class FoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Food
    form_class = FoodForm
    template_name = 'food_update.html'
    permission_required = 'webapp.change_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})


