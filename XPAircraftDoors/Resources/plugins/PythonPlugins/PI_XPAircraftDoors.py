################################################################################
#                                                                              #
#    PI_XPAircraftDoors.py                           #####     ####            #
#                                                    ##   ##   ##   ##         #
#    By: Bruno Costa <support@bybrunocosta.com>      ##  ##    ##              #
#                                                    ##   ##   ##              #
#    Created: 2024-03-03T22:19:19.368Z               ##   ##   ##   ##         #
#    Updated: 2024-10-10T19:39:26.707Z               #####     ####            #
#                                                                              #
################################################################################
#
#    MIT License
#
#    Copyright (c) 2024, Bruno Costa
#    All rights reserved.
#


class B738:
    @classmethod
    def dispatch(cls, acf_dir):
        # Try to match aircraft by directory
        if acf_dir in cls.supported_dir:
            cls.supported_dir[acf_dir]()
            return 1
        # Try to match aircraft by aircraft plugin
        for plugin in cls.acf_plugins:
            plugin_id = xp.findPluginBySignature(plugin)
            if plugin_id != xp.NO_PLUGIN_ID and xp.isPluginEnabled(plugin_id):
                cls.acf_plugins[plugin]()
                return 1
        return 0

    @staticmethod
    def b738X():
        Aircraft.configuration_name = "Zibomod B738"
        Aircraft.door_open_value = 0 # Door open value
        Aircraft.door_closed_value = 2 # Door closed value

        # Dataref containing int array with door statuses
        setattr(Aircraft, "doors_dataref", xp.findDataRef('laminar/B738/doors/status'))

        # Datarefs containing command to open doors. Must be in order.
        Aircraft.door_command_open_datarefs = [
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
        Aircraft.door_command_close_datarefs = [
            'sim/flight_controls/door_close_1',
            'sim/flight_controls/door_close_5',
            'sim/flight_controls/door_close_9',
            'sim/flight_controls/door_close_4',
            'sim/flight_controls/door_close_8',
            'sim/flight_controls/door_close_10',
            'sim/flight_controls/door_close_2',
            'sim/flight_controls/door_close_3'
        ]

    supported_dir = {
        "B737-800X": b738X
    }

    acf_plugins = {
        "zibomod.by.Zibo": b738X
    }


class Laminar:
    @classmethod
    def dispatch(cls, acf_dir, acf_icao):
        # Check if supported airliner
        if acf_icao in cls.supported_icao and \
            acf_dir == cls.supported_dir[acf_icao]:
            cls.laminar()
            return 1
        return 0

    @staticmethod
    def laminar():
        Aircraft.configuration_name = "Laminar Research"

        Aircraft.door_open_value = 1 # Door open value
        Aircraft.door_closed_value = 0 # Door closed value
        # Dataref containing int array with door statuses
        setattr(Aircraft, "doors_dataref", xp.findDataRef('sim/flightmodel2/misc/door_open_ratio'))
        
        # Aircraft.door_open_value = 0 # Door open value
        # Aircraft.door_closed_value = -1 # Door closed value
        # # Datarefs containing door status
        # door_datarefs = []
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide1"))
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide2"))
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide3"))
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide4"))
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide5"))
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide6"))
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide7"))
        # door_datarefs.append(xp.findDataRef("laminar/A333/ECAM/doors/slide8"))
        # setattr(Aircraft, "door_datarefs", door_datarefs)

        # Datarefs containing command to open doors. Must be in order.
        Aircraft.door_command_open_datarefs = [
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
        Aircraft.door_command_close_datarefs = [
            'sim/flight_controls/door_close_1',
            'sim/flight_controls/door_close_2',
            'sim/flight_controls/door_close_3',
            'sim/flight_controls/door_close_4',
            'sim/flight_controls/door_close_5',
            'sim/flight_controls/door_close_6',
            'sim/flight_controls/door_close_7',
            'sim/flight_controls/door_close_8'
        ]

    supported_icao = {
        "A333",
        "B738"
    }

    supported_dir = {
        "A333": "Airbus A330-300",
        "B738": "Boeing 737-800"
    }


class Aircraft:
    configuration_name = None
    door_open_value = 0
    door_closed_value = 0
    door_command_open_datarefs = []
    door_command_close_datarefs = []

    supported_acf = {
        "Laminar": Laminar.dispatch,
        "B738": B738.dispatch
    }


################################################################################
#                                                                              #
# WARNING: EDITING BEYOND THIS POINT MAY LEAD TO UNINTENDED CONSEQUENCES!      #
#                                                                              #
# THE CODE BELOW HOLDS SECRETS AND SURPRISES THAT EVEN THE BRAVEST MAY FIND    #
# PERPLEXING. ENTER AT YOUR OWN RISK!                                          #
#                                                                              #
################################################################################

__version__ = "v1.3.1"

import xp, os

DOOR_CLOSED = 0
DOOR_OPEN = 1
MAX_RETRIES = 3
NUMBER_OF_DOORS = 8
DEFAULT_FLIGHT_LOOP_INTERVAL = -1

XPTK_DOORS_STATUS_DATAREF_NAME = "xptk/doors/status"


class classproperty(property):

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


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
    def extract_dir(acf_path):
        dir = os.path.dirname(acf_path)

        return str(os.path.basename(dir))

    @staticmethod
    def extract_studio(acf_path):
        dir = os.path.dirname(os.path.dirname(acf_path))

        return str(os.path.basename(dir))


class FrameRateMonitor:
    frame_rate = 1

    @classmethod
    def enable(cls):
        if cls.flight_loop_id is None:
            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)
        return 1

    @classmethod
    def disable(cls):
        if cls.flight_loop_id:
            xp.destroyFlightLoop(cls.flight_loop_id)
            cls.flight_loop_id = None

    @classmethod
    def reload(cls):
        cls.disable()
        cls.enable()

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        cls.frame_rate = 1 / sinceLast
        return -1

    flight_loop = flight_loop_callback
    flight_loop_id = None


class AcfSelector:
    flight_loop_counter = 0

    @classmethod
    def enable(cls):
        if cls.flight_loop_id is None:
            PythonInterface.handler(AcfMonitor.disable)
            cls.flight_loop_counter = 0

            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)
        return 1

    @classmethod
    def disable(cls):
        if cls.flight_loop_id:
            xp.destroyFlightLoop(cls.flight_loop_id)
            cls.flight_loop_id = None

    @classmethod
    def reload(cls):
        cls.disable()
        cls.enable()

    @classmethod
    def retrieve_acf(cls, acf_icao):
        _, acf_path = xp.getNthAircraftModel(0)
        acf_dir = Utils.extract_dir(acf_path)

        xp.sys_log("[INFO] Trying to retrieve configuration for '" + acf_icao + "'.")
        is_supported_laminar_acf = Utils.extract_studio(acf_path) == "Laminar Research" and \
                                    Aircraft.supported_acf["Laminar"](acf_dir, acf_icao)
        is_supported_addon_acf = acf_icao in Aircraft.supported_acf and \
                                    Aircraft.supported_acf[acf_icao](acf_dir)
        if is_supported_laminar_acf or is_supported_addon_acf:
            invalid_dataref = False
            for attr_name, attr_value in vars(Aircraft).items():
                if attr_name.endswith("_dataref") and not callable(attr_value):
                    if attr_value is None:
                        invalid_dataref = True
                        xp.sys_log(f"[WARNING] Unable to find {attr_name} dataref for {Aircraft.configuration_name}.")
                elif attr_name.endswith("_datarefs") and not callable(attr_value):
                    if isinstance(attr_value, dict):
                        for key, value in attr_value.items():
                            if not value:
                                invalid_dataref = True
                                xp.sys_log(f"[WARNING] Invalid dataref found in {Aircraft.configuration_name}'s {attr_name} at {key}.")
                    else:
                        for index, value in enumerate(attr_value):
                            if index == NUMBER_OF_DOORS:
                                invalid_dataref = True
                                xp.sys_log(f"[WARNING] Dataref limit reached in {Aircraft.configuration_name}'s {attr_name}. \
                                           Max datarefs size is: {str(NUMBER_OF_DOORS)}.")
                                break
                            elif not value:
                                invalid_dataref = True
                                xp.sys_log(f"[WARNING] Invalid dataref found in {Aircraft.configuration_name}'s {attr_name} at {index}.")
            if not invalid_dataref and (hasattr(Aircraft, "doors_dataref") or hasattr(Aircraft, "door_datarefs")):
                xp.sys_log(f"[INFO] '{Aircraft.configuration_name}' configuration loaded.")
                return 1
            else:
                xp.sys_log(f"[WARNING] Identified an issue with '{Aircraft.configuration_name}' configuration. Retrying to load configuration.")
        return 0

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        PythonInterface.handler(AcfMonitor.disable)

        acf_icao = xp.getDatas(cls.acf_icao_dataref)
        if not cls.retrieve_acf(acf_icao):
            cls.flight_loop_counter += 1
            if cls.flight_loop_counter < MAX_RETRIES:
                xp.sys_log("[WARNING] Unable to retrieve '" + acf_icao + "' configuration. " + \
                    "Will try again in 5 seconds.")
                PythonInterface.flight_loop_interval = 5 # seconds
                return PythonInterface.flight_loop_interval

            xp.sys_log("[ERROR] A valid configuration for '" + acf_icao + "' was not found. " + \
                "Ensure you're using a supported aircraft.")
            PythonInterface.handler(Menu.disable)
        else:
            PythonInterface.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL
            PythonInterface.handler(AcfMonitor.enable)
        return 0

    flight_loop = flight_loop_callback
    flight_loop_id = None

    acf_icao_dataref = xp.findDataRef('sim/aircraft/view/acf_ICAO')


