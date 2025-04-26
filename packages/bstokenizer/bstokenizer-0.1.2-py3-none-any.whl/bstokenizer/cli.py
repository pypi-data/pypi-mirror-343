"""
Command line interface for BeatSaber Tokenizer.
Provides tools for converting Beat Saber maps between different formats.
"""

import sys
import json
import os
import argparse
import logging
from .mapconvert import convert

def setup_logging(verbose: bool = False):
    """Configure logging based on verbosity"""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )

def convert_map():
    """
    Command line tool for converting Beat Saber maps between formats.
    
    Usage: 
        bsconvert <input_file> <output_file> [--v2|--v3|--v4] [--verbose]
    """
    parser = argparse.ArgumentParser(
        description="Convert Beat Saber maps between v2, v3, and v4 formats"
    )
    parser.add_argument("input_file", help="Path to input map file")
    parser.add_argument("output_file", help="Path to output map file")
    parser.add_argument(
        "--target", 
        choices=["v2", "v3", "v4", "2", "3", "4"], 
        help="Target map format version (defaults to auto-detect)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            map_data = json.load(f)
    except Exception as e:
        logging.error(f"Error reading input file: {e}")
        sys.exit(1)
    
    # Auto-detect target version if not specified
    target_version = args.target
    if target_version is None:
        if "_version" in map_data:
            target_version = "v3"  # Convert from v2 to v3
            logging.info("Auto-detected v2 format, converting to v3")
        elif map_data.get("version", "").startswith("4"):
            target_version = "v3"  # Convert from v4 to v3
            logging.info("Auto-detected v4 format, converting to v3")
        elif "version" in map_data:
            target_version = "v2"  # Convert from v3 to v2
            logging.info("Auto-detected v3 format, converting to v2")
        else:
            logging.error("Could not auto-detect map version. Please specify --target")
            sys.exit(1)
    
    try:
        output_data = convert(map_data, target_version)
        
        # Handle v4 output (tuple of beatmap and lightshow)
        if isinstance(output_data, tuple):
            beatmap, lightshow = output_data
            
            # Create output filenames
            output_base = os.path.splitext(args.output_file)[0]
            beatmap_file = f"{output_base}_Beatmap.dat"
            lightshow_file = f"{output_base}_Lightshow.dat"
            
            # Save beatmap
            with open(beatmap_file, 'w', encoding='utf-8') as f:
                json.dump(beatmap, f, indent=2)
                
            # Save lightshow
            with open(lightshow_file, 'w', encoding='utf-8') as f:
                json.dump(lightshow, f, indent=2)
                
            logging.info("Conversion completed:")
            print(f"- Beatmap: {beatmap_file}")
            print(f"- Lightshow: {lightshow_file}")
        else:
            # Standard single file output
            with open(args.output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
            logging.info(f"Conversion completed: {args.input_file} → {args.output_file}")
            print(f"Conversion completed: {args.input_file} → {args.output_file}")
    except Exception as e:
        logging.error(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    convert_map()