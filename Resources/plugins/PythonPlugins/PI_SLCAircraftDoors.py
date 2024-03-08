################################################################################
#                                                                              #
#    PI_SLCAircraftDoors.py                          #####     ####            #
#                                                    ##   ##   ##   ##         #
#    By: Bruno Costa                                 ##  ##    ##              #
#                                                    ##   ##   ##              #
#    Created: 03/03/2024 22:19:19                    ##   ##   ##   ##         #
#    Updated: 05/03/2024 17:22:30                    #####     ####            #
#                                                                              #
################################################################################
#
#    MIT License
#
#    Copyright (c) 2024, Bruno Costa
#    All rights reserved.
#

class Aircraft:
    doors_dataref = None
    door_open_value = 0
    door_closed_value = 0
    door_commands_open = []
    door_commands_close = []

    @staticmethod
    def A333():
        Aircraft.door_open_value = 1 # Door open value
        Aircraft.door_closed_value = 0 # Door closed value

        # Dataref containing int array with door statuses
        Aircraft.doors_dataref = xp.findDataRef('sim/flightmodel2/misc/door_open_ratio')

        # Datarefs containing command to open doors. Must be in order.
        Aircraft.door_commands_open = [
            'sim/flight_controls/door_open_1', 
            'sim/flight_controls/door_open_2',
            'sim/flight_controls/door_open_3',
            'sim/flight_controls/door_open_4',
            'sim/flight_controls/door_open_5',
            'sim/flight_controls/door_open_6',
            'sim/flight_controls/door_open_7',
            'sim/flight_controls/door_open_8'
        ]

        # Datarefs containing command to close doors. Must be in order.
        Aircraft.door_commands_close = [
            'sim/flight_controls/door_close_1',
            'sim/flight_controls/door_close_2',
            'sim/flight_controls/door_close_3',
            'sim/flight_controls/door_close_4',
            'sim/flight_controls/door_close_5',
            'sim/flight_controls/door_close_6',
            'sim/flight_controls/door_close_7',
            'sim/flight_controls/door_close_8'
        ]

    @staticmethod
    def B738():
        Aircraft.door_open_value = 1 # Door open value
        Aircraft.door_closed_value = 0 # Door closed value

        # Dataref containing int array with door statuses
        Aircraft.doors_dataref = xp.findDataRef('sim/flightmodel2/misc/door_open_ratio')

        # Datarefs containing command to open doors. Must be in order.
        Aircraft.door_commands_open = [
            'sim/flight_controls/door_open_1', 
            'sim/flight_controls/door_open_2',
            'sim/flight_controls/door_open_3',
            'sim/flight_controls/door_open_4',
            'sim/flight_controls/door_open_5',
            'sim/flight_controls/door_open_6',
            'sim/flight_controls/door_open_7',
            'sim/flight_controls/door_open_8'
        ]

        # Datarefs containing command to close doors. Must be in order.
        Aircraft.door_commands_close = [
            'sim/flight_controls/door_close_1',
            'sim/flight_controls/door_close_2',
            'sim/flight_controls/door_close_3',
            'sim/flight_controls/door_close_4',
            'sim/flight_controls/door_close_5',
            'sim/flight_controls/door_close_6',
            'sim/flight_controls/door_close_7',
            'sim/flight_controls/door_close_8'
        ]

    @staticmethod
    def B738X():
        Aircraft.door_open_value = 0 # Door open value
        Aircraft.door_closed_value = 2 # Door closed value

        # Dataref containing int array with door statuses
        Aircraft.doors_dataref = xp.findDataRef('laminar/B738/doors/status')

        # Datarefs containing command to open doors. Must be in order.
        Aircraft.door_commands_open = [
            'sim/flight_controls/door_open_1', 
            'sim/flight_controls/door_open_5',
            'sim/flight_controls/door_open_9',
            'sim/flight_controls/door_open_4',
            'sim/flight_controls/door_open_8',
            'sim/flight_controls/door_open_10',
            'sim/flight_controls/door_open_2',
            'sim/flight_controls/door_open_3'
        ]

        # Datarefs containing command to close doors. Must be in order.
        Aircraft.door_commands_close = [
            'sim/flight_controls/door_close_1',
            'sim/flight_controls/door_close_5',
            'sim/flight_controls/door_close_9',
            'sim/flight_controls/door_close_4',
            'sim/flight_controls/door_close_8',
            'sim/flight_controls/door_close_10',
            'sim/flight_controls/door_close_2',
            'sim/flight_controls/door_close_3'
        ]

    @staticmethod
    def MD82():
        Aircraft.door_open_value = 1 # Door open value
        Aircraft.door_closed_value = 0 # Door closed value

        # Dataref containing int array with door statuses
        Aircraft.doors_dataref = xp.findDataRef('sim/flightmodel2/misc/door_open_ratio')

        # Datarefs containing command to open doors. Must be in order.
        Aircraft.door_commands_open = [
            'sim/flight_controls/door_open_1', 
            'sim/flight_controls/door_open_2',
            'sim/flight_controls/door_open_3',
            'sim/flight_controls/door_open_4',
            'sim/flight_controls/door_open_5',
            'sim/flight_controls/door_open_6',
            'sim/flight_controls/door_open_7',
            'sim/flight_controls/door_open_8'
        ]

        # Datarefs containing command to close doors. Must be in order.
        Aircraft.door_commands_close = [
            'sim/flight_controls/door_close_1',
            'sim/flight_controls/door_close_2',
            'sim/flight_controls/door_close_3',
            'sim/flight_controls/door_close_4',
            'sim/flight_controls/door_close_5',
            'sim/flight_controls/door_close_6',
            'sim/flight_controls/door_close_7',
            'sim/flight_controls/door_close_8'
        ]

    # Dictionary of supported aircraft
    aircraft = {
        "Airbus A330-300": A333, # Laminar A333
        "Boeing 737-800": B738, # Laminar B738
        "B737-800X": B738X, # Zibomod B738
        "McDonnell Douglas MD-82": MD82 # Laminar MD-82
    }

