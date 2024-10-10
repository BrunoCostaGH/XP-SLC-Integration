################################################################################
#                                                                              #
#    PI_AutoGHDforZibo.py                            #####     ####            #
#                                                    ##   ##   ##   ##         #
#    By: Bruno Costa <support@bybrunocosta.com>      ##  ##    ##              #
#                                                    ##   ##   ##              #
#    Created: 2024-03-15T22:08:48.801Z               ##   ##   ##   ##         #
#    Updated: 2024-10-10T19:52:06.010Z               #####     ####            #
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
        if DEBUG: xp.sys_log(f"[DEBUG] Entering B738.dispatch with acf_dir: {acf_dir}")
        # Try to match aircraft by directory
        if acf_dir in cls.supported_dir:
            if DEBUG: xp.sys_log(f"[DEBUG] Matching aircraft by directory: {acf_dir}")
            cls.supported_dir[acf_dir]()
            return 1
        # Try to match aircraft by aircraft plugin
        for plugin in cls.acf_plugins:
            plugin_id = xp.findPluginBySignature(plugin)
            if DEBUG: xp.sys_log(f"[DEBUG] Checking plugin: {plugin}, plugin_id: {plugin_id}")
            if plugin_id != xp.NO_PLUGIN_ID and xp.isPluginEnabled(plugin_id):
                if DEBUG: xp.sys_log(f"[DEBUG] Matching aircraft by plugin: {plugin}")
                cls.acf_plugins[plugin]()
                return 1
        if DEBUG: xp.sys_log("[DEBUG] No match found for aircraft.")
        return 0

    @staticmethod
    def b738X():
        if DEBUG: xp.sys_log("[DEBUG] Configuring Zibomod B738")
        Aircraft.configuration_name = "Zibomod B738"
        Aircraft.ghd_set_name = "Boeing737-800X.set"
        Aircraft.door_open_value = 1 # Door open value
        Aircraft.door_closed_value = 0 # Door closed value

        # Dataref containing int representing airside services state
        Aircraft.auto_flight = xp.findDataRef("laminar/B738/tab/auto_flight")

        # Datarefs containing door status
        door_datarefs = {}
        door_datarefs[FWD_ENTRY] = xp.findDataRef("737u/doors/L1")
        door_datarefs[AFT_ENTRY] = xp.findDataRef("737u/doors/L2")
        door_datarefs[FWD_SERVICE] = xp.findDataRef("737u/doors/R1")
        door_datarefs[AFT_SERVICE] = xp.findDataRef("737u/doors/R2")
        door_datarefs[FWD_CARGO] = xp.findDataRef("737u/doors/Fwd_Cargo")
        door_datarefs[AFT_CARGO] = xp.findDataRef("737u/doors/aft_Cargo")
        setattr(Aircraft, "door_datarefs", door_datarefs)

        # Datarefs containing command to open doors
        door_open_command_datarefs = {}
        door_open_command_datarefs[FWD_ENTRY] = xp.findCommand("sim/flight_controls/door_open_1")
        door_open_command_datarefs[AFT_ENTRY] = xp.findCommand("sim/flight_controls/door_open_4")
        door_open_command_datarefs[FWD_SERVICE] = xp.findCommand("sim/flight_controls/door_open_5")
        door_open_command_datarefs[AFT_SERVICE] = xp.findCommand("sim/flight_controls/door_open_8")
        door_open_command_datarefs[FWD_CARGO] = xp.findCommand("sim/flight_controls/door_open_9")
        door_open_command_datarefs[AFT_CARGO] = xp.findCommand("sim/flight_controls/door_open_10")
        setattr(Aircraft, "door_open_command_datarefs", door_open_command_datarefs)

        # Datarefs containing command to close doors
        door_close_command_datarefs = {}
        door_close_command_datarefs[FWD_ENTRY] = xp.findCommand("sim/flight_controls/door_close_1")
        door_close_command_datarefs[AFT_ENTRY] = xp.findCommand("sim/flight_controls/door_close_4")
        door_close_command_datarefs[FWD_SERVICE] = xp.findCommand("sim/flight_controls/door_close_5")
        door_close_command_datarefs[AFT_SERVICE] = xp.findCommand("sim/flight_controls/door_close_8")
        door_close_command_datarefs[FWD_CARGO] = xp.findCommand("sim/flight_controls/door_close_9")
        door_close_command_datarefs[AFT_CARGO] = xp.findCommand("sim/flight_controls/door_close_10")
        setattr(Aircraft, "door_close_command_datarefs", door_close_command_datarefs)

        # Dataref containing bool, if aircraft has own stairs
        Aircraft.not_airstairs_dataref = xp.findDataRef("laminar/B738/not_airstairs")
        # Dataref containing bool, if aircraft is using own stairs
        Aircraft.airstairs_hide_dataref = xp.findDataRef("laminar/B738/airstairs_hide")
        # Dataref containing command, toggle airstairs
        Aircraft.airstairs_toggle_command_dataref = xp.findCommand("laminar/B738/airstairs_ext_toggle")

        # Dataref containing bool, if aircraft is loading
        Aircraft.loading_dataref = xp.findDataRef("laminar/b738/fmodpack/fmod_play_cargo")

        # Dataref containing bool, if aircraft is boarding
        Aircraft.boarding_dataref = xp.findDataRef("laminar/b738/fmodpack/leg_started")

        # Dataref containing bool, if boarding is complete
        Aircraft.pax_board_dataref = xp.findDataRef("laminar/b738/fmodpack/pax_board")

        # Dataref containing bool, if beacon is on
        Aircraft.beacon_dataref = xp.findDataRef("sim/cockpit/electrical/beacon_lights_on")

        # Dataref containing bool, if chocks are on
        Aircraft.chocks_dataref = xp.findDataRef("laminar/B738/fms/chock_status")
        # Dataref containing command, toggle chocks
        Aircraft.chocks_command_dataref = xp.findCommand("laminar/B738/toggle_switch/chock")

        # Dataref containing float, distance to nearest jetway
        Aircraft.jetway_distance_dataref = xp.findDataRef("laminar/B738/jetway_nearest")

    supported_dir = {
        "B737-800X": b738X
    }

    acf_plugins = {
        "zibomod.by.Zibo": b738X
    }


