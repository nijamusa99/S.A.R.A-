from enum import Enum

class Genero(str, Enum):
    COMEDIA = "Comedia"
    DRAMA = "Drama"
    MUSICAL = "Musical"
    INFANTIL = "Infantil"
    STAND_UP = "Stand-up"
    CLASICO = "Clasico"

class DiaSemana(int, Enum):
    LUNES = 0
    MARTES = 1
    MIERCOLES = 2
    JUEVES = 3
    VIERNES = 4
    SABADO = 5
    DOMINGO = 6