from functools import reduce
from pprint import pprint
from random import randint, uniform


def cross_list(left, right, mask):
    result = []
    for l in left:
        for r in right:
            result.append(mask.format(l=l, r=r))
    return result

class Ambiente:

    CARTAS_ESPANHOLAS = cross_list(
        ['o', 'c', 'e', 'p'],
        ['a', '2', '3', '4', '5', '6', '7', 's', 'c', 'r'], 
        "{r}{l}"
    )

    def __init__(self, tipo) -> None:
        self.tipo = tipo

        self.__attrib = {
            'brisca_mao_mesa': {
                'information_units': self.CARTAS_ESPANHOLAS + [''],
                'information_vector_dimensions': {
                    'mao_posicao_1': 40,
                    'mao_posicao_2': 41,
                    'mao_posicao_3': 41,
                    'mesa': 41,
                },
                'action_space': range(3),
                'action_space_sample': self.action_space_sample_randint02,
            }
        }

        self.atributos_tipo()

    def atributos_tipo(self):
        attrib = self.__attrib[self.tipo]

        self.information_units = attrib['information_units']
        self.information_vector_dimensions = attrib['information_vector_dimensions']
        self.action_space = attrib['action_space']
        self.action_space_sample = attrib['action_space_sample']

        self.information_vector_dims = list(self.information_vector_dimensions.values())
        self.observation_space_size = reduce(
            lambda x, ac: x * ac,
            self.information_vector_dims
        )

    def reset(self):
        return randint(0, self.observation_space_size-1)

    def step(self, action):
        # if 
        return randint(0, self.observation_space_size-1)

    # action space samples

    def action_space_sample_randint02(self):
        """Não precisa pegar o valor na list action_space, pois são inteiros de 0 a 2"""
        return randint(0, 2)

    def idx_vector2state(self, vector):
        """
        Multiplica cada valor pelo produto das dimensões anteriores
        Ex.:
        dimensões 2, 3 e 4
        tamanho do espaço: 2 * 3 * 4 = 24 = [0..23]
        vetor máximo de valores: (1, 2, 3)
        estado = 1 + 2*(2) + 3*(2*3) = 1 + 4 + 18 = 23
        vetor mínimo de valores: (0, 0, 0)
        estado = 0 + 0*(2) + 0*(2*3) = 0
        vetor exemplo: (0, 2, 1)
        estado = 0 + 2*(2) + 1*(2*3) = 0 + 4 + 6 = 10
        Converter:
            10 / (2*3) = 1 resto 4
            4 / (2) = 2 resto 0
            0 / 1 = 0
        """
        state = 0
        multiplic = 1
        for idx, value in enumerate(vector):
            if idx:
                multiplic *= self.information_vector_dims[idx-1]
                # print(idx, self.information_vector_dims[idx-1], multiplic)
            value *= multiplic
            state += value
        return state

    def state2idx_vector(self, state):
        multiplics = []
        multiplic = 1
        for idx, value in enumerate(self.information_vector_dims):
            if idx:
                multiplic *= self.information_vector_dims[idx-1]
                multiplics.append(multiplic)
        # pprint(multiplics)
        vector = []
        for divisor in multiplics[::-1]:
            # print(divisor)
            vector.append(state // divisor)
            state = state % divisor
        vector.append(state)
        return vector[::-1]

    def info_vector2idx_vector(self, info):
        return [
            self.information_units.index(i)
            for i in info
        ]

    def idx_vector2info_vector(self, idx):
        return [
            self.information_units[i]
            for i in idx
        ]

    def info_vector2state(self, info):
        return self.idx_vector2state(self.info_vector2idx_vector(info))

    def state2info_vector(self, state):
        return self.idx_vector2info_vector(self.state2idx_vector(state))


if __name__ == '__main__':
    amb = Ambiente('brisca_mao_mesa')
    info_vector = ['ao', 'ac', 'ae', '2e']
    print(info_vector)
    vector = amb.info_vector2idx_vector(info_vector)
    print(vector)
    info_vector = amb.idx_vector2info_vector(vector)
    print(info_vector)

    # print(
    #     'vai volta',
    #     amb.state2info_vector(
    #         amb.info_vector2state(info_vector)
    #     )
    # )



    vector = [2, 4, 6, 9]
    print(vector)
    state = amb.idx_vector2state(vector)
    print(state)
    vector = amb.state2idx_vector(state)
    print(vector)

    info = amb.idx_vector2info_vector(vector)
    print(info)
    state = amb.info_vector2state(info)
    print(state)
    info = amb.state2info_vector(state)
    print(info)
