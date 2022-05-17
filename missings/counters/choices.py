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

    def abbr(self):
        return {
            self.CIUDAD_DE_MEXICO: "cdmx",
            self.AGUASCALIENTES: "ags",
            self.BAJA_CALIFORNIA: "bc",
            self.BAJA_CALIFORNIA_SUR: "bcs",
            self.CAMPECHE: "camp",
            self.COAHUILA_DE_ZARAGOZA: "coah",
            self.COLIMA: "col",
            self.CHIAPAS: "chis",
            self.CHIHUAHUA: "chih",
            self.DURANGO: "dgo",
            self.GUANAJUATO: "gto",
            self.GUERRERO: "gro",
            self.HIDALGO: "hgo",
            self.JALISCO: "jal",
            self.MEXICO: "edomex",
            self.MICHOACAN_DE_OCAMPO: "mich",
            self.MORELOS: "mor",
            self.NAYARIT: "nay",
            self.NUEVO_LEON: "nl",
            self.OAXACA: "oax",
            self.PUEBLA: "pue",
            self.QUERETARO: "qro",
            self.QUINTANA_ROO: "qroo",
            self.SAN_LUIS_POTOSI: "slp",
            self.SINALOA: "sin",
            self.SONORA: "son",
            self.TABASCO: "tab",
            self.TAMAULIPAS: "tamps",
            self.TLAXCALA: "tlax",
            self.VERACRUZ_DE_IGNACIO_DE_LA_LLAVE: "ver",
            self.YUCATAN: "yuc",
            self.ZACATECAS: "zac",
        }.get(self)

    @classmethod
    def from_abbr(cls, abbr):
        return {
            "cdmx": cls.CIUDAD_DE_MEXICO,
            "ags": cls.AGUASCALIENTES,
            "bc": cls.BAJA_CALIFORNIA,
            "bcs": cls.BAJA_CALIFORNIA_SUR,
            "camp": cls.CAMPECHE,
            "coah": cls.COAHUILA_DE_ZARAGOZA,
            "col": cls.COLIMA,
            "chis": cls.CHIAPAS,
            "chih": cls.CHIHUAHUA,
            "dgo": cls.DURANGO,
            "gto": cls.GUANAJUATO,
            "gro": cls.GUERRERO,
            "hgo": cls.HIDALGO,
            "jal": cls.JALISCO,
            "edomex": cls.MEXICO,
            "mich": cls.MICHOACAN_DE_OCAMPO,
            "mor": cls.MORELOS,
            "nay": cls.NAYARIT,
            "nl": cls.NUEVO_LEON,
            "oax": cls.OAXACA,
            "pue": cls.PUEBLA,
            "qro": cls.QUERETARO,
            "qroo": cls.QUINTANA_ROO,
            "slp": cls.SAN_LUIS_POTOSI,
            "sin": cls.SINALOA,
            "son": cls.SONORA,
            "tab": cls.TABASCO,
            "tamps": cls.TAMAULIPAS,
            "tlax": cls.TLAXCALA,
            "ver": cls.VERACRUZ_DE_IGNACIO_DE_LA_LLAVE,
            "yuc": cls.YUCATAN,
            "zac": cls.ZACATECAS,
        }.get(abbr)


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


class AlertTypeChoices(models.TextChoices):
    ALBA = ("AL", _("Alba"))
    AMBER = ("AM", _("Amber"))
    ODISEA = ("OD", _("Odisea"))
    OTHER = ("OT", _("Other"))
