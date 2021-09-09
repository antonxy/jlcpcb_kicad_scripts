import os
import sys
import pcbnew
import csv
import kicad_netlist_reader
from decimal import Decimal
import wx


"""
pcbnew action plugin to export component placement list according to JLCPCB format.
SMT and Through-Hole will be contained in the file.

Run bom generation first so that the netlistfile {board}.xml is generated.
This script will read the field JlcRotOffset from the netlist file
to correct for different rotation in Kicad and JLC library.

Installation:

Windows 7/Windows 10:
Install the plugin together with kicad_netlist_reader.py in: %APPDATA%\kicad\scripting\plugins

GNU/Linux:
Install the plugin together with kicad_netlist_reader.py in: ~/.kicad/scripting/plugins or ~/.kicad_plugins

Access from pcbnew through Tools > External Plugins
"""

class jlcpcb_cpl(pcbnew.ActionPlugin):
    def defaults(self):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Export CPL in JLC Format"
        self.category = "Export"
        self.description = "Generate CPL for JLCPCB assembly"

    def Run(self):
        my_board = pcbnew.GetBoard()
        net = kicad_netlist_reader.netlist(os.path.splitext(my_board.GetFileName())[0] + ".xml")
        outname = os.path.join(os.path.dirname(my_board.GetFileName()), "jlc_cpl.csv")
        
        f = open(outname, 'w')
        out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
        out.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        
        grouped = net.groupComponents()

        for module in my_board.GetModules():
            if module.GetAttributes() != pcbnew.MOD_VIRTUAL:
                # Get rotation offset for this reference from netlist
                c = None
                offset = 0
                for group in grouped:
                    for component in group:
                        if module.GetReference() == component.getRef():
                            c = component
                            offstr = c.getField("JlcRotOffset")
                            if offstr != "":
                                offset = int(offstr)
                if c is None:
                    raise "did not find component in netlist"
                pos = module.GetPosition()
                mid_x = Decimal(pos[0]) / Decimal(1000000)
                mid_y = Decimal(pos[1]) / Decimal(-1000000)
                out.writerow([
                    module.GetReference(),
                    "{}mm".format(mid_x),
                    "{}mm".format(mid_y),
                    "Top" if module.GetLayer() == 0 else "Bottom",
                    (module.GetOrientationDegrees() + offset) % 360])
        wx.MessageBox("Placement file generated.",
              'Done', wx.OK | wx.ICON_INFORMATION)


jlcpcb_cpl().register()
