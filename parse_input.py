from io import open
import json
import re
import ast
import math

file = open("pokedex.json")
pokedex = json.loads(file.read())

file = open("moves.json")
moves_dict = json.loads(file.read())

file = open("items.json")
items_dict = json.loads(file.read())

file = open("abilities.json")
abilities_dict = json.loads(file.read())

types_set = set()

for pokemans in pokedex.values():
    for poke_type in pokemans['types']:
        types_set.add(poke_type)


max_stat_val = 714
stats_list = ['atk', 'def', 'spa', 'spd', 'spe', 'hp']
types_list = list(types_set)
abilities_list = list(abilities_dict.keys())
moves_list = list(moves_dict.keys())
items_list = list(items_dict.keys())
conditions_list = ['burn', 'poison', 'paralysis', 'sleep', 'freeze', 'confusion', 'taunt', 'cantswitch', 'fnt']
weather_list = ["sun", "rain", "hail", "sand", "other"]
weather_corrections = {"harsh sun": "sun", "torrential rain": "rain"}

terrain_list = ["electric", "psychic", "grassy", "misty"]
# Burn, Poison, Paralysis, Sleep, Freeze
# volatile status:
# confusion: bool
# taunt: bool
# can't switch: bool


# Pokemon stat calculator
# Calculates actual stats of a pokemon given level and base stats
# Uses max EVs for the two stats most likely to be invested, and 0 for others.
# Also guesses nature using standard competitive battle conventions
# Uses Showdown rating to select from possible abilities

def initialize_mon(species, level):
    stat_sort = []
    base_stats = pokedex[species]['baseStats']
    for stat in base_stats:
        stat_sort.append((stat, base_stats[stat]))

    # Sort the base stats
    stat_sort.sort(key=lambda x: x[1], reverse=True)
    for i in range(len(stat_sort)): stat_sort[i] = stat_sort[i][0]

    # Decide which stats are probably maxed
    max_stats = []
    if "spe" in stat_sort[:2]:
        max_stats.append("spe")
    elif "spe" in stat_sort[4:] or stat_sort[0] in ["def", "spd"] or stat_sort.index("hp") < stat_sort.index("spe"):
        max_stats.append("hp")
        stat_sort.remove("hp")
    else:
        max_stats.append("spe")

    if max_stats[0] == "spe":
        if stat_sort.index("atk") < stat_sort.index("spa"):
            max_stats.append("atk")
        else:
            max_stats.append("spa")
    else:
        max_stats.append(stat_sort[0])

    if 'hp' in stat_sort:
        stat_sort.remove('hp')

    stats = {}

    # calculate stat values
    for stat in base_stats:
        if stat in max_stats:
            stats[stat] = 5 + math.floor((base_stats[stat] * 2 + 94) * level / 100)
        else:
            stats[stat] = 5 + math.floor((base_stats[stat] * 2 + 31) * level / 100)

    # HP is calculated slightly differently
    stats['hp'] += level + 5

    # Predict nature
    if stat_sort.index("atk") < stat_sort.index("spa"):
        stats['spa'] = math.floor(stats['spa'] * .9)
    else:
        stats['atk'] = math.floor(stats['atk'] * .9)

    if 'spe' in max_stats:
        stats['spe'] = math.floor(stats['spe'] * 1.1)
    else:
        stats[stat_sort[0]] = math.floor(stats[stat_sort[0]] * 1.1)

    # Decide the most likely ability using the ratings from the ability dict
    poss_abil = [pokedex[species]["abilities"][i].lower().replace(" ", "") for i in pokedex[species]["abilities"]]
    poss_abil.sort(key=lambda x: abilities_dict[x]['rating'], reverse=True)

    # After sorting, the ability with the highest rating is chosen (arbitrary in case of ties)
    ability = poss_abil[0]

    return stats, ability


def normalize(val, min_val=0, max_val=100):
    return (val - min_val) / max_val


def one_hot(items, base_list):
    encoded_features = [0] * len(base_list)

    for item in items:
        loc = find(base_list, item)
        if loc != -1:
            encoded_features[loc] = 1.0

    return encoded_features


def get_pokemon_vector(details, condition, stats, moves, items, ability):

    pokemon_level = normalize(int(details.split(',')[1][2:]))

    condition_list_temp = condition.split(' ')
    hitpoint_percent_temp = condition_list_temp[0].split("/")
    if len(hitpoint_percent_temp) == 1:  # in the case of fnt
        hitpoint_percent = 0
    else:
        hitpoint_percent = int(hitpoint_percent_temp[0]) * 1.0 / int(hitpoint_percent_temp[1])
        stats['hp'] = hitpoint_percent_temp[1]

    if len(condition_list_temp) == 1:  # no conditions
        condition_list = [0] * len(conditions_list)
    else:
        condition_list = one_hot(condition_list_temp[1:], conditions_list)

    stat_list = [normalize(int(stats[x]), max_val=max_stat_val) for x in stats_list]
    move_list = one_hot(moves, moves_list)
    pokemon_item = one_hot(items, items_list)
    ability = one_hot([ability], abilities_list)

    pokemon_features = [hitpoint_percent]
    pokemon_features += condition_list
    pokemon_features += stat_list
    pokemon_features += move_list
    pokemon_features += pokemon_item
    pokemon_features += ability
    pokemon_features.append(pokemon_level)

    # print(pokemon_name, hitpoint_percent, condition_list, stat_list, move_list, pokemon_item, ability, pokemon_level)

    return pokemon_features


