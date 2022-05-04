from django.db import models
from django.utils.translation import gettext_lazy as _


class StateChoices(models.TextChoices):
    CIUDAD_DE_MEXICO = ("MX-CMX", _("Ciudad de Mexico"))
    AGUASCALIENTES = ("MX-AGU", _("Aguascalientes"))
    BAJA_CALIFORNIA = ("MX-BCN", _("Baja California"))
    BAJA_CALIFORNIA_SUR = ("MX-BCS", _("Baja California Sur"))
    CAMPECHE = ("MX-CAM", _("Campeche"))
    COAHUILA_DE_ZARAGOZA = ("MX-COA", _("Coahuila de Zaragoza"))
    COLIMA = ("MX-COL", _("Colima"))
    CHIAPAS = ("MX-CHP", _("Chiapas"))
    CHIHUAHUA = ("MX-CHH", _("Chihuahua"))
    DURANGO = ("MX-DUR", _("Durango"))
    GUANAJUATO = ("MX-GUA", _("Guanajuato"))
    GUERRERO = ("MX-GRO", _("Guerrero"))
    HIDALGO = ("MX-HID", _("Hidalgo"))
    JALISCO = ("MX-JAL", _("Jalisco"))
    MEXICO = ("MX-MEX", _("Mexico"))
    MICHOACAN_DE_OCAMPO = ("MX-MIC", _("Michoacan de Ocampo"))
    MORELOS = ("MX-MOR", _("Morelos"))
    NAYARIT = ("MX-NAY", _("Nayarit"))
    NUEVO_LEON = ("MX-NLE", _("Nuevo Leon"))
    OAXACA = ("MX-OAX", _("Oaxaca"))
    PUEBLA = ("MX-PUE", _("Puebla"))
    QUERETARO = ("MX-QUE", _("Queretaro"))
    QUINTANA_ROO = ("MX-ROO", _("Quintana Roo"))
    SAN_LUIS_POTOSI = ("MX-SLP", _("San Luis Potosi"))
    SINALOA = ("MX-SIN", _("Sinaloa"))
    SONORA = ("MX-SON", _("Sonora"))
    TABASCO = ("MX-TAB", _("Tabasco"))
    TAMAULIPAS = ("MX-TAM", _("Tamaulipas"))
    TLAXCALA = ("MX-TLA", _("Tlaxcala"))
    VERACRUZ_DE_IGNACIO_DE_LA_LLAVE = ("MX-VER", _("Veracruz de Ignacio de la Llave"))
    YUCATAN = ("MX-YUC", _("Yucatan"))
    ZACATECAS = ("MX-ZAC", _("Zacatecas"))


class PhysicalBuildChoices(models.TextChoices):
    SLIM = ("S", _("Slim"))
    REGULAR = ("R", _("Regular"))
    HEAVY = ("H", _("Heavy"))


class ComplexionChoices(models.TextChoices):
    BROWN = ("BR", _("Brown"))
    LIGHT_BROWN = ("LB", "Light brown")
    DARK_BROWN = ("DB", "Dark brown")
    WHITE = ("WH", _("White"))
    BLACK = ("BL", _("Black"))


class SexChoices(models.TextChoices):
    MALE = ("M", _("Male"))
    FEMALE = ("F", _("Female"))
    OTHER = ("O", _("Other"))


class AlertType(models.TextChoices):
    ALBA = ("AL", _("Alba"))
    AMBER = ("AM", _("Amber"))
    ODISEA = ("OD", _("Odisea"))
