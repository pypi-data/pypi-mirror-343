import json
import os
import random
import string
import argparse

from collections import namedtuple

from Class.seedSettings import ExtraConfigurationData, SeedSettings
from Module import appconfig
from Module.RandomizerSettings import RandomizerSettings
from Module.generate import generateSeedCLI
from Module.seedshare import SharedSeed
from Module.version import LOCAL_UI_VERSION

# CLI arguments & docs
parser = argparse.ArgumentParser(
    description="A command line utility for generating KH2 Randomizer seed strings from a given preset"
)
parser.add_argument(
    "preset",
    help='preset from which to generate seed string (default: "League Summer 2025")',
    nargs="?",
    default="League Summer 2025",
)
args = parser.parse_args()

SeedInfo = namedtuple(
    "SeedInfo",
    ["seed_name", "requested_preset", "generator_string", "hash_icons", "spoiler_html"],
)

requested_preset = args.preset


def make_random_seed_from_preset_name(requested_type: str):
    # TODO: Search for the specific preset file instead of loading all of them
    # load preset data for all presets in folder
    preset_json = {}
    for preset_file_name in os.listdir(appconfig.PRESET_FOLDER):
        preset_name, extension = os.path.splitext(preset_file_name)
        if extension == ".json":
            with open(
                os.path.join(appconfig.PRESET_FOLDER, preset_file_name), "r"
            ) as presetData:
                try:
                    settings_json = json.load(presetData)
                    preset_json[preset_name] = settings_json
                except Exception:
                    print(
                        "Unable to load preset [{}], skipping".format(preset_file_name)
                    )

    # get seed name at random
    characters = string.ascii_letters + string.digits
    seedString = "".join(random.choice(characters) for i in range(30))
    makeSpoilerLog = False
    settings = SeedSettings()
    try:
        settings.apply_settings_json(preset_json[requested_type])
    except KeyError:
        print(
            '\033[31mNo preset file found with the name \033[1m"{}"\033[0m'.format(
                requested_type
            )
        )
        exit(128)

    shared_seed = SharedSeed(
        generator_version=LOCAL_UI_VERSION,
        seed_name=seedString,
        spoiler_log=makeSpoilerLog,
        settings_string=settings.settings_string(),
        tourney_gen=True,
    )
    shared_string_text = shared_seed.to_share_string()

    rando_settings = RandomizerSettings(
        seedString, makeSpoilerLog, LOCAL_UI_VERSION, settings, shared_string_text
    )

    extra_data = ExtraConfigurationData(
        platform="PC", tourney=True, custom_cosmetics_executables=[]
    )

    spoiler_log = generateSeedCLI(rando_settings, extra_data)

    return SeedInfo(
        seed_name=seedString,
        requested_preset=requested_type,
        generator_string=shared_string_text,
        hash_icons=rando_settings.seedHashIcons,
        spoiler_html=spoiler_log,
    )


if __name__ == "__main__":
    seed_info = make_random_seed_from_preset_name(requested_preset)
    print(seed_info.generator_string)
    print(seed_info.hash_icons)
