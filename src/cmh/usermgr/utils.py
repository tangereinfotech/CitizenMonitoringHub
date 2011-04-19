def get_or_create_citizen (mobile, name):
    from cmh.usermgr.models import Citizen

    try:
        citizen = Citizen.objects.get (mobile = mobile)
    except Citizen.DoesNotExist:
        citizen = Citizen.objects.create (mobile = mobile, name = name)

    return citizen
