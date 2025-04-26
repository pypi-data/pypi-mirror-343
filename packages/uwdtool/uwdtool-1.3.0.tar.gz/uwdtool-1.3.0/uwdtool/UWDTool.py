import argparse

from .Common import print_err, HELP_STR
from .Unpacker import Unpacker
from .Packer import Packer
from .Inspector import Inspector


def main():
    Main().main()


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog = "uwdtool",
            description = HELP_STR,
            formatter_class = argparse.RawTextHelpFormatter
        )
        g = self.parser.add_mutually_exclusive_group()

        g.add_argument("-p", "--pack", action="store_true", help="packing files in input-path directory")
        g.add_argument("-u", "--unpack", action="store_true", help="unpacking input-path file to output-path directory")
        g.add_argument("-isp", "--inspect", action="store_true", help="show file information list of input-path file")

        self.parser.add_argument("-i", dest="ARG_INPUT", help="input path")
        self.parser.add_argument("-o", dest="ARG_OUTPUT", help="output path")
        self.parser.add_argument("-c", "--compression", choices=["brotli", "gzip", "none"], required=False, default="auto", help="Compression type to use when packing or unpacking")

    def main(self):
        args = self.parser.parse_args()

        if args.pack:
            Packer(args.ARG_INPUT, args.ARG_OUTPUT, args.compression).pack()
        elif args.unpack:
            Unpacker(args.ARG_INPUT, args.ARG_OUTPUT, args.compression).unpack()
        elif args.inspect:
            Inspector(args.ARG_INPUT, args.compression).inspect()
        else:
            print_err("Please select option.")


if __name__ == "__main__":
    Main().main()