class AcfMonitor:
    xptk_doors_status_data_cache = 0
    sim_doors_data_cache = [0] * NUMBER_OF_DOORS

    @classproperty
    def engines_running(self) -> bool:
        values = []
        xp.getDatavi(self.engines_is_burning_fuel_dataref, values, count=2)
        return any(values)

    @classproperty
    def on_ground(self) -> bool:
        gear_on_ground_data = []
        xp.getDatavi(self.gear_on_ground_dataref, gear_on_ground_data, count=3)
        return any(gear_on_ground_data)

    @classmethod
    def reset_data(cls):
        cls.xptk_doors_status_data_cache = 0
        cls.sim_doors_data_cache = [Aircraft.door_closed_value] * NUMBER_OF_DOORS

    @classmethod
    def enable(cls):
        if cls.flight_loop_id is None:
            cls.reset_data()

            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)
        return 1

    @classmethod
    def disable(cls):
        if cls.flight_loop_id:
            PythonInterface.handler(FrameRateMonitor.disable)

            xp.destroyFlightLoop(cls.flight_loop_id)
            cls.flight_loop_id = None

    @classmethod
    def reload(cls):
        cls.disable()
        cls.enable()

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        if cls.on_ground:
            if not cls.engines_running:
                PythonInterface.handler(FrameRateMonitor.enable)

                sim_doors_data = []
                if hasattr(Aircraft, "doors_dataref"):
                    xp.getDatavi(getattr(Aircraft, "doors_dataref"), sim_doors_data, count=NUMBER_OF_DOORS)
                elif hasattr(Aircraft, "door_datarefs"):
                    door_datarefs = getattr(Aircraft, "door_datarefs")
                    for dataref in door_datarefs:
                        sim_doors_data.append(xp.getDatai(dataref))

                cached = sim_doors_data == cls.sim_doors_data_cache
                if not cached:
                    xptk_doors_status_data = cls.xptk_doors_status_data_cache
                    for i, door_status in enumerate(sim_doors_data):
                        if door_status != cls.sim_doors_data_cache[i]:
                            if door_status in {Aircraft.door_closed_value, Aircraft.door_open_value}:
                                cls.sim_doors_data_cache[i] = door_status
                                xptk_doors_status_data = Utils.set_bit_at_index(xptk_doors_status_data, door_status, i)
                                xp.setDatai(cls.xptk_doors_status_dataref, xptk_doors_status_data)
                                cls.xptk_doors_status_data_cache = xptk_doors_status_data
                PythonInterface.flight_loop_interval = -1 * FrameRateMonitor.frame_rate / 2 # 2x Real-time
            else:
                PythonInterface.handler(FrameRateMonitor.disable)
                PythonInterface.flight_loop_interval = 2 # seconds
        else:
            PythonInterface.handler(FrameRateMonitor.disable)
            PythonInterface.flight_loop_interval = 30 # seconds
        return PythonInterface.flight_loop_interval

    flight_loop = flight_loop_callback
    flight_loop_id = None
    xptk_doors_status_dataref = None

    gear_on_ground_dataref = xp.findDataRef('sim/flightmodel2/gear/on_ground')
    engines_is_burning_fuel_dataref = xp.findDataRef('sim/flightmodel2/engines/engine_is_burning_fuel')

