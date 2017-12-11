# Pokemon stat calculator
# Calculates actual stats of a pokemon given level and base stats
# Uses max EVs for the two stats most likely to be invested, and 0 for others.
# Also guesses nature using standard competitive battle conventions
# Uses Showdown rating to select from possible abilities

import math

def initialize_mon(species, level):
    # If the pokedex is accessed some other way, fix that here
    global pokedex
    global abilities
    
    stat_sort = []
    base_stats = pokedex[species]['baseStats']
    for stat in base_stats:
        stat_sort.append((stat, base_stats[stat]))
    
    # Sort the base stats
    stat_sort.sort(key=lambda x: x[1], reverse = True)
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
            stats[stat] = 5 + math.floor((base_stats[stat]*2 + 94) * level / 100)
        else:
            stats[stat] = 5 + math.floor((base_stats[stat]*2 + 31) * level / 100)
            
    # HP is calculated slightly differently
    stats['hp'] += level + 5
    
    # Predict nature
    if stat_sort.index("atk") < stat_sort.index("spa"):
        stats['spa'] = math.floor(stats['spa']*.9)
    else:
        stats['atk'] = math.floor(stats['atk']*.9)
    
    if 'spe' in max_stats:
        stats['spe'] = math.floor(stats['spe']*1.1)
    else:
        stats[stat_sort[0]] = math.floor(stats[stat_sort[0]]*1.1)
    
    # Decide the most likely ability using the ratings from the ability dict
    poss_abil = [pokedex[species]["abilities"][i] for i in pokedex[species]["abilities"]]
    poss_abil.sort(key=lambda x: abilities[x]['rating'], reverse = True)
    
    # After sorting, the ability with the highest rating is chosen (arbitrary in case of ties)
    ability = poss_abil[0]
    
    return (stats, ability)