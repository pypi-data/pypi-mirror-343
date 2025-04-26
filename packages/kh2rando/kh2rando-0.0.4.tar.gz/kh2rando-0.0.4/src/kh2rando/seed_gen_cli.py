import argparse
from seed_gen import generator

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
requested_preset = args.preset


if __name__ == "__main__":
    seed_info = generator.make_random_seed_from_preset_name(requested_preset)
    print(seed_info.generator_string)
    print(seed_info.hash_icons)