class Menu:
    id = None
    
    @classproperty
    def is_enabled(cls) -> bool:
        if xp.checkMenuItemState(cls.id, 0) == 2:
            return True
        return False

    @classmethod
    def create(cls):
        cls.id = xp.createMenu('XPAircraftDoors', handler=cls.callback)
        xp.appendMenuItem(cls.id, 'Enabled', 'enabled')
        xp.checkMenuItem(cls.id, 0, xp.Menu_Unchecked)
        return cls.id

    @classmethod
    def destroy(cls):
        if cls.id:
            xp.destroyMenu(cls.id)

    @classmethod
    def enable(cls):
        if cls.id is None:
            xp.sys_log("[ERROR] Unable to create Plugin's menu.")
            return 0

        for attr_name, attr_value in vars(AcfSelector).items():
            if attr_name.endswith("_dataref") and not callable(attr_value):
                if attr_value is None:
                    xp.sys_log(f"[ERROR] Unable to find {attr_name} dataref.")
                    return 0

        for attr_name, attr_value in vars(AcfMonitor).items():
            if attr_name.endswith("_dataref") and not callable(attr_value):
                if attr_value is None:
                    xp.sys_log(f"[ERROR] Unable to find {attr_name} dataref.")
                    return 0
        
        xpuipc_plugin_id = xp.findPluginBySignature('XPUIPC/XPWideFS.')

        if xpuipc_plugin_id == xp.NO_PLUGIN_ID:
            xp.sys_log("[ERROR] Unable to find XPUIPC.")
            return 0

        AcfSelector.enable()
        xp.checkMenuItem(cls.id, 0, xp.Menu_Checked)
        return 1

    @classmethod
    def disable(cls):
        AcfMonitor.disable()
        AcfSelector.disable()
        FrameRateMonitor.disable()
        xp.checkMenuItem(cls.id, 0, xp.Menu_Unchecked)

    @classmethod
    def reload(cls):
        cls.disable()
        cls.enable()

    @classmethod
    def callback(cls, menuRefCon, itemRefCon):
        if itemRefCon == 'enabled' and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Checked:
            cls.disable()
        elif itemRefCon == 'enabled' and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Unchecked:
            cls.enable()


