import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smproject.settings')
import django
django.setup()
from smapp.models import *


def add_user(nombre, apellido, rut, clave, correo):
    u = User.objects.get_or_create(username=rut, first_name=nombre, last_name=apellido, email=correo)[0]
    u.set_password('ita8192198')
    u.save()
    return u


def add_concierge(conserje, telefono, edificio):
    e = Consierge.objects.get_or_create(userOrigin=conserje, phone=telefono, building=edificio)[0]
    e.save()
    return e


def add_resident(residente, telefono, depa):
    e = Resident.objects.get_or_create(userOrigin=residente, phone=telefono)[0]
    e.apartment.add(depa)
    e.save()
    return e


def add_owner(dueno, telefono):
    e = Owner.objects.get_or_create(userOrigin=dueno, phone=telefono)[0]
    e.save()
    return e


def add_building(nombre, direccion, telefono, dueno):
    c = Building.objects.get_or_create(name=nombre, address=direccion, phone=telefono, owner=dueno)[0]
    c.save()
    return c


def add_apartment(numero, piso, edificio):
    a = Apartment.objects.get_or_create(number=numero, floor=piso, building=edificio)[0]
    a.save()
    return a


def add_visit(nombre, r, fecha, residente, comentario, recibido, consierge):
    v = Visit.objects.get_or_create(name=nombre, rut=r, date=fecha, resident=residente, note=comentario, received=recibido, consierge=consierge)[0]
    v.save()
    return v


def add_publication(publicador, titulo, fecha, hora, mensaje, tipo):
    p = Publication.objects.get_or_create(publisher=publicador, title=titulo, date=fecha, hour=hora, message=mensaje, type=tipo)[0]
    p.save()
    return p


def add_location(nombre, edificio):
    l = Location.objects.get_or_create(name=nombre, building=edificio)[0]
    l.save()
    return l


def add_event(titulo, inicio, fin, td, residente, locacion):
    e = Event.objects.get_or_create(title=titulo, start=inicio, end=fin, all_day=td, resident=residente, location=locacion)[0]
    e.save()
    return e


def add_rent(mes, monto, residente, fecha):
    r = Rent.objects.get_or_create(month=mes,amount=monto, resident=residente, date=fecha)
    return r


def populate():

    x = add_user('felipe', 'rios', '18346436-1', 'ita8192198', 'felipe.rios@mail.udp.cl')

    y = add_user('Karin', 'schaa', '7552796-9', 'ita8192198', 'mail@mail.cl')

    z  = add_user('Alejandro', 'rios', '7970991-3', 'ita8192198', 'mail@mail.cl')

    dueno = add_owner(z, '8192198')

    edificio = add_building('prueba', 'isla 89798', '8192198', dueno)

    departamento = add_apartment(1, 1, edificio)

    conserje = add_concierge(x, '9181898', edificio)

    residente = add_resident(y, '8192898', departamento)

    add_visit('jorge', '18346436-1', datetime.now(), residente, 'bien prueba', 1, conserje)

    locacion = add_location('quincho', edificio)

    add_event('cumple prueba', '2017-01-24 15:06:33', '2017-01-24 15:06:33', 0, residente, locacion)

    add_rent('Mayo', 5000, residente, datetime.now())

    add_publication(x, 'prueba', '2017-01-24', '12:51', 'mensaje prueba', 'Evento')


# Start execution here!
if __name__ == '__main__':
    print "Iniciando..."
    populate()