def get_pokemon(p):
    """
    :param p: pokemon name
    :return: pokemon_dict
    """

    pokemon_dict_temp = {
        'id': pokedex[p]["num"],
        'base_stats': pokedex[p]["baseStats"],
        'types': pokedex[p]["types"],
        'abilities': [x.lower().replace(" ", "") for x in pokedex[p]["abilities"].values()]
    }     # makes them searchable

    return pokemon_dict_temp


def parse_json(s):
    s = re.sub(r'null', '"null"', s)
    return json.loads(re.sub(r'\\', '', s))  # ast.literal_eval(

# lines = tuple(open("console-feed-list.txt", 'r', encoding='utf8'))
lines = tuple(open("temp_console_2.txt", 'r', encoding='utf8'))


def find(l, p):
    return next((i for i, x in enumerate(l) if x == p), -1)


def inside(l, p):
    # print([True if p in x else False for x in l])
    return any([True if p in x else False for x in l])

my_name = "therobotcarlson2"
my_identity = ""

feature_vector = []
# weather: id ( or None)
# terrain: id ( or None)
# trick room: bool
field = []

# stealth rock: bool
# sticky web: bool
# spikes: number of layers
# toxic spikes: number of layers
hazards_side_p1 = []
hazards_side_p2 = []

# reflect: bool
# light screen: bool  (# aurora veil = reflect + lightscreen)
# safeguard: bool
defenses_side_p1 = []
defenses_side_p2 = []

# types: id  # one hot encoding
# ability: id
# item: id
# move set: set<ids>
# level: int
# hp%: float
# major status: id
# Burn, Poison, Paralysis, Sleep, Freeze
# volatile status:
# confusion: bool
# taunt: bool
# can't switch: bool
# stat changes: list<int>

pokemon_data_p1 = []
pokemon_data_p2 = []

pokemon_dict_p2 = {}

for line in lines:
    line = line[:-1]
    # print(line)
    line = ast.literal_eval(line)['message']

    loc = line.find("{")

    if loc != -1:
        re.sub(r'\\', '', re.sub(r'null', '"null"', line[loc:-1]))
        line = parse_json(line[loc:-1])

        if 'searching' in line:
            # print(line)
            continue  # do nothing
        elif 'wait' in line:
            continue  # also do nothing
        elif 'active' in line:  # ['active']
            if line['side']['name'] == my_name:
                # print("updating %s's pokemon" % my_identity)

                for pokemon in line['side']['pokemon']:
                    # print(pokemon['ident'][4:].lower().replace(' ', ''))
                    pokemon_base = get_pokemon(pokemon["ident"][4:].lower().replace(' ', ''))
                    # print(pokemon_base['id'], pokemon_base['types'], pokemon_base['abilities'])
                    # print(pokemon['active'], pokemon['condition'].split("/"), pokemon['moves'])
                    if pokemon['active']:
                        pokemon_data_p1 = get_pokemon_vector(pokemon['details'],
                                                             pokemon['condition'],
                                                             pokemon['stats'],
                                                             pokemon['moves'],
                                                             [pokemon['item']],
                                                             pokemon['ability'])
                        # print(pokemon['ident'][4:].lower())
        elif 'forceSwitch' in line:
            # print("forceSwitch:", line['forceSwitch'][0])
            continue
    else:
        line_data = line.replace("\\n", "").split('"')
        if len(line_data) == 1:
            continue
        else:
            line_data = line_data[1].split("|")[1:]
        line_data = [x for x in line_data if x != '']

        if inside(line_data, "player"):
            if 'start' in line_data:
                switch_index = line_data.index('switch')
                pokemon_name = line_data[switch_index + 1][5:].lower()
                pokemon_level = int(line_data[switch_index + 2].split(',')[1][2:])
                stats, ability = initialize_mon(pokemon_name, pokemon_level)

                pokemon_data_p2 = get_pokemon_vector(line_data[switch_index + 2],
                                                     line_data[switch_index + 3],
                                                     stats,
                                                     [],
                                                     [],
                                                     ability)
                print(line_data[switch_index + 1][5:].lower())
                pokemon_dict_p2[pokemon_name] = {
                    'moves': [],
                    'abilities': [ability],
                    'stats': stats,
                }

            continue
        elif inside(line_data, "choice"):
            if inside(line_data, "switch"):
                # print(line_data)
                continue
            elif inside(line_data, "move"):
                # print(line_data)
                continue
            else:
                # print(line_data)
                continue
        elif inside(line_data, "init"):  # done
            my_identity = "p1" if line_data[-3] == my_name else "p2"
            # print("my id:", my_identity)
            continue
        elif inside(line_data, "inactive"):
            # print(line_data)
            continue
        elif inside(line_data, "/search"):
            # print(line_data)
            continue
        elif inside(line_data, "/choose"):
            # print(line_data)
            continue
        elif inside(line_data, "raw"):  # done
            elo_change_str = re.search(r'[\-\+](\d+)', line_data[-1]).group(0)

            if "+" in elo_change_str:
                elo_change = int(elo_change_str[1:])
            else:
                elo_change = int(elo_change_str)

            # print(elo_change, "need to start a new game")
            break
        else:
            # print(line_data)
            continue

