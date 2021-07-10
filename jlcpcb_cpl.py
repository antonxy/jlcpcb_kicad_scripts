import os
import sys
import pcbnew
import csv

"""
pcbnew action plugin to export component placement list according to JLCPCB format.
SMT and Through-Hole will be contained in the file.

WARNING: Axis origin seems not to match and had to be manually corrected after ordering,
check before using next time


Windows 7/Windows 10:
Install the plugins in: %APPDATA%\kicad\scripting\plugins

GNU/Linux:
Install the plugins in: ~/.kicad/scripting/plugins or ~/.kicad_plugins

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
            outname = os.path.join(os.path.dirname(my_board.GetFileName()), "jlc_cpl.csv")
                
            f = open(outname, 'w')
            out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
            out.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])

            for module in my_board.GetModules():
                if module.GetAttributes() != pcbnew.MOD_VIRTUAL:
                    out.writerow([
                        module.GetReference(),
                        "{}mm".format(pcbnew.ToMM(module.GetPosition().x)),
                        "{}mm".format(pcbnew.ToMM(module.GetPosition().y)),
                        "Top" if module.GetLayer() == 0 else "Bottom",
                        module.GetOrientation()/10])


jlcpcb_cpl().register()
