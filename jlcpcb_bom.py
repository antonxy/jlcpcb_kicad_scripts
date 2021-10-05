#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    BOM export matching JLCPCB format.
    Each component should have a field named LCSC containing the LCSC part nr.
    
    Command line:
    python "pathToFile/jlcpcb_bom.py" "%I" "%O.csv"
    
    Place in C:\Program Files\KiCad\bin\scripting\plugins\ and access in eeschema through Tools > Generate Bill of Materials > Add new plugin
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a set of rows for a header providing general information
out.writerow(['Comment', 'Designator', 'Footprint', 'JLCPCB Part #'])

# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()

# Output all of the component information
for group in grouped:
    refs = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        refs += component.getRef() + ","
        c = component

    # Fill in the component groups common data
    out.writerow([c.getValue(), refs, c.getFootprint(), c.getField("JLC")])


