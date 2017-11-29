import json
from itertools import groupby
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



vals2 = "{\"active\":[{\"moves\":[{\"move\":\"Volt Switch\",\"id\":\"voltswitch\",\"pp\":32,\"maxpp\":32,\"target\":\"normal\",\"disabled\":false},{\"move\":\"Heal Bell\",\"id\":\"healbell\",\"pp\":8,\"maxpp\":8,\"target\":\"allyTeam\",\"disabled\":false},{\"move\":\"Scald\",\"id\":\"scald\",\"pp\":24,\"maxpp\":24,\"target\":\"normal\",\"disabled\":false},{\"move\":\"Ice Beam\",\"id\":\"icebeam\",\"pp\":16,\"maxpp\":16,\"target\":\"normal\",\"disabled\":false}]}],\"side\":{\"name\":\"therobotcarlson2\",\"id\":\"p1\",\"pokemon\":[{\"ident\":\"p1: Lanturn\",\"details\":\"Lanturn, L83, F\",\"condition\":\"343/343\",\"active\":true,\"stats\":{\"atk\":101,\"def\":144,\"spa\":174,\"spd\":174,\"spe\":159},\"moves\":[\"voltswitch\",\"healbell\",\"scald\",\"icebeam\"],\"baseAbility\":\"voltabsorb\",\"item\":\"lifeorb\",\"pokeball\":\"pokeball\",\"ability\":\"voltabsorb\"},{\"ident\":\"p1: Lycanroc\",\"details\":\"Lycanroc-Midnight, L83, F\",\"condition\":\"277/277\",\"active\":false,\"stats\":{\"atk\":239,\"def\":172,\"spa\":139,\"spd\":172,\"spe\":184},\"moves\":[\"stealthrock\",\"suckerpunch\",\"firefang\",\"stoneedge\"],\"baseAbility\":\"noguard\",\"item\":\"lifeorb\",\"pokeball\":\"pokeball\",\"ability\":\"noguard\"},{\"ident\":\"p1: Milotic\",\"details\":\"Milotic, L79, F\",\"condition\":\"280/280\",\"active\":false,\"stats\":{\"atk\":140,\"def\":170,\"spa\":204,\"spd\":243,\"spe\":174},\"moves\":[\"sleeptalk\",\"rest\",\"dragontail\",\"scald\"],\"baseAbility\":\"marvelscale\",\"item\":\"leftovers\",\"pokeball\":\"pokeball\",\"ability\":\"marvelscale\"},{\"ident\":\"p1: Arcanine\",\"details\":\"Arcanine, L77, M\",\"condition\":\"265/265\",\"active\":false,\"stats\":{\"atk\":214,\"def\":168,\"spa\":199,\"spd\":168,\"spe\":191},\"moves\":[\"roar\",\"flareblitz\",\"crunch\",\"willowisp\"],\"baseAbility\":\"flashfire\",\"item\":\"leftovers\",\"pokeball\":\"pokeball\",\"ability\":\"flashfire\"},{\"ident\":\"p1: Rotom\",\"details\":\"Rotom-Heat, L79\",\"condition\":\"209/209\",\"active\":false,\"stats\":{\"atk\":107,\"def\":215,\"spa\":211,\"spd\":215,\"spe\":181},\"moves\":[\"voltswitch\",\"willowisp\",\"thunderbolt\",\"overheat\"],\"baseAbility\":\"levitate\",\"item\":\"lifeorb\",\"pokeball\":\"pokeball\",\"ability\":\"levitate\"},{\"ident\":\"p1: Latios\",\"details\":\"Latios, L75, M\",\"condition\":\"244/244\",\"active\":false,\"stats\":{\"atk\":140,\"def\":164,\"spa\":239,\"spd\":209,\"spe\":209},\"moves\":[\"dracometeor\",\"psyshock\",\"calmmind\",\"roost\"],\"baseAbility\":\"levitate\",\"item\":\"latiosite\",\"pokeball\":\"pokeball\",\"ability\":\"levitate\"}]},\"rqid\":2}"
vals = "{\"active\":[{\"moves\":[{\"move\":\"Dark Pulse\",\"id\":\"darkpulse\",\"pp\":21,\"maxpp\":24,\"target\":\"any\",\"disabled\":false},{\"move\":\"Hidden Power Fighting\",\"id\":\"hiddenpower\",\"pp\":21,\"maxpp\":24,\"target\":\"normal\",\"disabled\":false},{\"move\":\"Power Gem\",\"id\":\"powergem\",\"pp\":30,\"maxpp\":32,\"target\":\"normal\",\"disabled\":false},{\"move\":\"Nasty Plot\",\"id\":\"nastyplot\",\"pp\":32,\"maxpp\":32,\"target\":\"self\",\"disabled\":false}]}],\"side\":{\"name\":\"therobotcarlson2\",\"id\":\"p1\",\"pokemon\":[{\"ident\":\"p1: Persian\",\"details\":\"Persian-Alola, L83, M\",\"condition\":\"31/244 tox\",\"active\":true,\"stats\":{\"atk\":104,\"def\":147,\"spa\":172,\"spd\":156,\"spe\":239},\"moves\":[\"darkpulse\",\"hiddenpowerfighting60\",\"powergem\",\"nastyplot\"],\"baseAbility\":\"technician\",\"item\":\"lifeorb\",\"pokeball\":\"pokeball\",\"ability\":\"technician\"},{\"ident\":\"p1: Nihilego\",\"details\":\"Nihilego, L77\",\"condition\":\"0 fnt\",\"active\":false,\"stats\":{\"atk\":86,\"def\":117,\"spa\":240,\"spd\":246,\"spe\":203},\"moves\":[\"toxicspikes\",\"sludgewave\",\"powergem\",\"acidspray\"],\"baseAbility\":\"beastboost\",\"item\":\"\",\"pokeball\":\"pokeball\",\"ability\":\"beastboost\"},{\"ident\":\"p1: Yanmega\",\"details\":\"Yanmega, L80, F\",\"condition\":\"0 fnt\",\"active\":false,\"stats\":{\"atk\":168,\"def\":184,\"spa\":232,\"spd\":136,\"spe\":198},\"moves\":[\"gigadrain\",\"uturn\",\"ancientpower\",\"airslash\"],\"baseAbility\":\"speedboost\",\"item\":\"lifeorb\",\"pokeball\":\"pokeball\",\"ability\":\"speedboost\"},{\"ident\":\"p1: Kyurem\",\"details\":\"Kyurem-White, L73\",\"condition\":\"0 fnt\",\"active\":false,\"stats\":{\"atk\":180,\"def\":174,\"spa\":291,\"spd\":188,\"spe\":181},\"moves\":[\"roost\",\"focusblast\",\"dracometeor\",\"icebeam\"],\"baseAbility\":\"turboblaze\",\"item\":\"leftovers\",\"pokeball\":\"pokeball\",\"ability\":\"turboblaze\"},{\"ident\":\"p1: Decidueye\",\"details\":\"Decidueye, L79, F\",\"condition\":\"0 fnt\",\"active\":false,\"stats\":{\"atk\":215,\"def\":164,\"spa\":204,\"spd\":204,\"spe\":156},\"moves\":[\"roost\",\"leafblade\",\"suckerpunch\",\"spiritshackle\"],\"baseAbility\":\"longreach\",\"item\":\"lifeorb\",\"pokeball\":\"pokeball\",\"ability\":\"longreach\"},{\"ident\":\"p1: Blissey\",\"details\":\"Blissey, L77, F\",\"condition\":\"0 fnt\",\"active\":false,\"stats\":{\"atk\":20,\"def\":60,\"spa\":160,\"spd\":252,\"spe\":129},\"moves\":[\"protect\",\"stealthrock\",\"toxic\",\"seismictoss\"],\"baseAbility\":\"naturalcure\",\"item\":\"leftovers\",\"pokeball\":\"pokeball\",\"ability\":\"naturalcure\"}]},\"rqid\":74}"

