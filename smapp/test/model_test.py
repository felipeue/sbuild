from django.test import TestCase
from smapp.models import *
import nose.tools as nt
from django.contrib.auth.models import User


class InsertTest(TestCase):
    # Set user for test
    def setUp(self):
        self.usuario = User.objects.create_user(username="alejandro",
                                                email='ale@almacencooperativo.cl',
                                                first_name='alejandro',
                                                last_name='rios')



        felipe = User.objects.create_user(username="feli",
                                          email='feli@almacencooperativo.cl',
                                          first_name='felipe',
                                          last_name='rios')

    def test_models(self):
        # Test insert UserLt model
        owner = Owner.objects.create(userOrigin=self.usuario,
                                     rut="18346436-1",
                                     phone='+56971397675',
                                            )

        nt.assert_equal(owner.userOrigin, self.usuario)
        nt.assert_equal(owner.phone, "+56971397675")
        nt.assert_equal(owner.rut, "18346436-1")

        edificio = Building.objects.create(name="ed prueba",
                                           address="vergara 554",
                                           phone="+56971397675",
                                           owner=owner)

        nt.assert_equal(edificio.name, "ed prueba")
        nt.assert_equal(edificio.address, "vergara 554")
        nt.assert_equal(edificio.phone, "+56971397675")
        nt.assert_equal(edificio.owner, owner)

        departamento = Apartment.objects.create(number=1,
                                                floor=1,
                                                building=edificio)

        nt.assert_equal(departamento.number, 1)
        nt.assert_equal(departamento.floor, 1)
        nt.assert_equal(departamento.building, edificio)

        karin = User.objects.create_user(username="Karin",
                                         email="karin@almacencooperativo.cl",
                                         first_name="karin",
                                         last_name="schaa")

        residente = Resident.objects.create(userOrigin=karin,
                                            rut="7552796-9",
                                            phone="+56971397675",
                                            apartment=departamento)

        nt.assert_equal(residente.userOrigin, karin)
        nt.assert_equal(residente.rut, '7552796-9')
        nt.assert_equal(residente.phone, '+56971397675')
        nt.assert_equal(residente.apartment, departamento)

        jose = User.objects.create_user(username="Jose",
                                        email="jose@almacencooperativo.cl",
                                        first_name="jose",
                                        last_name="perez")

        conserje = Consierge.objects.create(userOrigin=jose,
                                            rut='18346436-1',
                                            phone='+56971397675',
                                            building=edificio)

        nt.assert_equal(conserje.userOrigin,jose)
        nt.assert_equal(conserje.rut, '18346436-1')
        nt.assert_equal(conserje.phone, '+56971397675')
        nt.assert_equal(conserje.building, edificio)

        visita = Visit.objects.create(name='visita',
                                      rut='18346436-1',
                                      date='2016-11-14 20:00:00',
                                      resident=residente,
                                      note='Test',
                                      received=True)

        nt.assert_equal(visita.name, 'visita')
        nt.assert_equal(visita.rut, '18346436-1')
        nt.assert_equal(visita.date, '2016-11-14 20:00:00')
        nt.assert_equal(visita.resident, residente)
        nt.assert_equal(visita.received, True)

        publicacion = Publication.objects.create(resident=residente,
                                                 title='titulo',
                                                 date='2016-11-14',
                                                 hour='00:00:00',
                                                 message='mensaje',
                                                 type='1')

        nt.assert_equal(publicacion.resident,residente)
        nt.assert_equal(publicacion.title, 'titulo')
        nt.assert_equal(publicacion.date, '2016-11-14')
        nt.assert_equal(publicacion.hour, '00:00:00')
        nt.assert_equal(publicacion.message, 'mensaje')
        nt.assert_equal(publicacion.type, '1')

        evento = Event.objects.create(title='titulo',
                                      start='2016-11-14 20:00:00',
                                      end='2016-11-14 20:00:00',
                                      all_day='0',
                                      resident=residente,
                                      location='locacion')

        nt.assert_equal(evento.title, 'titulo')
        nt.assert_equal(evento.start, '2016-11-14 20:00:00')
        nt.assert_equal(evento.end, '2016-11-14 20:00:00')
        nt.assert_equal(evento.all_day, '0')
        nt.assert_equal(evento.resident, residente)
        nt.assert_equal(evento.location, 'locacion')

        arriendo = Rent.objects.create(month='Enero',
                                       amount=10000,
                                       resident=residente,
                                       date='2016-11-14 20:00:00')

        nt.assert_equal(arriendo.month, 'Enero')
        nt.assert_equal(arriendo.amount, 10000)
        nt.assert_equal(arriendo.resident, residente)
        nt.assert_equal(arriendo.date, '2016-11-14 20:00:00')