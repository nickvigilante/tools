import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", required=True, dest="str")
args = parser.parse_args()

npa = {
    "a": "ALPHA",
	"b": "BRAVO",
	"c": "CHARLIE",
	"d": "DELTA",
	"e": "ECHO",
	"f": "FOXTROT",
	"g": "GOLF",
	"h": "HOTEL",
	"i": "INDIA",
	"j": "JULIET",
	"k": "KILO",
	"l": "LIMA",
	"m": "MIKE",
	"n": "NOVEMBER",
	"o": "OSCAR",
	"p": "PAPA",
	"q": "QUEBEC",
	"r": "ROMEO",
	"s": "SIERRA",
	"t": "TANGO",
	"u": "UNIFORM",
	"v": "VICTOR",
	"w": "WHISKEY",
	"x": "X-RAY",
	"y": "YANKEE",
	"z": "ZULU",
}

for s in args.str:
    # print(s)
    row = "CAPITAL " if s.isupper() and s.lower() in npa.keys() else ""
    row += npa[s.lower()] if s.lower() in npa.keys() else s
    print(row)
