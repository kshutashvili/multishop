from collections import defaultdict
from django.contrib.sites.shortcuts import get_current_site

from contacts.models import PhoneNumber, SocialNetRef


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


def social_networks_ref(request):
    site_obj = get_current_site(request)
    social_networks_refs = defaultdict(list)
    limits = {SocialNetRef.REFTYPES.FACEBOOK: 1,
              SocialNetRef.REFTYPES.VKONTAKTE: 1,
              SocialNetRef.REFTYPES.MAILRU: 1,
              SocialNetRef.REFTYPES.TWITTER: 1,
              SocialNetRef.REFTYPES.ODNOKLASSNIKI: 1,
              SocialNetRef.REFTYPES.PINTEREST: 1,
              SocialNetRef.REFTYPES.GOOGLE: 1,
              SocialNetRef.REFTYPES.YOUTUBE: 1}
    refs_list = SocialNetRef.objects.filter(site=site_obj)
    for ref in refs_list.iterator():
        if ref.ref_type not in limits:
            continue
        if len(social_networks_refs[ref.ref_type]) < limits[ref.ref_type]:
            social_networks_refs[ref.ref_type].append(ref.reference)
        else:
            del limits[ref.ref_type]
        if not limits:
            break
    return {'social_networks_refs': social_networks_refs}
