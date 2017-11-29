import json

file = open("pokedex.json")
pokedex = json.loads(file.read())

file = open("moves.json")
moves_dict = json.loads(file.read())

file = open("items.json")
items_dict = json.loads(file.read())

file = open("abilities.json")
abilities_dict = json.loads(file.read())

# def get_moves

def get_ability(ability):
    return abilities_dict[ability]


def get_pokemon(pokemon):
    """
    :param pokemon: pokemon name
    :return: pokemon_dict
    """

    pokemon_dict_temp = {
        'id': pokedex[pokemon]["num"],
        'base_stats': pokedex[pokemon]["baseStats"],
        'types': pokedex[pokemon]["types"],
        'abilities': [x.lower().replace(" ", "") for x in pokedex[pokemon]["abilities"].values()]
    }     # makes them searchable

    return pokemon_dict_temp


pokemon_dict = get_pokemon("bulbasaur")

print(get_pokemon("bulbasaur"))

# r = requests.get('https://api.github.com/user')


