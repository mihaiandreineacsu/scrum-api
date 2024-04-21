from FantasyNameGenerator import (
    DnD, Stores, Pathfinder, Items
)
import random

OPTIONS = [
    Stores.Antique, Stores.Clothes, Stores.Enchanter, Stores.Alchemist,
    Stores.Restaurant, Stores.Jeweller, Stores.Blacksmith, Stores.General,
    Stores.Town, Stores.Brothel, Stores.Gunsmith, Stores.Guild,
    Items.Relic, Items.Weapon,
    DnD.Aarakocra, DnD.Aasimer, DnD.Bugbear, DnD.Centaur,
    DnD.Changeling, DnD.Dragonborn, DnD.Drow, DnD.Duergar,
    DnD.Dwarf, DnD.Elf, DnD.Fetchling, DnD.Firbolg,
    DnD.Genasi, DnD.Gith, DnD.Gnome, DnD.Goblin,
    DnD.Goliath, DnD.Halfling, DnD.Hobgoblin, DnD.Human,
    DnD.Kalashtar, DnD.Kenku, DnD.Kobold, DnD.Lizardfolk,
    DnD.Loxodon, DnD.Minotaur, DnD.Orc, DnD.Shifter,
    DnD.Svirfneblin, DnD.Tabaxi, DnD.Tiefling, DnD.Tortle,
    DnD.Triton, DnD.Vedalken, DnD.Warforged,
    Pathfinder.Anadi, Pathfinder.Android, Pathfinder.Automaton, Pathfinder.Azarketi,
    Pathfinder.Catfolk, Pathfinder.Character, Pathfinder.Conrasu, Pathfinder.Dhampir,
    Pathfinder.Dwarf, Pathfinder.Elf, Pathfinder.Fetchling,
    Pathfinder.Fleshwarp, Pathfinder.Gillman, Pathfinder.Goblin, Pathfinder.Grippli,
    Pathfinder.Halfling, Pathfinder.Vishkanya, Pathfinder.Ghoran, Pathfinder.Gnoll,
    Pathfinder.Gnome, Pathfinder.Goloma, Pathfinder.Hobgoblin, Pathfinder.Human,
    Pathfinder.Ifrit, Pathfinder.Kashrishi, Pathfinder.Kitsune, Pathfinder.Kobold,
    Pathfinder.Leshy, Pathfinder.Lizardfolk, Pathfinder.Merfolk, Pathfinder.Nagaji,
    Pathfinder.Orc, Pathfinder.Oread, Pathfinder.Poppet, Pathfinder.Ratfolk,
    Pathfinder.Shisk, Pathfinder.Shoony, Pathfinder.Skeleton, Pathfinder.Sprite,
    Pathfinder.Strix, Pathfinder.Suli, Pathfinder.Sylph,
    Pathfinder.Tengu, Pathfinder.Tian, Pathfinder.Vanara, Pathfinder.Vishkanya,
]

def generate_name():
    option = random.choice(OPTIONS)
    return option.generate()