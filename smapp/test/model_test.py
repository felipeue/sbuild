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