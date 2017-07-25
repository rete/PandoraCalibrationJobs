#!/usr/bin/python

"""
"""

from calibration.CalibrationManager import CalibrationManager
from calibration.MipScaleStep import *
from calibration.EcalEnergyStep import *
from calibration.HcalEnergyStep import *

import os
import sys
from shutil import copyfile
import argparse

compactFile = ""
maxNIterations = 5
startStep = 0
endStep = sys.maxint
lcioPhotonFile = "ddsim-photon-calibration.slcio"
lcioKaon0LFile = "ddsim-kaon0L-calibration.slcio"
lcioMuonFile = "ddsim-muon-calibration.slcio"

ecalCalibrationAccuracy = 0.01
hcalCalibrationAccuracy = 0.01

inputCalibrationFile = ""
outputCalibrationFile = None

marlinSteeringFile = ""
pathToPandoraAnalysis = ""
maxRecordNumber = 0   # process the whole file


manager = CalibrationManager()

# add a calibration step here
manager.addStep( MipScaleStep() )
manager.addStep( EcalEnergyStep() )
manager.addStep( HcalBarrelEnergyStep() )
manager.addStep( HcalEndcapEnergyStep() )



parser = argparse.ArgumentParser("Running energy calibration:",
                                     formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--showSteps", action="store_true", default=False,
                        help="Show the registered steps and exit", required = False)

parsed = parser.parse_known_args()[0]

if parsed.showSteps :
    manager.printSteps()
    sys.exit(0)

parser.add_argument("--compactFile", action="store", default=compactFile,
                        help="The compact XML file", required = True)

parser.add_argument("--steeringFile", action="store", default=marlinSteeringFile,
                        help="The Marlin steering file (please, look at ILDConfig package)", required = True)

parser.add_argument("--maxNIterations", action="store", default=maxNIterations,
                        help="The maximum number of Marlin reconstruction iterations for calibration", required = False)

parser.add_argument("--ecalCalibrationAccuracy", action="store", default=ecalCalibrationAccuracy,
                        help="The calibration constants accuracy for ecal calibration", required = False)

parser.add_argument("--hcalCalibrationAccuracy", action="store", default=hcalCalibrationAccuracy,
                        help="The calibration constants accuracy for hcal calibration", required = False)

parser.add_argument("--inputCalibrationFile", action="store", default=inputCalibrationFile,
                        help="The XML input calibration file", required = True)

parser.add_argument("--outputCalibrationFile", action="store", default=outputCalibrationFile,
                        help="The XML output calibration file", required = False)

parser.add_argument("--lcioPhotonFile", action="store", default=lcioPhotonFile,
                        help="The lcio input file containing photons to process", required = False)

parser.add_argument("--lcioKaon0LFile", action="store", default=lcioKaon0LFile,
                        help="The lcio input file containing kaon0L to process", required = False)

parser.add_argument("--lcioMuonFile", action="store", default=lcioMuonFile,
                        help="The lcio input file containing muons to process", required = False)

parser.add_argument("--pandoraAnalysis", action="store", default=pathToPandoraAnalysis,
                        help="The path to the PandoraAnalysis package", required = True)

parser.add_argument("--maxRecordNumber", action="store", default=maxRecordNumber,
                        help="The maximum number of events to process", required = False)

parser.add_argument("--startStep", action="store", default=startStep,
                        help="The step id to start from", required = False)

parser.add_argument("--endStep", action="store", default=endStep,
                        help="The step id to stop at", required = False)

parsed = parser.parse_args()


# configure and run
manager.readCmdLine(parsed)
manager.run()

# write the output of each step here
manager.writeXml(parsed.outputCalibrationFile)


#