active_dict = json.loads(vals)

print("----------active moves------------")
for item in active_dict['active'][0]['moves']:
    temp = moves_dict[item['id']]
    temp.pop('desc')
    temp.pop('shortDesc')
    temp.pop('contestType')
    print(temp, '\n')

print("-----------p1 stats-----------")
for item in active_dict['side']['pokemon']:
    stats = item["stats"]
    print(item['ident'][4:])
    print("active:", item["active"])
    print("types:", get_pokemon(item['ident'][4:].lower())['types'])
    print("item:", item["item"], ", baseAbility:", item["baseAbility"], ", ability", item["ability"])
    print("stats:", stats)
    print(item['moves'], ", hp:", item['condition'], "\n")
    
print("------------ move -------------")

# print(active_dict['side'], '\n')

move_stuffs = [
"move hiddenpower|\n|\n|switch|p2a: Dodrio|Dodrio, L81, F|100/100\n|-damage|p2a: Dodrio|76/100|[from] Stealth Rock\n|move|p1a: Persian|Hidden Power|p2a: Dodrio\n|-damage|p2a: Dodrio|37/100\n|-damage|p1a: Persian|196/244|[from] item: Life Orb\n|\n|upkeep\n|turn|21",
"move darkpulse|\n|\n|move|p1a: Persian|Dark Pulse|p2a: Dodrio\n|-damage|p2a: Dodrio|0 fnt\n|-damage|p1a: Persian|172/244|[from] item: Life Orb\n|faint|p2a: Dodrio\n|\n|upkeep",
"",
""
]

move_stuff2 = "move powergem|\n|\n|move|p1a: Persian|Power Gem|p2a: Hypno\n|-damage|p2a: Hypno|64/100\n|-damage|p1a: Persian|100/244|[from] item: Life Orb\n|move|p2a: Hypno|Toxic|p1a: Persian\n|-status|p1a: Persian|tox\n|\n|-heal|p2a: Hypno|70/100|[from] item: Leftovers\n|-damage|p1a: Persian|85/244 tox|[from] psn\n|upkeep\n|turn|26"
move_stuff = "move hiddenpower|\n|\n|move|p2a: Hypno|Protect|p2a: Hypno\n|-singleturn|p2a: Hypno|Protect\n|move|p1a: Persian|Hidden Power|p2a: Hypno\n|-activate|p2a: Hypno|move: Protect\n|\n|-heal|p2a: Hypno|82/100|[from] item: Leftovers\n|upkeep\n|turn|25"
move_list = [x for x in move_stuff.replace('\n', '').split('|') if x != '']

print(move_list, '\n')

print([x for x in move_stuff2.replace('\n', '').split('|') if x != ''])


grouped_list = [list(group) for k, group in groupby(move_list, lambda x: x == "move") if not k]

# print(grouped_list)
# print(grouped_list[1][0][5:], "used", grouped_list[1][1], "on", grouped_list[1][2][5:])
# print("Totals: ")
# print(grouped_list[1][4][5:], grouped_list[1][5])
# print(grouped_list[1][7][5:], grouped_list[1][8])
# print("\n")
# print(grouped_list[2][0][5:], "used", grouped_list[2][1], "on", grouped_list[2][2][5:])
# print("Totals: ")
# print(grouped_list[2][7][5:], grouped_list[2][8])
# print(grouped_list[2][11][5:], grouped_list[2][12])

