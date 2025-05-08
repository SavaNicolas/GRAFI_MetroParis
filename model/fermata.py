from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Fermata:
    id_fermata: int
    nome: str
    coordX: Decimal
    coordY: Decimal


    def __hash__(self):
        return self.id_fermata

    def __str__(self):
        return f"{self.nome}"

    def __eq__(self, other):
        return self.id_fermata == other.id_fermata
