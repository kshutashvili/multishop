from oscar.apps.order.admin import *  # noqa

from .models import OneClickOrder, \
    CallRequest, ShippingMethod, PaymentMethod, InstallmentPayment


class SimpleOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'when_created', 'order_status')


class OneClickAdmin(admin.ModelAdmin):
    list_display = ('phone', 'when_created',)


class CallRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'when_created', 'site')


class InstallmentPaymentAdmin(admin.ModelAdmin):
    list_display = ('phone', 'created', 'site')

class ShippingMethodAdmin(admin.ModelAdmin):
    fields = ('name_ru', 'name_uk', 'shipping_price')

class PaymentMethodAdmin(admin.ModelAdmin):
    fields = ('name_ru', 'name_uk', )

admin.site.register(ShippingMethod, ShippingMethodAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(OneClickOrder, OneClickAdmin)

admin.site.register(CallRequest, CallRequestAdmin)

admin.site.register(InstallmentPayment, InstallmentPaymentAdmin)
