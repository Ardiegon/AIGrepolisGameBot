import argparse
import sys

from easydict import EasyDict

from grepobot.brain import Brain
from grepobot.utils.common import config_loader

def parse_args():
    parser = argparse.ArgumentParser(description="Grepobot CLI")
    parser.add_argument("--version", action="version", version="Grepobot 0.1.0")
    parser.add_argument("--config", type=str, help="Path to the configuration file", default="config.yaml")
    
    return parser.parse_args()

def main():
    args = parse_args()
    config = EasyDict(config_loader(args.config))
    bot = Brain(game_data=config)
    bot.run()

if __name__ == "__main__":
    main()