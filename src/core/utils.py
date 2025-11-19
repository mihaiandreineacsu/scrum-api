import random
import re

from FantasyNameGenerator import DnD, Pathfinder
from FantasyNameGenerator.Base import Character

PATH_FINDERS = [
    Pathfinder.Anadi,
    Pathfinder.Android,
    Pathfinder.Automaton,
    Pathfinder.Azarketi,
    Pathfinder.Catfolk,
    Pathfinder.Conrasu,
    Pathfinder.Dhampir,
    Pathfinder.Dwarf,
    Pathfinder.Elf,
    Pathfinder.Fetchling,
    Pathfinder.Fleshwarp,
    Pathfinder.Gillman,
    Pathfinder.Goblin,
    Pathfinder.Grippli,
    Pathfinder.Halfling,
    Pathfinder.Vishkanya,
    Pathfinder.Ghoran,
    Pathfinder.Gnoll,
    Pathfinder.Gnome,
    Pathfinder.Goloma,
    Pathfinder.Hobgoblin,
    Pathfinder.Human,
    Pathfinder.Ifrit,
    Pathfinder.Kashrishi,
    Pathfinder.Kitsune,
    Pathfinder.Kobold,
    Pathfinder.Leshy,
    Pathfinder.Lizardfolk,
    Pathfinder.Merfolk,
    Pathfinder.Nagaji,
    Pathfinder.Orc,
    Pathfinder.Oread,
    Pathfinder.Poppet,
    Pathfinder.Ratfolk,
    Pathfinder.Shisk,
    Pathfinder.Shoony,
    Pathfinder.Skeleton,
    Pathfinder.Sprite,
    Pathfinder.Strix,
    Pathfinder.Suli,
    Pathfinder.Sylph,
    Pathfinder.Tengu,
    Pathfinder.Tian,
    Pathfinder.Vanara,
    Pathfinder.Vishkanya,
]
DNDS = [
    DnD.Aarakocra,
    DnD.Aasimer,
    DnD.Bugbear,
    DnD.Centaur,
    DnD.Changeling,
    DnD.Dragonborn,
    DnD.Drow,
    DnD.Duergar,
    DnD.Dwarf,
    DnD.Elf,
    DnD.Fetchling,
    DnD.Firbolg,
    DnD.Genasi,
    DnD.Gith,
    DnD.Gnome,
    DnD.Goblin,
    DnD.Goliath,
    DnD.Halfling,
    DnD.Hobgoblin,
    DnD.Human,
    DnD.Kalashtar,
    DnD.Kenku,
    DnD.Kobold,
    DnD.Lizardfolk,
    DnD.Loxodon,
    DnD.Minotaur,
    DnD.Orc,
    DnD.Shifter,
    DnD.Svirfneblin,
    DnD.Tabaxi,
    DnD.Tiefling,
    DnD.Tortle,
    DnD.Triton,
    DnD.Vedalken,
    DnD.Warforged,
]
OPTIONS: list[type[Character]] = [*PATH_FINDERS, *DNDS]

PRIORITY_CHOICES = [("Urgent", "Urgent"), ("Medium", "Medium"), ("Low", "Low")]


def generate_name() -> str:
    """Random pick a generated FantasyName"""
    option = random.choice(OPTIONS)
    return option.generate()


def normalize_spacing(value: str) -> str:
    """Normalize string by stripping and reducing spaces."""
    return re.sub(r"\s+", " ", value.strip())


def remove_spacing(value: str) -> str:
    """Normalize string by removing spaces."""
    return re.sub(r"\s+", "", value.strip())
