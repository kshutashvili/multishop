# -*- coding: utf-8 -*-
from django.db.models import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from oscar.apps.basket.models import Line
from oscar.apps.basket.views import BasketAddView as OscarBasketAddView, \
    BasketView as OscarBasketView
from oscar.apps.catalogue.models import ProductImage
from oscar.apps.partner.strategy import Selector


class BasketAddView(OscarBasketAddView):
    def form_valid(self, form):
        super(BasketAddView, self).form_valid(form)
        selector = Selector()
        strategy = selector.strategy(request=self.request,
                                     user=self.request.user)
        purchase_info = strategy.fetch_for_product(product=self.product)
        price = purchase_info.price.excl_tax
        if price is None:
            price = 0
        img = self.product.primary_image()
        if isinstance(img, ProductImage):
            img_url = img.original.url
        else:
            img_url = img['original'].name

        return JsonResponse({'id': self.product.id, 'upc': self.product.upc,
                             'title': self.product.title,
                             'img': img_url,
                             'price': price})

    def form_invalid(self, form):
        super(BasketAddView, self).form_invalid(form)
        return JsonResponse({'errors': form.errors.values()})


class BasketView(OscarBasketView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(BasketView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            products = self.request.basket.lines.all()
            basket_products = []
            for line in products:
                img = line.product.primary_image()
                if isinstance(img, ProductImage):
                    img_url = img.original.url
                else:
                    img_url = img['original'].name
                data = {'id': line.product.id, 'upc': line.product.upc,
                        'title': line.product.title, 'img': img_url,
                        'price': line.line_price_excl_tax_incl_discounts / line.quantity,
                        'quantity': line.quantity}
                basket_products.append(data)
            return JsonResponse({'basket_products': basket_products})
        return super(BasketView, self).render_to_response(context,
                                                          **response_kwargs)


@require_POST
def delete_item_from_basket(request, *args, **kwargs):
    try:
        request.basket.lines.get(product__id=kwargs['id']).delete()
    except ObjectDoesNotExist:
        pass
    return HttpResponse(status=204)


@require_POST
def update_items_quantity(request):
    """
    update items quantity based on user input
    in future this functionality probably should be moved to
    view that will process the order
    """
    for product, quantity in request.POST.items():
        line = Line.objects.get(basket=request.basket, product__id=product)
        if request.basket.is_quantity_allowed(quantity):
            line.quantity = quantity
            line.save()
            return HttpResponse(status=200)
        else:
            return JsonResponse(
                {'errors': 'Превышено максимально доступное число товаров'})