################################################################################
#                                                                              #
# WARNING: EDITING BEYOND THIS POINT MAY LEAD TO UNINTENDED CONSEQUENCES!      #
#                                                                              #
# THE CODE BELOW HOLDS SECRETS AND SURPRISES THAT EVEN THE BRAVEST MAY FIND    #
# PERPLEXING. ENTER AT YOUR OWN RISK!                                          #
#                                                                              #
################################################################################

VERSION = "v1.0.1"
DOOR_CLOSED = 0
DOOR_OPEN = 1

import xp, os

class Utils:

    @staticmethod
    def get_bit_at_index(data, index):
        mask = 1 << index
        return (data & mask) >> index

    @staticmethod
    def set_bit_at_index(data, value, index):
        mask = 1 << index
        if value == Aircraft.door_closed_value:
            return data & ~mask  # Clear the bit at the index
        else:
            return data | mask  # Set the bit at the index to 1

    @staticmethod
    def extract_aircraft_dir(aircraft_path):
        dir = os.path.dirname(aircraft_path)

        return str(os.path.basename(dir))

    @staticmethod
    def sim_aircraft_init():
        PythonInterface.reset_data()

        _, aircraft_path = xp.getNthAircraftModel(0)
        aircraft_dir = Utils.extract_aircraft_dir(aircraft_path)
        if aircraft_dir in Aircraft.aircraft:
            Aircraft.aircraft[aircraft_dir]()

            if Aircraft.doors_dataref:
                xp.sys_log(aircraft_dir + " configuration loaded.")
            else:
                xp.sys_log(aircraft_dir + " configuration loaded, with errors.")
            return 1
        xp.sys_log(aircraft_dir + " configuration was not found. " + \
            "Ensure you're using a supported aircraft and haven't changed the original directory name.")
        return 0

