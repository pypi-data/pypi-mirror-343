import random
import string
from typing import List

from ..Class.exceptions import RandomizerExceptions
from ..Class.seedSettings import ExtraConfigurationData
from .RandomizerSettings import RandomizerSettings
from .hints import Hints
from .multiworld import MultiWorld, MultiWorldConfig
from .newRandomize import Randomizer
from .seedEvaluation import LocationInformedSeedValidator
from .zipper import SeedZip, SeedZipResult


def generateSeed(
    settings: RandomizerSettings, extra_data: ExtraConfigurationData
) -> SeedZipResult:
    last_error = None
    for attempt in range(50):
        newSeedValidation = LocationInformedSeedValidator()
        try:
            randomizer = Randomizer(settings)
            location_spheres = newSeedValidation.validate_seed(settings, randomizer)
            # hints = Hints.generate_hints(randomizer, settings)
            hints = Hints.generate_hints_v2(randomizer, settings)
            zipper = SeedZip(settings, randomizer, hints, extra_data, location_spheres)
            return zipper.create_zip()
        except RandomizerExceptions as e:
            characters = string.ascii_letters + string.digits
            settings.random_seed = "".join(random.choice(characters) for i in range(30))
            settings.create_full_seed_string()
            last_error = e
            continue
    raise last_error


def generateSeedCLI(
    settings: RandomizerSettings, extra_data: ExtraConfigurationData
) -> str:
    last_error = None
    for attempt in range(50):
        newSeedValidation = LocationInformedSeedValidator()
        try:
            randomizer = Randomizer(settings)
            location_spheres = newSeedValidation.validate_seed(
                settings, randomizer, False
            )
            # hints = Hints.generate_hints(randomizer, settings)
            hints = Hints.generate_hints_v2(randomizer, settings)
            zipper = SeedZip(settings, randomizer, hints, extra_data, location_spheres)
            return zipper.make_spoiler_without_zip()
        except RandomizerExceptions as e:
            characters = string.ascii_letters + string.digits
            settings.random_seed = "".join(random.choice(characters) for i in range(30))
            settings.create_full_seed_string()
            last_error = e
            continue
    raise last_error


def generateMultiWorldSeed(
    settingsSet: List[RandomizerSettings], extra_data: ExtraConfigurationData
) -> list[SeedZipResult]:
    newSeedValidation = LocationInformedSeedValidator()
    randomizers = []
    unreachables = []
    last_error = None

    for player_settings in settingsSet:
        for attempt in range(50):
            try:
                last_error = None
                randomizer = Randomizer(player_settings)
                unreachable = newSeedValidation.validate_seed(
                    player_settings, randomizer
                )
                randomizers.append(randomizer)
                unreachables.append(unreachable)

                break
            except RandomizerExceptions as e:
                characters = string.ascii_letters + string.digits
                player_settings.random_seed = "".join(
                    random.choice(characters) for i in range(30)
                )
                player_settings.create_full_seed_string()
                last_error = e
                continue
        if last_error is not None:
            raise last_error

    # each individual randomization is done and valid, now we can mix the item pools
    m = MultiWorld(randomizers, MultiWorldConfig(settingsSet[0]))

    seed_outputs: list[SeedZipResult] = []
    for settings, randomizer, unreachable in zip(
        settingsSet, randomizers, unreachables
    ):
        hints = Hints.generate_hints_v2(randomizer, settings)
        zipper = SeedZip(
            settings, randomizer, hints, extra_data, unreachable, m.multi_output
        )
        seed_outputs.append(zipper.create_zip())

    return seed_outputs