class PythonInterface:
    xptk_doors_status = 0

    def read_xp_acf_doors(self, read_ref_con):
        return self.xptk_doors_status

    def write_xp_acf_doors(self, write_ref_con, value):
        if AcfMonitor.on_ground:
            self.xptk_doors_status = value
            AcfMonitor.xptk_doors_status_data_cache = value

            # Runs command to open or close sim door based on xptk/doors/status
            for i in range(NUMBER_OF_DOORS):
                xp_door_status = Utils.get_bit_at_index(value, i)
                sim_door_open = AcfMonitor.sim_doors_data_cache[i] == Aircraft.door_open_value

                # Check if xptk/doors/status changed, but not sim doors.
                if (xp_door_status == DOOR_CLOSED and sim_door_open) or \
                    (xp_door_status == DOOR_OPEN and not sim_door_open):
                    if xp_door_status == DOOR_CLOSED:
                        sim_command = xp.findCommand(Aircraft.door_command_close_datarefs[i])
                        if sim_command is None:
                            self.xptk_doors_status = Utils.set_bit_at_index(self.xptk_doors_status, Aircraft.door_open_value, i)
                            AcfMonitor.xptk_doors_status_data_cache = self.xptk_doors_status
                        else:
                            xp.commandOnce(sim_command)
                            AcfMonitor.sim_doors_data_cache[i] = Aircraft.door_closed_value
                    else:
                        sim_command = xp.findCommand(Aircraft.door_command_open_datarefs[i])
                        if sim_command is None or AcfMonitor.engines_running:
                            self.xptk_doors_status = Utils.set_bit_at_index(self.xptk_doors_status, Aircraft.door_closed_value, i)
                            AcfMonitor.xptk_doors_status_data_cache = self.xptk_doors_status
                        else:
                            xp.commandOnce(sim_command)
                            AcfMonitor.sim_doors_data_cache[i] = Aircraft.door_open_value

    @staticmethod
    def handler(func, *args):
        return func(*args)

    def __init__(self):
        self.Name = "XPAircraftDoors"
        self.Sig = "xpaircraftdoors.xppython3"
        self.Desc = "Translate XP Aircrafts door data to XPUIPC offset"

        self.xptk_doors_status_accessor = None
        self.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL

    def XPluginStart(self):
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

        self.xptk_doors_status_accessor = xp.registerDataAccessor(
                    XPTK_DOORS_STATUS_DATAREF_NAME, 
                    readInt=self.read_xp_acf_doors,
                    writeInt=self.write_xp_acf_doors
                )
        setattr(AcfMonitor, "xptk_doors_status_dataref", xp.findDataRef(XPTK_DOORS_STATUS_DATAREF_NAME))
        Menu.create()
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored

        xp.unregisterDataAccessor(self.xptk_doors_status_accessor)
        Menu.destroy()

    def XPluginEnable(self):
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.

        return Menu.enable()

    def XPluginDisable(self):
        # Called once by X-Plane, when plugin is requested to be disabled. All plugins
        # are disabled prior to Stop.
        # Return is ignored

        Menu.disable()

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        # Called by X-Plane whenever a plugin message is being sent to your
        # plugin. Messages include MSG_PLANE_LOADED, MSG_ENTERED_VR, etc., as
        # described in XPLMPlugin module.
        # Messages may be custom inter-plugin messages, as defined by other plugins.
        # Return is ignored
        if (inMessage == xp.MSG_PLANE_LOADED):
            if Menu.is_enabled:
                Menu.reload()
            else:
                Menu.enable()