class PythonInterface:
    aircraft_doors = 0

    @property
    def on_ground(self) -> bool:
        gear_on_ground_data = []
        xp.getDatavi(self.gear_on_ground_dataref, gear_on_ground_data, count=3)
        return any(gear_on_ground_data)

    @staticmethod
    def reset_data():
        PythonInterface.aircraft_doors = 0
        PythonInterface.slc_doors_data_cache = 0
        PythonInterface.sim_doors_data_cache = [0] * 8

    def read_slc_aircraft_doors(self, read_ref_con):
        return self.aircraft_doors

    def write_slc_aircraft_doors(self, write_ref_con, value):
        if self.on_ground:
            self.aircraft_doors = value
            self.slc_doors_data_cache = value

            # Runs command to open or close sim door based on slc/doors/status
            for i in range(8):
                slc_door_status = Utils.get_bit_at_index(value, i)
                sim_door_open = self.sim_doors_data_cache[i] == Aircraft.door_open_value

                # Check if slc/doors/status changed, but not sim doors.
                if (slc_door_status == DOOR_CLOSED and sim_door_open) or \
                (slc_door_status == DOOR_OPEN and not sim_door_open):
                    if slc_door_status == DOOR_CLOSED:
                        xp.commandOnce(xp.findCommand(Aircraft.door_commands_close[i]))
                        self.sim_doors_data_cache[i] = Aircraft.door_closed_value
                    else:
                        xp.commandOnce(xp.findCommand(Aircraft.door_commands_open[i]))
                        self.sim_doors_data_cache[i] = Aircraft.door_open_value

    def loopCallback(self, lastCall, elapsedTime, counter, refCon):
        if self.on_ground:
            if Aircraft.doors_dataref:
                sim_doors_data = []
                xp.getDatavi(Aircraft.doors_dataref, sim_doors_data, count=8)

                # Check if sim door status has changed
                if sim_doors_data != self.sim_doors_data_cache:
                    slc_doors_data = self.slc_doors_data_cache
                    for i, door_status in enumerate(sim_doors_data):
                        if door_status in {Aircraft.door_closed_value, Aircraft.door_open_value}:
                            self.sim_doors_data_cache[i] = sim_doors_data[i]
                            slc_doors_data = Utils.set_bit_at_index(slc_doors_data, door_status, i)
                    xp.setDatai(self.slc_doors_dataref, slc_doors_data)
                    self.slc_doors_data_cache = slc_doors_data
            else:
                xp.sys_log("Identified an issue with the loaded configuration. Initiating reload attempt.")
                Utils.sim_aircraft_init()
            self.flight_loop_interval = 1
        else:
            self.flight_loop_interval = 30
        return self.flight_loop_interval

    def __init__(self):
        self.Name = "SLCAircraftDoors"
        self.Sig = "slcaircraftdoors.xppython3"
        self.Desc = "Plugin to handle SLC Virtual Doors based on aircraft doors"

        self.flight_loop = self.loopCallback
        self.flight_loop_id = None
        self.flight_loop_interval = 1

        self.gear_on_ground_dataref = xp.findDataRef('sim/flightmodel2/gear/on_ground')

        self.slc_doors_data_cache = 0
        self.sim_doors_data_cache = [0] * 8

    def XPluginStart(self):
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

        self.slc_doors_dataref = xp.registerDataAccessor(
                    'slc/doors/status', 
                    readInt=self.read_slc_aircraft_doors,
                    writeInt=self.write_slc_aircraft_doors
                )
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored

        xp.unregisterDataAccessor(self.slc_doors_dataref)

    def XPluginEnable(self):
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.

        if not Utils.sim_aircraft_init():
            if self.flight_loop_id:
                xp.destroyFlightLoop(self.flight_loop_id)
        elif not self.flight_loop_id:
            self.flight_loop_id = xp.createFlightLoop(self.flight_loop, phase=1)
            xp.scheduleFlightLoop(self.flight_loop_id, interval=self.flight_loop_interval)

        return 1

    def XPluginDisable(self):
        # Called once by X-Plane, when plugin is requested to be disabled. All plugins
        # are disabled prior to Stop.
        # Return is ignored

        if self.flight_loop_id:
            xp.destroyFlightLoop(self.flight_loop_id)

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        # Called by X-Plane whenever a plugin message is being sent to your
        # plugin. Messages include MSG_PLANE_LOADED, MSG_ENTERED_VR, etc., as
        # described in XPLMPlugin module.
        # Messages may be custom inter-plugin messages, as defined by other plugins.
        # Return is ignored
        if (inMessage == xp.MSG_PLANE_LOADED):
            xp.sys_log("Received MSG_PLANE_LOADED.")
            if not Utils.sim_aircraft_init():
                if self.flight_loop_id:
                    xp.destroyFlightLoop(self.flight_loop_id)
            elif not self.flight_loop_id:
                self.flight_loop_id = xp.createFlightLoop(self.flight_loop, phase=1)
                xp.scheduleFlightLoop(self.flight_loop_id, interval=self.flight_loop_interval)