class Aircraft:
    configuration_name = None
    door_open_value = 0
    door_closed_value = 0

    ghd_set_name = None
    auto_flight = None
    not_airstairs_dataref = None
    airstairs_hide_dataref = None
    airstairs_toggle_command_dataref = None
    loading_dataref = None
    boarding_dataref = None
    pax_board_dataref = None
    beacon_dataref = None
    chocks_dataref = None
    chocks_command_dataref = None
    jetway_distance_dataref = None

    supported_acf = {
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

__version__ = "v1.4.0"

import json
import xp, os

DEBUG = False

DOOR_OPEN = 1
DOOR_CLOSED = 0

MAX_RETRIES = 3
NUMBER_OF_DOORS = 6
DEFAULT_FLIGHT_LOOP_INTERVAL = -1

CATERING_FWD = "Catering-1"
CATERING_AFT = "Catering-2"
STAIRWAY_FWD = "Stairway_l-1"
STAIRWAY_AFT = "Stairway_l-2"
BUS = "Neoplan-1"
VAN = "Van-1"
CARGO_BELT_FWD = "Loader(B)-1"
CARGO_BELT_AFT = "Loader(B)-2"
BAGGAGE_FWD = "Baggage-1"
BAGGAGE_AFT = "Baggage-2"

FWD_ENTRY = "FWD ENTRY"
AFT_ENTRY = "AFT ENTRY"
FWD_SERVICE = "FWD SERVICE"
AFT_SERVICE = "AFT SERVICE"
FWD_CARGO = "FWD CARGO"
AFT_CARGO = "AFT CARGO"

SETTING_AUTOMATED_DOOR_CONTROL = "automated_door_control"
XP_JETWAY_CONNECTED_DATAREF_NAME = "xptk/ghd/jetway_connected"

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
        if DEBUG: xp.sys_log("[DEBUG] Entering FrameRateMonitor.enable method.")
        if cls.flight_loop_id is None:
            if DEBUG: xp.sys_log("[DEBUG] Creating and scheduling flight loop.")
            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)
        else:
            if DEBUG: xp.sys_log("[DEBUG] Flight loop already enabled.")
        if DEBUG: xp.sys_log("[DEBUG] Exiting FrameRateMonitor.enable method.")
        return 1

    @classmethod
    def disable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering FrameRateMonitor.disable method.")
        if cls.flight_loop_id:
            if DEBUG: xp.sys_log("[DEBUG] Destroying flight loop.")
            xp.destroyFlightLoop(cls.flight_loop_id)
            cls.flight_loop_id = None
        else:
            if DEBUG: xp.sys_log("[DEBUG] Flight loop already disabled.")
        if DEBUG: xp.sys_log("[DEBUG] Exiting FrameRateMonitor.disable method.")

    @classmethod
    def reload(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering FrameRateMonitor.reload method.")
        cls.disable()
        cls.enable()
        if DEBUG: xp.sys_log("[DEBUG] Exiting FrameRateMonitor.reload method.")

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        # if DEBUG: xp.sys_log(f"[DEBUG] Entering FrameRateMonitor.flight_loop_callback with sinceLast: {sinceLast}, elapsedTime: {elapsedTime}, counter: {counter}, refCon: {refCon}")
        cls.frame_rate = 1 / sinceLast
        # if DEBUG: xp.sys_log(f"[DEBUG] Updated frame_rate to: {cls.frame_rate}")
        # if DEBUG: xp.sys_log("[DEBUG] Exiting FrameRateMonitor.flight_loop_callback.")
        return -1

    flight_loop = flight_loop_callback
    flight_loop_id = None


class Config:

    @classmethod
    def save(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Config.save method.")
        config = {}
        for attr_name, attr_value in vars(cls).items():
            is_function = callable(attr_value) or isinstance(attr_value, classmethod)
            is_default_attr = attr_name == "prf_file_path" or attr_name == "setting_defaults" or attr_name.startswith("__")
            if not is_function and not is_default_attr:
                config[attr_name] = attr_value

        with open(cls.prf_file_path, "w", encoding="utf-8") as file:
            json.dump(config, file)
        if DEBUG: xp.sys_log("[DEBUG] Exiting Config.save method.")

    @classmethod
    def create(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Config.create method.")
        xp.sys_log(f"[INFO] Initializing configuration file.\nPath: {cls.prf_file_path}.")
        setattr(cls, "settings", cls.setting_defaults)
        cls.save()
        cls.unload()
        if DEBUG: xp.sys_log("[DEBUG] Exiting Config.create method.")

    @classmethod
    def load(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Config.load method.")
        if not os.path.exists(cls.prf_file_path):
            deprecated_file_path = os.path.join(xp.getSystemPath()[:-1], "Resources", "plugins", "PythonPlugins", "AutoGHDforZibo.ini")
            if os.path.exists(deprecated_file_path):
                os.remove(deprecated_file_path)
            else:
                cls.create()

        config = {}
        with open(cls.prf_file_path, "r", encoding="utf-8") as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError:
                xp.sys_log(f"[ERROR] Invalid configuration file.\nPath: {cls.prf_file_path}.")
                return 0
        for key, value in config.items():
            setattr(cls, str(key), value)
        for setting, default in cls.setting_defaults.items():
            if cls.get(f".settings.{setting}") is None:
                return cls.set(f".settings.{setting}", default)
        if DEBUG: xp.sys_log("[DEBUG] Exiting Config.load method.")
        return 1

    @classmethod
    def unload(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Config.unload method.")
        attr_list = []
        for attr_name, attr_value in vars(cls).items():
            is_function = callable(attr_value) or isinstance(attr_value, classmethod)
            is_default_attr = attr_name == "prf_file_path" or attr_name == "setting_defaults" or attr_name.startswith("__")
            if not is_function and not is_default_attr:
                attr_list.append(attr_name)
        for attr_name in attr_list:
            delattr(cls, attr_name)
        if DEBUG: xp.sys_log("[DEBUG] Exiting Config.unload method.")

    @classmethod
    def reload(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Config.reload method.")
        cls.unload()
        cls.load()
        if DEBUG: xp.sys_log("[DEBUG] Exiting Config.reload method.")

    @classmethod
    def get(cls, path: str):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering Config.get method with path: {path}")
        obj = cls
        try:
            route = path.split(".")[1:]
            if len(route) == 1:
                result = getattr(obj, route[-1])
            else:
                for item in route[:-1]:
                    obj = getattr(obj, item)
                result = obj.get(route[-1], None)
            if DEBUG: xp.sys_log(f"[DEBUG] Exiting Config.get method with result: {result}")
            return result
        except AttributeError:
            if DEBUG: xp.sys_log("[DEBUG] Config.get: AttributeError encountered.")
            return None

    @classmethod
    def set(cls, path: str, value):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering Config.set method with path: {path}, value: {value}")
        obj = cls
        try:
            route = path.split(".")[1:]
            if len(route) == 1:
                setattr(obj, route[-1], value)
            else:
                for item in route[:-1]:
                    if not hasattr(obj, item):
                        setattr(obj, item, {})
                    obj = getattr(obj, item)
                obj[route[-1]] = value
            cls.save()
            cls.reload()
            if DEBUG: xp.sys_log("[DEBUG] Exiting Config.set method.")
        except AttributeError:
            if DEBUG: xp.sys_log("[DEBUG] Config.set: AttributeError encountered.")

    prf_file_path = os.path.join(os.path.dirname(xp.getPrefsPath()), "AutoGHDforZibo.prf")
    setting_defaults = {SETTING_AUTOMATED_DOOR_CONTROL: True}


class GHD:

    @classproperty
    def is_enabled(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering GHD.is_enabled method.")
        result = xp.getDatai(GHD.drf_control_dataref) == 1
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting GHD.is_enabled method with result: {result}")
        return result

    @classmethod
    def set_dataref_from_set(cls, index, value, z_coordinate):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering GHD.set_dataref_from_set method with index: {index}, value: {value}, z_coordinate: {z_coordinate}")
        if z_coordinate is not None:
            if z_coordinate < 0:
                # fwd
                value += "-1"
            else:
                # aft
                value += "-2"

        if value in cls.ghd_datarefs:
            cls.ghd_datarefs[value] = xp.findDataRef(f"jd/ghd/select_{index:02d}")
        else:
            xp.sys_log(f"[WARNING] Unsupported type: '{value}'.")
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.set_dataref_from_set method.")

    @classmethod
    def get_set(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering GHD.get_set method.")
        ghd_path = os.path.dirname(xp.getPluginInfo(cls.plugin_id).filePath)
        set_path = os.path.join(ghd_path, "Sets", "Default", Aircraft.ghd_set_name)
        custom_set_path = os.path.join(ghd_path, "Sets", "Custom", Aircraft.ghd_set_name)
        if os.path.exists(custom_set_path):
            set_path = custom_set_path
        elif not os.path.exists(set_path):
            xp.sys_log(f"[ERROR] Failed to locate a suitable configuration set for '{Aircraft.configuration_name}' within JarDesign's Ground Handling Deluxe (GHD).")
            PythonInterface.handler(Menu.disable)
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.get_set method with result: 0")
            return 0

        xp.sys_log(f"[INFO] Found a configuration set for '{Aircraft.configuration_name}' at '{set_path}'.")

        index = 0
        type_name = None
        z_coordinates = []
        with open(set_path, "r") as file:
            for line in file:
                if not line.strip():
                    continue

                if line.startswith("01 type_name"):
                    type_name = line.split("=")[1].strip()
                if line.startswith("04 z_coordinate"):
                    z_coordinates.append(float(line.split("=")[1].strip()))
                if line.startswith("17 split_point"):
                    split_point = int(line.split("=")[1].strip())
                    z_coordinate = z_coordinates[split_point] if split_point < len(z_coordinates) else None
                    cls.set_dataref_from_set(index, type_name, z_coordinate)
                    index += 1
                    type_name = None
                    z_coordinates.clear()

        valid_dataref_count = 0
        for value in cls.ghd_datarefs.values():
            if value is not None:
                valid_dataref_count += 1
        if valid_dataref_count == 0:
            xp.sys_log("[ERROR] Unable to find any supported type within configuration set.")
            PythonInterface.handler(Menu.disable)
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.get_set method with result: 0")
            return 0

        xp.sys_log("[INFO] Loaded JarDesign's Ground Handling Deluxe (GHD) configuration set.")
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.get_set method with result: 1")
        return 1

    @classmethod
    def reset_data(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering GHD.reset_data method.")
        for key in cls.ghd_datarefs.keys():
            cls.ghd_datarefs[key] = None
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.reset_data method.")

    @classmethod
    def enable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering GHD.enable method.")
        if not xp.isPluginEnabled(cls.plugin_id):
            xp.sys_log("[ERROR] JarDesign's Ground Handling Deluxe (GHD) is disabled.")
            PythonInterface.handler(Menu.disable)
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.enable method with result: 0")
            return 0

        PythonInterface.handler(FrameRateMonitor.enable)
        cls.reset_data()

        if not cls.get_set():
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.enable method with result: 0")
            return 0

        xp.setDatai(GHD.drf_control_dataref, 1)
        xp.setDatai(GHD.execute_dataref, 1)
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.enable method with result: 1")
        return 1

    @classmethod
    def disable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering GHD.disable method.")
        xp.setDatai(GHD.drf_control_dataref, 0)
        xp.setDatai(GHD.execute_dataref, 0)
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.disable method.")

    @classmethod
    def select(cls, name):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering GHD.select method with name: {name}")
        if not cls.is_enabled:
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.select method because GHD is not enabled.")
            return
        if cls.ghd_datarefs[name] is None:
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.select method because dataref is None.")
            return
        if name in cls.ghd_dependencies and cls.ghd_dependencies[name] is not None:
            if cls.ghd_dependencies[name] != BUS:
                PythonInterface.handler(AcfMonitor.call_service_crew, cls.ghd_dependencies[name])
        xp.setDatai(cls.ghd_datarefs[name], 1)
        cls.execute()
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.select method.")

    @classmethod
    def remove(cls, name):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering GHD.remove method with name: {name}")
        if not cls.is_enabled:
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.remove method because GHD is not enabled.")
            return
        if cls.ghd_datarefs[name] is None:
            if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.remove method because dataref is None.")
            return
        if name in cls.ghd_dependencies and cls.ghd_dependencies[name] is not None:
            PythonInterface.handler(AcfMonitor.remove_service_crew, cls.ghd_dependencies[name])
        xp.setDatai(cls.ghd_datarefs[name], 0)
        cls.execute()
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.remove method.")

    @classmethod
    def execute(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering GHD.execute method.")
        xp.setDatai(GHD.drf_control_dataref, 1)
        xp.setDatai(GHD.execute_dataref, 1)
        if DEBUG: xp.sys_log("[DEBUG] Exiting GHD.execute method.")

    plugin_id = xp.findPluginBySignature("jardesign.crew.ground.handling")
    execute_dataref = xp.findDataRef("jd/ghd/execute")
    drf_control_dataref = xp.findDataRef("jd/ghd/drfcontrol")

    ghd_datarefs = {
        CATERING_FWD: None,
        CATERING_AFT: None,
        STAIRWAY_FWD: None,
        STAIRWAY_AFT: None,
        BUS: None,
        VAN: None,
        CARGO_BELT_FWD: None,
        CARGO_BELT_AFT: None,
        BAGGAGE_FWD: None,
        BAGGAGE_AFT: None
    }

    ghd_dependencies = {
        CATERING_FWD: None,
        CATERING_AFT: None,
        STAIRWAY_FWD: BUS,
        STAIRWAY_AFT: BUS,
        BUS: None,
        VAN: None,
        CARGO_BELT_FWD: BAGGAGE_FWD,
        CARGO_BELT_AFT: BAGGAGE_AFT,
        BAGGAGE_FWD: None,
        BAGGAGE_AFT: None
    }

    ghd_by_door = {
        FWD_ENTRY: STAIRWAY_FWD,
        AFT_ENTRY: STAIRWAY_AFT,
        FWD_SERVICE: CATERING_FWD,
        AFT_SERVICE: CATERING_AFT,
        FWD_CARGO: CARGO_BELT_FWD,
        AFT_CARGO: CARGO_BELT_AFT
    }


class AcfSelector:
    flight_loop_counter = 0

    @classmethod
    def enable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfSelector.enable method.")
        if cls.flight_loop_id is None:
            PythonInterface.handler(AcfMonitor.disable)
            cls.flight_loop_counter = 0

            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfSelector.enable method.")
        return 1

    @classmethod
    def disable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfSelector.disable method.")
        if cls.flight_loop_id:
            xp.destroyFlightLoop(cls.flight_loop_id)
            cls.flight_loop_id = None
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfSelector.disable method.")

    @classmethod
    def retrieve_acf(cls, acf_icao):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering AcfSelector.retrieve_acf method with acf_icao: {acf_icao}")
        _, acf_path = xp.getNthAircraftModel(0)
        acf_dir = Utils.extract_dir(acf_path)

        xp.sys_log(f"[INFO] Trying to retrieve configuration for '{acf_icao}'.")
        is_supported_addon_acf = acf_icao in Aircraft.supported_acf and \
                                    Aircraft.supported_acf[acf_icao](acf_dir)
        if is_supported_addon_acf:
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
                        invalid_dataref = True
                        xp.sys_log(f"[WARNING] Unsupported type {type(attr_value)}. Requires {type(dict())}.")
            if not invalid_dataref and hasattr(Aircraft, "door_datarefs"):
                xp.sys_log(f"[INFO] '{Aircraft.configuration_name}' configuration loaded.")
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfSelector.retrieve_acf method with result: 1")
                return 1
            else:
                xp.sys_log(f"[WARNING] Identified an issue with '{Aircraft.configuration_name}' configuration. Retrying to load configuration.")
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfSelector.retrieve_acf method with result: 0")
        return 0

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfSelector.flight_loop_callback method.")
        PythonInterface.handler(AcfMonitor.disable)

        acf_icao = xp.getDatas(cls.acf_icao_dataref)
        if not cls.retrieve_acf(acf_icao):
            cls.flight_loop_counter += 1
            if cls.flight_loop_counter < MAX_RETRIES:
                xp.sys_log(f"[WARNING] Unable to retrieve '{acf_icao}' configuration. " + \
                    "Will try again in 5 seconds.")
                PythonInterface.flight_loop_interval = 5 # seconds
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfSelector.flight_loop_callback method with retry.")
                return PythonInterface.flight_loop_interval

            xp.sys_log(f"[ERROR] A valid configuration for '{acf_icao}' was not found. " + \
                "Ensure you're using a supported aircraft.")
            PythonInterface.handler(Menu.disable)
        else:
            PythonInterface.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL
            PythonInterface.handler(AcfMonitor.enable)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfSelector.flight_loop_callback method.")
        return 0

    flight_loop = flight_loop_callback
    flight_loop_id = None

    acf_icao_dataref = xp.findDataRef("sim/aircraft/view/acf_ICAO")


class AcfMonitor:
    automated_door_control = False
    after_land = False
    loading = False
    boarding = 0
    auto_flight_state_cache = 0
    sim_doors_data_cache = {}

    @classproperty
    def engines_running(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.engines_running method.")
        values = []
        xp.getDatavi(cls.engines_is_burning_fuel_dataref, values, count=2)
        result = any(values)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.engines_running method with result: {result}")
        return result

    @classproperty
    def on_ground(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.on_ground method.")
        gear_on_ground_data = []
        xp.getDatavi(cls.gear_on_ground_dataref, gear_on_ground_data, count=3)
        result = any(gear_on_ground_data)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.on_ground method with result: {result}")
        return result

    @classproperty
    def has_chocks(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.has_chocks method.")
        result = xp.getDatai(Aircraft.chocks_dataref)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.has_chocks method with result: {result}")
        return result

    @classproperty
    def beacon_on(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.beacon_on method.")
        result = xp.getDatai(Aircraft.beacon_dataref)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.beacon_on method with result: {result}")
        return result

    @classproperty
    def auto_flight_state(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.auto_flight_state method.")
        result = xp.getDatai(Aircraft.auto_flight)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.auto_flight_state method with result: {result}")
        return result

    @classproperty
    def has_builtin_stairs(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.has_builtin_stairs method.")
        result = not xp.getDatai(Aircraft.not_airstairs_dataref)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.has_builtin_stairs method with result: {result}")
        return result
    
    @classproperty
    def using_builtin_stairs(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.using_builtin_stairs method.")
        result = not xp.getDatai(Aircraft.airstairs_hide_dataref)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.using_builtin_stairs method with result: {result}")
        return result

    @classproperty
    def requested_service_crew(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.requested_service_crew method.")
        result = xp.getDatai(Aircraft.loading_dataref)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.requested_service_crew method with result: {result}")
        return result

    @classproperty
    def started_flight_leg(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.started_flight_leg method.")
        result = xp.getDatai(Aircraft.boarding_dataref)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.started_flight_leg method with result: {result}")
        return result

    @classproperty
    def pax_onboard(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.pax_onboard method.")
        result = xp.getDatai(Aircraft.pax_board_dataref)
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.pax_onboard method with result: {result}")
        return result

    @classproperty
    def near_jetway(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.near_jetway method.")
        result = xp.getDataf(Aircraft.jetway_distance_dataref) <= 0.05
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting AcfMonitor.near_jetway method with result: {result}")
        return result

    @classmethod
    def reset_cache(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.reset_cache method.")
        cls.sim_doors_data_cache = {}
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.reset_cache method.")

    @classmethod
    def reset_data(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.reset_data method.")
        cls.automated_door_control = Config.get(f".settings.{SETTING_AUTOMATED_DOOR_CONTROL}")
        cls.after_land = False
        cls.loading = False
        cls.boarding = 0
        cls.auto_flight_state_cache = 0
        cls.reset_cache()
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.reset_data method.")

    @classmethod
    def enable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.enable method.")
        if cls.flight_loop_id is None:
            if not PythonInterface.handler(GHD.enable):
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.enable method with result: 0")
                return 0
            cls.reset_data()

            if cls.airstairs_flight_loop_id is None:
                cls.airstairs_flight_loop_id = xp.createFlightLoop(cls.airstairs_flight_loop, phase=1)
            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.enable method with result: 1")
        return 1

    @classmethod
    def disable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.disable method.")
        if cls.flight_loop_id:
            PythonInterface.handler(FrameRateMonitor.disable)
            PythonInterface.handler(GHD.disable)

            if cls.airstairs_flight_loop_id:
                xp.destroyFlightLoop(cls.airstairs_flight_loop_id)
                cls.airstairs_flight_loop_id = None
            xp.destroyFlightLoop(cls.flight_loop_id)
            cls.flight_loop_id = None
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.disable method.")

    @classmethod
    def reload(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.reload method.")
        cls.disable()
        cls.enable()
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.reload method.")

    @classmethod
    def airstairs_flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.airstairs_flight_loop_callback method.")
        xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.airstairs_flight_loop_callback method.")
        return 0

    @classmethod
    def call_service_crew(cls, name):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering AcfMonitor.call_service_crew method with name: {name}")
        if cls.beacon_on:
            if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.call_service_crew method because beacon is on.")
            return
        if not cls.has_chocks:
            xp.commandOnce(Aircraft.chocks_command_dataref)
        if name in {STAIRWAY_FWD, BUS, VAN}:
            if cls.near_jetway:
                if name == STAIRWAY_FWD and not xp.getDatai(cls.xp_jetway_connected_dataref):
                    xp.commandOnce(cls.toggle_jetway_command_dataref)
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.call_service_crew method because near jetway.")
                return
            if name == STAIRWAY_FWD and cls.has_builtin_stairs:
                if not cls.using_builtin_stairs:
                    xp.scheduleFlightLoop(cls.airstairs_flight_loop_id, interval=1)
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.call_service_crew method because using built-in stairs.")
                return
        GHD.select(name)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.call_service_crew method.")

    @classmethod
    def remove_service_crew(cls, name):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering AcfMonitor.remove_service_crew method with name: {name}")
        if name in {STAIRWAY_FWD, BUS, VAN}:
            if cls.near_jetway:
                if name == STAIRWAY_FWD and xp.getDatai(cls.xp_jetway_connected_dataref):
                    xp.commandOnce(cls.toggle_jetway_command_dataref)
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.remove_service_crew method because near jetway.")
                return
            elif name == STAIRWAY_FWD and cls.has_builtin_stairs:
                if cls.using_builtin_stairs:
                    xp.scheduleFlightLoop(cls.airstairs_flight_loop_id, interval=1)
                cls.remove_service_crew(GHD.ghd_dependencies[name])
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.remove_service_crew method because using built-in stairs.")
                return
        if name in GHD.ghd_dependencies.values():
            other_dependents_name = [key for key, value in GHD.ghd_dependencies.items() if value == name]
            other_dependents_state = [xp.getDatai(GHD.ghd_datarefs[name]) for name in other_dependents_name]
            if name == BUS:
                if other_dependents_state.count(1) == 1 and cls.using_builtin_stairs:
                    if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.remove_service_crew method because using built-in stairs.")
                    return
            elif other_dependents_state.count(1) > 1:
                if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.remove_service_crew method because other dependents are active.")
                return
        GHD.remove(name)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.remove_service_crew method.")

    @classmethod
    def start_loading(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.start_loading method.")
        cls.loading = True
        if not cls.auto_flight_state and not cls.automated_door_control:
            if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.start_loading method because auto flight state and automated door control are both disabled.")
            return
        door_open_commands = getattr(Aircraft, "door_open_command_datarefs", None)
        if cls.automated_door_control and door_open_commands:
            if cls.has_builtin_stairs and cls.using_builtin_stairs:
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
                xp.commandOnce(door_open_commands[FWD_ENTRY])
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
            else:
                xp.commandOnce(door_open_commands[FWD_ENTRY])
            xp.commandOnce(door_open_commands[FWD_SERVICE])
            xp.commandOnce(door_open_commands[AFT_SERVICE])
            xp.commandOnce(door_open_commands[FWD_CARGO])
            xp.commandOnce(door_open_commands[AFT_CARGO])
            if not cls.near_jetway:
                xp.commandOnce(door_open_commands[AFT_ENTRY])
            cls.check_doors()
        else:
            cls.call_service_crew(STAIRWAY_FWD)
            cls.call_service_crew(STAIRWAY_AFT)
            cls.call_service_crew(CATERING_FWD)
            cls.call_service_crew(CATERING_AFT)
            cls.call_service_crew(CARGO_BELT_FWD)
            cls.call_service_crew(CARGO_BELT_AFT)
        cls.remove_service_crew(BUS)
        cls.call_service_crew(VAN)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.start_loading method.")

    @classmethod
    def stop_loading(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.stop_loading method.")
        cls.loading = False
        door_close_commands = getattr(Aircraft, "door_close_command_datarefs", None)
        if cls.automated_door_control and door_close_commands:
            xp.commandOnce(door_close_commands[FWD_SERVICE])
            xp.commandOnce(door_close_commands[AFT_SERVICE])
            xp.commandOnce(door_close_commands[FWD_CARGO])
            xp.commandOnce(door_close_commands[AFT_CARGO])
            cls.check_doors()
        cls.remove_service_crew(VAN)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.stop_loading method.")

    @classmethod
    def start_boarding(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.start_boarding method.")
        cls.boarding = 1
        if not cls.auto_flight_state and not cls.automated_door_control:
            if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.start_boarding method because auto flight state and automated door control are both disabled.")
            return
        door_open_commands = getattr(Aircraft, "door_open_command_datarefs", None)
        if cls.automated_door_control and door_open_commands:
            if cls.has_builtin_stairs and cls.using_builtin_stairs:
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
                xp.commandOnce(door_open_commands[FWD_ENTRY])
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
            else:
                xp.commandOnce(door_open_commands[FWD_ENTRY])
            if not cls.near_jetway:
                xp.commandOnce(door_open_commands[AFT_ENTRY])
            cls.check_doors()
        else:
            cls.call_service_crew(STAIRWAY_FWD)
            cls.call_service_crew(STAIRWAY_AFT)
        cls.call_service_crew(BUS)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.start_boarding method.")

    @classmethod
    def complete_boarding(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.complete_boarding method.")
        cls.boarding = 2
        door_close_commands = getattr(Aircraft, "door_close_command_datarefs", None)
        if cls.automated_door_control and door_close_commands:
            if cls.has_builtin_stairs and cls.using_builtin_stairs:
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
                xp.commandOnce(door_close_commands[FWD_ENTRY])
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
            else:
                xp.commandOnce(door_close_commands[FWD_ENTRY])
            xp.commandOnce(door_close_commands[AFT_ENTRY])
            cls.check_doors()
        cls.remove_service_crew(BUS)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.complete_boarding method.")

    @classmethod
    def start_unloading(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.start_unloading method.")
        cls.after_land = False
        if not cls.auto_flight_state and not cls.automated_door_control:
            if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.start_unloading method because auto flight state and automated door control are both disabled.")
            return
        if DEBUG: xp.sys_log("[DEBUG] Started unloading.")
        door_open_commands = getattr(Aircraft, "door_open_command_datarefs", None)
        if cls.automated_door_control and door_open_commands:
            if cls.has_builtin_stairs and cls.using_builtin_stairs:
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
                xp.commandOnce(door_open_commands[FWD_ENTRY])
                xp.commandOnce(Aircraft.airstairs_toggle_command_dataref)
            else:
                xp.commandOnce(door_open_commands[FWD_ENTRY])
            xp.commandOnce(door_open_commands[FWD_CARGO])
            xp.commandOnce(door_open_commands[AFT_CARGO])
            if not cls.near_jetway:
                xp.commandOnce(door_open_commands[AFT_ENTRY])
            cls.check_doors()
        else:
            cls.call_service_crew(STAIRWAY_FWD)
            cls.call_service_crew(STAIRWAY_AFT)
            cls.call_service_crew(CARGO_BELT_FWD)
            cls.call_service_crew(CARGO_BELT_AFT)
        cls.call_service_crew(BUS)
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.start_unloading method.")

    @classmethod
    def check_doors(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.check_doors method.")
        sim_doors_data = {}
        for door, dataref in dict(getattr(Aircraft, "door_datarefs")).items():
            data = xp.getDataf(dataref)
            sim_doors_data[door] = data
        for door, door_status in sim_doors_data.items():
            door_in_cache = door in cls.sim_doors_data_cache
            cached = door_in_cache and door_status == cls.sim_doors_data_cache[door]
            is_relevant_door_status = not door_in_cache or any(value in [Aircraft.door_open_value, Aircraft.door_closed_value] for value in [cls.sim_doors_data_cache[door], door_status])
            if not cached and is_relevant_door_status:
                if not (cls.near_jetway and GHD.ghd_by_door[door] == STAIRWAY_FWD and cls.auto_flight_state not in {0, 3}):
                    cls.sim_doors_data_cache[door] = door_status
                    if door_status == Aircraft.door_closed_value:
                        cls.remove_service_crew(GHD.ghd_by_door[door])
                    else:
                        cls.call_service_crew(GHD.ghd_by_door[door])
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.check_doors method.")

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        if DEBUG: xp.sys_log("[DEBUG] Entering AcfMonitor.flight_loop_callback method.")
        # Await initialization of jetway_distance_dataref by zibomod
        if counter < 100 and (xp.getDataf(Aircraft.jetway_distance_dataref) == 0.0 or xp.getDataf(Aircraft.jetway_distance_dataref) == 999.0):
            if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.flight_loop_callback method because jetway_distance_dataref is not initialized.")
            return 1

        if cls.on_ground:
            if not cls.engines_running:
                if not GHD.is_enabled:
                    if not PythonInterface.handler(GHD.enable):
                        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.flight_loop_callback method because GHD enable failed.")
                        return 0
                
                cls.check_doors()
                if cls.after_land and not cls.beacon_on:
                    cls.start_unloading()
                if not cls.loading and cls.requested_service_crew and not cls.beacon_on:
                    cls.start_loading()
                elif cls.loading and not cls.requested_service_crew:
                    cls.stop_loading()
                if not cls.boarding and cls.started_flight_leg and not cls.beacon_on:
                    cls.start_boarding()
                if cls.boarding == 1 and not cls.pax_onboard:
                    cls.complete_boarding()
                PythonInterface.flight_loop_interval = -1 * FrameRateMonitor.frame_rate / 2 # 2x Real-time
            else:
                PythonInterface.handler(FrameRateMonitor.disable)
                PythonInterface.flight_loop_interval = 2 # seconds
        else:
            if not cls.after_land:
                cls.after_land = True
            PythonInterface.handler(GHD.disable)
            PythonInterface.flight_loop_interval = 30 # seconds
        if DEBUG: xp.sys_log("[DEBUG] Exiting AcfMonitor.flight_loop_callback method.")
        return PythonInterface.flight_loop_interval

    flight_loop = flight_loop_callback
    flight_loop_id = None

    airstairs_flight_loop = airstairs_flight_loop_callback
    airstairs_flight_loop_id = None

    gear_on_ground_dataref = xp.findDataRef("sim/flightmodel2/gear/on_ground")
    engines_is_burning_fuel_dataref = xp.findDataRef("sim/flightmodel2/engines/engine_is_burning_fuel")
    toggle_jetway_command_dataref = xp.findCommand("sim/ground_ops/jetway")


class Menu:
    id = None

    @classproperty
    def is_enabled(cls) -> bool:
        # if DEBUG: xp.sys_log("[DEBUG] Entering Menu.is_enabled method.")
        result = xp.checkMenuItemState(cls.id, 0) == 2
        # if DEBUG: xp.sys_log(f"[DEBUG] Exiting Menu.is_enabled method with result: {result}")
        return result

    @classmethod
    def create(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Menu.create method.")
        cls.id = xp.createMenu("AutoGHDforZibo", handler=cls.callback)
        xp.appendMenuItem(cls.id, "Enabled", "enabled")
        xp.appendMenuSeparator(cls.id)
        xp.appendMenuItem(cls.id, "Automated Door Control", SETTING_AUTOMATED_DOOR_CONTROL)

        xp.checkMenuItem(cls.id, 0, xp.Menu_Unchecked)
        xp.checkMenuItem(cls.id, 2, xp.Menu_Unchecked)
        if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.create method.")
        return cls.id

    @classmethod
    def destroy(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Menu.destroy method.")
        if cls.id:
            xp.destroyMenu(cls.id)
        if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.destroy method.")

    @classmethod
    def enable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Menu.enable method.")
        if cls.id is None:
            xp.sys_log("[ERROR] Unable to create plugin's menu.")
            if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.enable method with result: 0")
            return 0

        for attr_name, attr_value in vars(AcfSelector).items():
            if attr_name.endswith("_dataref") and not callable(attr_value):
                if attr_value is None:
                    xp.sys_log(f"[ERROR] Unable to find {attr_name} dataref.")
                    if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.enable method with result: 0")
                    return 0

        for attr_name, attr_value in vars(AcfMonitor).items():
            if attr_name.endswith("_dataref") and not callable(attr_value):
                if attr_value is None:
                    xp.sys_log(f"[ERROR] Unable to find {attr_name} dataref.")
                    if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.enable method with result: 0")
                    return 0

        if GHD.plugin_id == xp.NO_PLUGIN_ID:
            xp.sys_log("[ERROR] Unable to find JarDesign's Ground Handling Deluxe (GHD).")
            if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.enable method with result: 0")
            return 0

        for attr_name, attr_value in vars(GHD).items():
            if attr_name.endswith("_dataref") and not callable(attr_value):
                if attr_value is None:
                    xp.sys_log(f"[ERROR] Unable to find {attr_name} dataref from JarDesign's Ground Handling Deluxe (GHD).")
                    if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.enable method with result: 0")
                    return 0

        AcfSelector.enable()
        xp.checkMenuItem(cls.id, 0, xp.Menu_Checked)
        if Config.get(f".settings.{SETTING_AUTOMATED_DOOR_CONTROL}") == True:
            xp.checkMenuItem(cls.id, 2, xp.Menu_Checked)
        if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.enable method with result: 1")
        return 1

    @classmethod
    def disable(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Menu.disable method.")
        AcfMonitor.disable()
        AcfSelector.disable()
        FrameRateMonitor.disable()

        xp.checkMenuItem(cls.id, 0, xp.Menu_Unchecked)
        if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.disable method.")
        
    @classmethod
    def reload(cls):
        if DEBUG: xp.sys_log("[DEBUG] Entering Menu.reload method.")
        cls.disable()
        cls.enable()
        if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.reload method.")

    @classmethod
    def callback(cls, menuRefCon, itemRefCon):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering Menu.callback method with menuRefCon: {menuRefCon}, itemRefCon: {itemRefCon}")
        if itemRefCon == "enabled" and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Checked:
            cls.disable()
        elif itemRefCon == "enabled" and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Unchecked:
            cls.enable()
        if itemRefCon == SETTING_AUTOMATED_DOOR_CONTROL and xp.checkMenuItemState(cls.id, 2) == xp.Menu_Checked:
            Config.set(f".settings.{SETTING_AUTOMATED_DOOR_CONTROL}", False)
            AcfMonitor.automated_door_control = Config.get(f".settings.{SETTING_AUTOMATED_DOOR_CONTROL}")
            if AcfMonitor.automated_door_control == False:
                xp.checkMenuItem(cls.id, 2, xp.Menu_Unchecked)
        elif itemRefCon == SETTING_AUTOMATED_DOOR_CONTROL and xp.checkMenuItemState(cls.id, 2) == xp.Menu_Unchecked:
            Config.set(f".settings.{SETTING_AUTOMATED_DOOR_CONTROL}", True)
            AcfMonitor.automated_door_control = Config.get(f".settings.{SETTING_AUTOMATED_DOOR_CONTROL}")
            if AcfMonitor.automated_door_control == True:
                xp.checkMenuItem(cls.id, 2, xp.Menu_Checked)
            AcfMonitor.reset_cache()
        if DEBUG: xp.sys_log("[DEBUG] Exiting Menu.callback method.")


class PythonInterface:
    xp_jetway_connected = 0

    @staticmethod
    def handler(func, *args):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.handler method.")
        result = func(*args)
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.handler method.")
        return result

    def monitor_jetway_handler(self, commandRef, phase, refCon):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.monitor_jetway_handler method.")
        if xp.getDatai(self.xp_jetway_connected_accessor) == 1:
            xp.setDatai(self.xp_jetway_connected_accessor, 0)
        else:
            xp.setDatai(self.xp_jetway_connected_accessor, 1)
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.monitor_jetway_handler method.")
        return 1
    
    def read_xp_jetway_connected(self, read_ref_con):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.read_xp_jetway_connected method.")
        result = self.xp_jetway_connected
        if DEBUG: xp.sys_log(f"[DEBUG] Exiting PythonInterface.read_xp_jetway_connected method with result: {result}")
        return result

    def write_xp_jetway_connected(self, write_ref_con, value):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering PythonInterface.write_xp_jetway_connected method with value: {value}")
        if value in [0, 1]:
            self.xp_jetway_connected = value
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.write_xp_jetway_connected method.")

    def __init__(self):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.__init__ method.")
        self.Name = "AutoGHDforZibo"
        self.Sig = "autoghdforzibo.xppython3"
        self.Desc = "Plugin to handle GHD automatically for Zibomod B737"

        self.xp_jetway_connected_accessor = None
        self.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.__init__ method.")

    def XPluginStart(self):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.XPluginStart method.")
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings
        
        xp.registerCommandHandler(
            AcfMonitor.toggle_jetway_command_dataref,
            self.monitor_jetway_handler,
            before=0
        )
        self.xp_jetway_connected_accessor = xp.registerDataAccessor(
                    XP_JETWAY_CONNECTED_DATAREF_NAME, 
                    readInt=self.read_xp_jetway_connected,
                    writeInt=self.write_xp_jetway_connected,
                    readRefCon=0
                )
        setattr(AcfMonitor, "xp_jetway_connected_dataref", xp.findDataRef(XP_JETWAY_CONNECTED_DATAREF_NAME))
        Menu.create()
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.XPluginStart method.")
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.XPluginStop method.")
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored

        xp.unregisterCommandHandler(
            AcfMonitor.toggle_jetway_command_dataref,
            self.monitor_jetway_handler,
            before=0
        )
        xp.unregisterDataAccessor(self.xp_jetway_connected_accessor)
        self.xp_jetway_connected_accessor = None
        delattr(AcfMonitor, "xp_jetway_connected_dataref")
        Menu.destroy()
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.XPluginStop method.")

    def XPluginEnable(self):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.XPluginEnable method.")
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.

        result = 1 if Config.load() and Menu.enable() else 0
        if DEBUG: xp.sys_log(f"[DEBUG] Exiting PythonInterface.XPluginEnable method with result: {result}")
        return result

    def XPluginDisable(self):
        if DEBUG: xp.sys_log("[DEBUG] Entering PythonInterface.XPluginDisable method.")
        # Called once by X-Plane, when plugin is requested to be disabled. All plugins
        # are disabled prior to Stop.
        # Return is ignored

        Config.unload()
        Menu.disable()
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.XPluginDisable method.")

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        if DEBUG: xp.sys_log(f"[DEBUG] Entering PythonInterface.XPluginReceiveMessage method with inFromWho: {inFromWho}, inMessage: {inMessage}, inParam: {inParam}")
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
        if DEBUG: xp.sys_log("[DEBUG] Exiting PythonInterface.XPluginReceiveMessage method.")