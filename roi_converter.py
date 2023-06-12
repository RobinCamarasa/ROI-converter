"""File that convert roi files into list of coordinates

Authors: Robin Camarasa, Ruysheng Su
"""
import json
import struct
import argparse
from typing import List
from pathlib import Path


def convert(byte_sequence: bytes, maximum: float = 1024, minimum: float = 1) -> float:
    """Convert a byte sequence into a float.

    :param byte_sequence: byte sequence to convert
    :param maximum: Upper bound of the reasonable range of float
    :param minimum: Lower bound of the reasonable range of float
    :return: None if the float is unrealistic or unparsable
    """
    try:
        float_conversion: float = struct.unpack("!f", byte_sequence)[0]
    except:
        return None
    if minimum <= float_conversion <= maximum:
        return float_conversion


def get_longest_sequence(complete_sequence: List[float]) -> List[float]:
    """Get the longest sequence of float from a complete sequence

    :param complete_sequence: Complete sequence from which the longest sequence of float is extracted
    :return: The longuest sequence of float
    """
    current_sequence, longest_sequence = [], []
    for item in complete_sequence:
        if item is not None:
            current_sequence.append(item)
            if len(current_sequence) > len(longest_sequence):
                longest_sequence = current_sequence
        else:
            current_sequence = []
    return longest_sequence


def main(user_input: argparse.Namespace):
    """Main function

    :param user_input: Input given by the user throught the CLI
    """
    with user_input.roi_file.open("rb") as file:
        byte_sequence = 1
        parsed_file = []
        # Parse file
        while byte_sequence:
            byte_sequence = file.read(4)
            parsed_file.append(convert(byte_sequence))

        # Get the most plausible sequence
        longest_sequence = get_longest_sequence(parsed_file)
        # Raise exception if this sequence does not have the right shape
        if len(longest_sequence) % 2 == 1:
            print(f"The parsing of {user_input.roi_file} did not work")

        with user_input.json_file.open("w") as fd:
            json.dump(
                {
                    "x": longest_sequence[: len(longest_sequence) // 2],
                    "y": longest_sequence[len(longest_sequence) // 2 :],
                },
                fd,
                indent=4,
            )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-r", "--roi-file", type=Path, help="Path to the roi file")
    parser.add_argument(
        "-j", "--json-file", type=Path, help="Output json file with coordinates"
    )
    main(parser.parse_args())
