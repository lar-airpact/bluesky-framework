#******************************************************************************
#
#  BlueSky Framework - Controls the estimation of emissions, incorporation of 
#                      meteorology, and the use of dispersion models to 
#                      forecast smoke impacts from fires.
#  Copyright (C) 2003-2006  USDA Forest Service - Pacific Northwest Wildland 
#                           Fire Sciences Laboratory
#  BlueSky Framework - Version 3.5.1    
#  Copyright (C) 2007-2009  USDA Forest Service - Pacific Northwest Wildland Fire 
#                      Sciences Laboratory and Sonoma Technology, Inc.
#                      All rights reserved.
#
# See LICENSE.TXT for the Software License Agreement governing the use of the
# BlueSky Framework - Version 3.5.1.
#
# Contributors to the BlueSky Framework are identified in ACKNOWLEDGEMENTS.TXT
#
#******************************************************************************

_bluesky_version_ = "3.5.1"

from kernel.core import Process

class DispersionMet(Process):
    def init(self):
        self.declare_input("met_info", "MetInfo")
        self.declare_output("met_info", "MetInfo")

class Dispersion(Process):
    def init(self):
        self.declare_input("met_info", "MetInfo")
        self.declare_input("fires", "FireInformation")
        self.declare_output("fires", "FireInformation")
