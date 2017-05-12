from oscar.apps.order.admin import *  # noqa

from .models import SimpleOrder, ShippingMethod, PaymentMethod, OneClickOrder, \
    CallRequest


class SimpleOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'when_created', 'order_status')


class OneClickAdmin(admin.ModelAdmin):
    list_display = ('phone', 'when_created',)


class CallRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'when_created', 'site')


admin.site.register(SimpleOrder, SimpleOrderAdmin)
admin.site.register(ShippingMethod)
admin.site.register(PaymentMethod)
admin.site.register(OneClickOrder, OneClickAdmin)

admin.site.register(CallRequest, CallRequestAdmin)

admin.site.unregister(Order)
admin.site.unregister(Line)
admin.site.unregister(LinePrice)
admin.site.unregister(LineAttribute)
admin.site.unregister(OrderNote)
admin.site.unregister(PaymentEvent)
admin.site.unregister(PaymentEventType)
admin.site.unregister(CommunicationEvent)
admin.site.unregister(ShippingEvent)
admin.site.unregister(ShippingEventType)
admin.site.unregister(OrderDiscount)
