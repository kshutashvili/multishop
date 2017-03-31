from collections import defaultdict
from django.contrib.sites.shortcuts import get_current_site

from contacts.models import PhoneNumber


def show_phone_numbers(request):
    site_obj = get_current_site(request)
    phone_numbers = defaultdict(list)
    limits = {PhoneNumber.OPERATOR.KIEVSTAR: 1,
              PhoneNumber.OPERATOR.LIFE: 1,
              PhoneNumber.OPERATOR.VODAFONE: 1}
    obj_list = PhoneNumber.objects.filter(site=site_obj)
    for phone in obj_list.iterator():
        if phone.operator not in limits:
            continue
        if len(phone_numbers[phone.operator]) < limits[phone.operator]:
            phone_numbers[phone.operator].append(phone.get_national_format())
        else:
            del limits[phone.operator]
        if not limits:
            break
    return {'phone_numbers': phone_numbers}
