from pprint import pprint
from random import seed, randint

from baralla.grupo import Grupo
from baralla.partida import Partida
from baralla.tipo_jogo import TipoJogo


class Jogo:
    
    def __init__(self, tipo_jogo_id=None, grupo:Grupo=None) -> None:
        self.tipo_jogo_id = tipo_jogo_id
        self.grupo = grupo

        self.tipo_jogo = TipoJogo(self.tipo_jogo_id)
        self.tipo_jogo_id = self.tipo_jogo.id
        self.jogo_def = self.tipo_jogo.definicao

        self.vencedor = None

    def iniciar(self):
        self.grupo.inicia_tipo_jogo(self.tipo_jogo)
        self.grupo.sorteia()
        partidas_vencedor = self.jogo_def['jogo']['condição de término']['jogador ganha n partidas']

        while max(*self.grupo.placar().values()) < partidas_vencedor:
            partida = Partida(self.tipo_jogo, self.grupo)
            self.vencedor = partida.brinca()
            self.vencedor.partidas += 1
            placar = self.grupo.placar()
            print('placar', placar)

        placar_revertido = {v: k for k, v in placar.items()}
        print('vencedor do jogo', placar_revertido[partidas_vencedor])
