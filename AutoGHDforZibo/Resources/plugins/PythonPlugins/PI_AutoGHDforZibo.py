################################################################################
#                                                                              #
#    PI_AutoGHDforZibo.py                            #####     ####            #
#                                                    ##   ##   ##   ##         #
#    By: Bruno Costa <support@bybrunocosta.com>      ##  ##    ##              #
#                                                    ##   ##   ##              #
#    Created: 2024-03-15T22:08:48.801Z               ##   ##   ##   ##         #
#    Updated: 2024-05-20T14:14:26.624Z               #####     ####            #
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
        Aircraft.ghd_set_name = "Boeing737-800X.set"
        Aircraft.door_open_value = 1 # Door open value
        Aircraft.door_closed_value = 0 # Door closed value

        # Dataref containing int representing airside services state
        Aircraft.auto_flight = xp.findDataRef("laminar/B738/tab/auto_flight")

        # Datarefs containing door status
        Aircraft.door_dataref["FWD ENTRY"] = xp.findDataRef("737u/doors/L1")
        Aircraft.door_dataref["AFT ENTRY"] = xp.findDataRef("737u/doors/L2")
        Aircraft.door_dataref["FWD SERVICE"] = xp.findDataRef("737u/doors/R1")
        Aircraft.door_dataref["AFT SERVICE"] = xp.findDataRef("737u/doors/R2")
        Aircraft.door_dataref["FWD CARGO"] = xp.findDataRef("737u/doors/Fwd_Cargo")
        Aircraft.door_dataref["AFT CARGO"] = xp.findDataRef("737u/doors/aft_Cargo")

        # Dataref containing bool, if aircraft is using own stairs
        Aircraft.not_airstairs_dataref = xp.findDataRef("laminar/B738/not_airstairs")

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
        Aircraft.chocks_command = xp.findCommand("laminar/B738/toggle_switch/chock")

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
    door_dataref = {}
    door_open_value = 0
    door_closed_value = 0

    ghd_set_name = None
    auto_flight = None
    not_airstairs_dataref = None
    loading_dataref = None
    boarding_dataref = None
    pax_board_dataref = None
    beacon_dataref = None
    chocks_dataref = None
    chocks_command = None
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

VERSION = "v1.3.1"
DOOR_CLOSED = 0
DOOR_OPEN = 1
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

SETTING_SERVICE_DOOR_OPEN = "call_service_on_door_open"
XP_JETWAY_CONNECTED_DATAREF_NAME = "xptk/ghd/jetway_connected"


import json
import warnings
import xp, os, configparser


class classproperty(property):

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class Config:

    @classmethod
    def save(cls):
        config = {}
        for attr_name, attr_value in vars(cls).items():
            is_function = callable(attr_value) or isinstance(attr_value, classmethod)
            is_default_attr = attr_name == "prf_file_path" or attr_name.startswith("__")
            if not is_function and not is_default_attr:
                config[attr_name] = attr_value

        with open(cls.prf_file_path, "w", encoding="utf-8") as file:
            json.dump(config, file)

    @classmethod
    def create(cls):
        xp.sys_log(f"[INFO] Initializing configuration file.\nPath: {cls.prf_file_path}.")
        setattr(
                cls,
                "settings",
                {
                    SETTING_SERVICE_DOOR_OPEN: True
                }
            )
        cls.save()
        cls.unload()

    @classmethod
    def load(cls):
        # Here for backwards compatibility
        def deprecated_retrieve():
            warnings.warn("This function is deprecated and will be removed in the future.", DeprecationWarning)
            deprecated_config = configparser.ConfigParser()
            deprecated_config.read(deprecated_file_path)
            deprecated_sections = deprecated_config.sections()
            for deprecated_section in deprecated_sections:
                deprecated_options = deprecated_config.options(deprecated_section)
                for deprecated_option in deprecated_options:
                    if deprecated_option == "services on door open":
                        # option = deprecated_config.get(deprecated_section, deprecated_option)
                        setattr(
                            cls,
                            "settings",
                            {
                                # SETTING_SERVICE_DOOR_OPEN: False if option == "False" else True
                                SETTING_SERVICE_DOOR_OPEN: True
                            }
                        )
            cls.save()
            cls.unload()

        if not os.path.exists(cls.prf_file_path):
            deprecated_file_path = os.path.join(xp.getSystemPath(), "Resources", "plugins", "PythonPlugins", "AutoGHDforZibo.ini")
            if os.path.exists(deprecated_file_path):
                deprecated_retrieve()
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
        return 1

    @classmethod
    def unload(cls):
        attr_list = []
        for attr_name, attr_value in vars(cls).items():
            is_function = callable(attr_value) or isinstance(attr_value, classmethod)
            is_default_attr = attr_name == "prf_file_path" or attr_name.startswith("__")
            if not is_function and not is_default_attr:
                attr_list.append(attr_name)
        for attr_name in attr_list:
            delattr(cls, attr_name)

    @classmethod
    def reload(cls):
        cls.unload()
        cls.load()

    @classmethod
    def get(cls, path: str):
        obj = cls
        try:
            route = path.split(".")[1:]
            if len(route) == 1:
                return getattr(obj, route[-1])
            else:
                for item in route[:-1]:
                    obj = getattr(obj, item)
                return obj.get(route[-1], None)
        except AttributeError:
            return None

    @classmethod
    def set(cls, path: str, value):
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
        except AttributeError:
            pass

    prf_file_path = os.path.join(os.path.dirname(xp.getPrefsPath()), "AutoGHDforZibo.prf")


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


class GHD:

    @classproperty
    def is_enabled(cls) -> bool:
        return xp.getDatai(GHD.drf_control_dataref)

    @classmethod
    def set_dataref_from_set(cls, index, value, z_coordinate):
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

    @classmethod
    def get_set(cls):
        ghd_path = os.path.dirname(xp.getPluginInfo(cls.plugin_id).filePath)
        set_path = ghd_path + "/Sets/Default/" + Aircraft.ghd_set_name
        if os.path.exists(ghd_path + "/Sets/Custom/" + Aircraft.ghd_set_name):
            set_path = ghd_path + "/Sets/Custom/" + Aircraft.ghd_set_name
        elif not os.path.exists(set_path):
            xp.sys_log(f"[ERROR] Failed to locate a suitable configuration set for '{Aircraft.configuration_name}' within JarDesign's Ground Handling Deluxe (GHD).")
            PythonInterface.handler(Menu.disable)
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
            return 0

        xp.sys_log("[INFO] Loaded JarDesign's Ground Handling Deluxe (GHD) configuration set.")
        return 1

    @classmethod
    def reset_data(cls):
        for key in cls.ghd_datarefs.keys():
            cls.ghd_datarefs[key] = None

    @classmethod
    def enable(cls):
        if not xp.isPluginEnabled(cls.plugin_id):
            xp.sys_log("[ERROR] JarDesign's Ground Handling Deluxe (GHD) is disabled.")
            PythonInterface.handler(Menu.disable)
            return 0

        PythonInterface.handler(FrameRateMonitor.enable)
        cls.reset_data()

        if not cls.get_set():
            return 0

        xp.setDatai(GHD.drf_control_dataref, 1)
        xp.setDatai(GHD.execute_dataref, 1)
        return 1

    @classmethod
    def disable(cls):
        xp.setDatai(GHD.drf_control_dataref, 0)
        xp.setDatai(GHD.execute_dataref, 0)

    @classmethod
    def select(cls, name):
        if cls.ghd_datarefs[name] is None:
            return
        if name in cls.ghd_dependencies:
            PythonInterface.handler(AcfMonitor.call_service_crew, cls.ghd_dependencies[name])
        xp.setDatai(cls.ghd_datarefs[name], 1)
        cls.execute()

    @classmethod
    def remove(cls, name):
        if cls.ghd_datarefs[name] is None:
            return
        if name in cls.ghd_dependencies:
            PythonInterface.handler(AcfMonitor.remove_service_crew, cls.ghd_dependencies[name])
        xp.setDatai(cls.ghd_datarefs[name], 0)
        cls.execute()

    @classmethod
    def execute(cls):
        xp.setDatai(GHD.drf_control_dataref, 1)
        xp.setDatai(GHD.execute_dataref, 1)

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
        STAIRWAY_FWD: BUS,
        STAIRWAY_AFT: BUS,
        CARGO_BELT_FWD: BAGGAGE_FWD,
        CARGO_BELT_AFT: BAGGAGE_AFT
    }

    ghd_by_door = {
        "FWD ENTRY": STAIRWAY_FWD,
        "AFT ENTRY": STAIRWAY_AFT,
        "FWD SERVICE": CATERING_FWD,
        "AFT SERVICE": CATERING_AFT,
        "FWD CARGO": CARGO_BELT_FWD,
        "AFT CARGO": CARGO_BELT_AFT
    }


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

        xp.sys_log(f"[INFO] Trying to retrieve configuration for '{acf_icao}'.")
        is_supported_addon_acf = acf_icao in Aircraft.supported_acf and \
                                    Aircraft.supported_acf[acf_icao](acf_dir)
        if is_supported_addon_acf:
            for door, dataref in Aircraft.door_dataref.items():
                if not dataref:
                    setattr(Aircraft, "invalid_dataref", True)
                    xp.sys_log(f"[WARNING] Unable to find {door} door's dataref for {Aircraft.configuration_name}.")

            for attr_name, attr_value in vars(Aircraft).items():
                if attr_name.endswith("_dataref") and not callable(attr_value):
                    if attr_value is None:
                        setattr(Aircraft, "invalid_dataref", True)
                        xp.sys_log(f"[WARNING] Unable to find {attr_name} dataref for {Aircraft.configuration_name}.")

            if not hasattr(Aircraft, "invalid_dataref"):
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
                xp.sys_log(f"[WARNING] Unable to retrieve '{acf_icao}' configuration. " + \
                    "Will try again in 5 seconds.")
                PythonInterface.flight_loop_interval = 5 # seconds
                return PythonInterface.flight_loop_interval

            xp.sys_log(f"[ERROR] A valid configuration for '{acf_icao}' was not found. " + \
                "Ensure you're using a supported aircraft.")
            PythonInterface.handler(Menu.disable)
        else:
            PythonInterface.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL
            PythonInterface.handler(AcfMonitor.enable)
        return 0

    flight_loop = flight_loop_callback
    flight_loop_id = None

    acf_icao_dataref = xp.findDataRef("sim/aircraft/view/acf_ICAO")


class AcfMonitor:
    service_door_open = False
    after_land = False
    loading = False
    boarding = 0
    auto_flight_state_cache = 0
    sim_doors_data_cache = {}

    @classproperty
    def engines_running(cls) -> bool:
        values = []
        xp.getDatavi(cls.engines_is_burning_fuel_dataref, values, count=2)
        return any(values)

    @classproperty
    def on_ground(cls) -> bool:
        gear_on_ground_data = []
        xp.getDatavi(cls.gear_on_ground_dataref, gear_on_ground_data, count=3)
        return any(gear_on_ground_data)

    @classproperty
    def has_chocks(cls) -> bool:
        return xp.getDatai(Aircraft.chocks_dataref)

    @classproperty
    def beacon_on(cls) -> bool:
        return xp.getDatai(Aircraft.beacon_dataref)

    @classproperty
    def auto_flight_state(cls) -> bool:
        return xp.getDatai(Aircraft.auto_flight)

    @classproperty
    def has_builtin_stairs(cls) -> bool:
        return not xp.getDatai(Aircraft.not_airstairs_dataref)

    @classproperty
    def requested_service_crew(cls) -> bool:
        return xp.getDatai(Aircraft.loading_dataref)

    @classproperty
    def started_flight_leg(cls) -> bool:
        return xp.getDatai(Aircraft.boarding_dataref)

    @classproperty
    def pax_onboard(cls) -> bool:
        return xp.getDatai(Aircraft.pax_board_dataref)

    @classproperty
    def near_jetway(cls) -> bool:
        return xp.getDataf(Aircraft.jetway_distance_dataref) <= 0.05

    @classmethod
    def reset_cache(cls):
        cls.sim_doors_data_cache = {}

    @classmethod
    def reset_data(cls):
        cls.service_door_open = Config.get(f".settings.{SETTING_SERVICE_DOOR_OPEN}")
        xp.setDatai(cls.xp_jetway_connected_dataref, 0)
        cls.after_land = False
        cls.loading = False
        cls.boarding = 0
        cls.auto_flight_state_cache = 0
        cls.reset_cache()

    @classmethod
    def enable(cls):
        if cls.flight_loop_id is None:
            if not PythonInterface.handler(GHD.enable):
                return 0
            cls.reset_data()

            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)
        return 1

    @classmethod
    def disable(cls):
        if cls.flight_loop_id:
            PythonInterface.handler(FrameRateMonitor.disable)
            PythonInterface.handler(GHD.disable)

            xp.destroyFlightLoop(cls.flight_loop_id)
            cls.flight_loop_id = None

    @classmethod
    def reload(cls):
        cls.disable()
        cls.enable()

    @classmethod
    def call_service_crew(cls, name):
        if cls.beacon_on:
            return
        if name in {STAIRWAY_FWD, BUS, VAN}:
            if cls.near_jetway:
                if name == STAIRWAY_FWD and not xp.getDatai(cls.xp_jetway_connected_dataref):
                    xp.sys_log(f"[INFO] Toggled jetway when calling for {name}.")
                    xp.commandOnce(cls.toggle_jetway_command)
                    xp.setDatai(cls.xp_jetway_connected_dataref, 1)
                return
            if name == STAIRWAY_FWD and cls.has_builtin_stairs:
                cls.call_service_crew(GHD.ghd_dependencies[name])
                return
        if not cls.has_chocks:
            xp.commandOnce(Aircraft.chocks_command)
        GHD.select(name)


    @classmethod
    def remove_service_crew(cls, name):
        if name in {STAIRWAY_FWD, BUS, VAN}:
            if cls.near_jetway:
                if name == STAIRWAY_FWD and xp.getDatai(cls.xp_jetway_connected_dataref):
                    xp.sys_log(f"[INFO] Toggled jetway when removing {name}.")
                    xp.commandOnce(cls.toggle_jetway_command)
                    xp.setDatai(cls.xp_jetway_connected_dataref, 0)
                return
            if name == STAIRWAY_FWD and cls.has_builtin_stairs:
                cls.remove_service_crew(GHD.ghd_dependencies[name])
                return
        GHD.remove(name)

    @classmethod
    def start_loading(cls):
        cls.call_service_crew(CATERING_FWD)
        cls.call_service_crew(CATERING_AFT)
        cls.call_service_crew(CARGO_BELT_FWD)
        cls.call_service_crew(CARGO_BELT_AFT)
        cls.call_service_crew(STAIRWAY_FWD)
        cls.call_service_crew(VAN)
        if not cls.near_jetway:
            cls.call_service_crew(STAIRWAY_AFT)
            cls.remove_service_crew(BUS)
        cls.loading = True

    @classmethod
    def start_boarding(cls):
        cls.loading = False
        cls.call_service_crew(STAIRWAY_FWD)
        cls.remove_service_crew(VAN)
        if not cls.near_jetway:
            cls.call_service_crew(STAIRWAY_AFT)
        cls.boarding = 1

    @classmethod
    def start_unloading(cls):
        cls.call_service_crew(CARGO_BELT_FWD)
        cls.call_service_crew(CARGO_BELT_AFT)

        cls.call_service_crew(STAIRWAY_FWD)
        if not cls.near_jetway:
            cls.call_service_crew(STAIRWAY_AFT)
        cls.after_land = False

    @classmethod
    def check_auto_flight_state(cls):
        auto_flight_state = cls.auto_flight_state
        cached = auto_flight_state == cls.auto_flight_state_cache
        if not cached:
            if cls.auto_flight_state_cache == 1 and auto_flight_state == 2:
                cls.auto_flight_state_cache = auto_flight_state
                return
            cls.auto_flight_state_cache = auto_flight_state
            if auto_flight_state in {1, 2, 3, 4}:
                if xp.getDatai(cls.xp_jetway_connected_dataref) == 1:
                    xp.setDatai(cls.xp_jetway_connected_dataref, 0)
                else:
                    xp.setDatai(cls.xp_jetway_connected_dataref, 1)

    @classmethod
    def check_doors(cls):
        sim_doors_data = {}
        for door, dataref in Aircraft.door_dataref.items():
            data = xp.getDataf(dataref)
            sim_doors_data[door] = data
        for door, door_status in sim_doors_data.items():
            cached = door in cls.sim_doors_data_cache and door_status == cls.sim_doors_data_cache[door]
            if not cached:
                if not (cls.near_jetway and GHD.ghd_by_door[door] == STAIRWAY_FWD and cls.auto_flight_state not in {0, 3}):
                    cls.sim_doors_data_cache[door] = door_status
                    if door_status == Aircraft.door_closed_value:
                        cls.remove_service_crew(GHD.ghd_by_door[door])
                    elif cls.service_door_open:
                        cls.call_service_crew(GHD.ghd_by_door[door])

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        if cls.on_ground:
            if not cls.engines_running:
                if GHD.is_enabled and cls.beacon_on:
                    PythonInterface.handler(GHD.disable)
                if GHD.is_enabled:
                    cls.check_auto_flight_state()
                    cls.check_doors()
                    if cls.after_land:
                        cls.start_unloading()
                    if not cls.loading and cls.requested_service_crew:
                        cls.start_loading()
                    if not cls.boarding and cls.started_flight_leg:
                        cls.start_boarding()
                    if cls.boarding == 1 and not cls.pax_onboard:
                        cls.remove_service_crew(BUS)
                        cls.boarding == 2
                elif not cls.beacon_on:
                    if not PythonInterface.handler(GHD.enable):
                        return 0
                PythonInterface.flight_loop_interval = -1 * FrameRateMonitor.frame_rate / 2 # 2x Real-time
            else:
                PythonInterface.handler(FrameRateMonitor.disable)
                PythonInterface.flight_loop_interval = 2 # seconds
        else:
            if not cls.after_land:
                cls.after_land = True
            PythonInterface.handler(FrameRateMonitor.disable)
            PythonInterface.flight_loop_interval = 30 # seconds
        return PythonInterface.flight_loop_interval

    flight_loop = flight_loop_callback
    flight_loop_id = None

    gear_on_ground_dataref = xp.findDataRef("sim/flightmodel2/gear/on_ground")
    engines_is_burning_fuel_dataref = xp.findDataRef("sim/flightmodel2/engines/engine_is_burning_fuel")
    toggle_jetway_command = xp.findCommand("sim/ground_ops/jetway")


class Menu:
    id = None

    @classproperty
    def is_enabled(cls) -> bool:
        if xp.checkMenuItemState(cls.id, 0) == 2:
            return True
        return False

    @classmethod
    def create(cls):
        cls.id = xp.createMenu("AutoGHDforZibo", handler=cls.callback)
        xp.appendMenuItem(cls.id, " Enabled", "enabled")
        xp.appendMenuSeparator(cls.id)
        xp.appendMenuItem(cls.id, " Service On Door Open", SETTING_SERVICE_DOOR_OPEN)

        xp.checkMenuItem(cls.id, 0, xp.Menu_Checked)
        if Config.get(f".settings.{SETTING_SERVICE_DOOR_OPEN}") == False:
            xp.checkMenuItem(cls.id, 2, xp.Menu_Unchecked)
        else:
            xp.checkMenuItem(cls.id, 2, xp.Menu_Checked)
        return cls.id

    @classmethod
    def destroy(cls):
        if cls.id:
            xp.destroyMenu(cls.id)

    @classmethod
    def enable(cls):
        if cls.id is None:
            xp.sys_log("[ERROR] Unable to create plugin's menu.")
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

        if GHD.plugin_id == xp.NO_PLUGIN_ID:
            xp.sys_log("[ERROR] Unable to find JarDesign's Ground Handling Deluxe (GHD).")
            return 0

        for attr_name, attr_value in vars(GHD).items():
            if attr_name.endswith("_dataref") and not callable(attr_value):
                if attr_value is None:
                    xp.sys_log(f"[ERROR] Unable to find {attr_name} dataref from JarDesign's Ground Handling Deluxe (GHD).")
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
    def callback(cls, menuRefCon, itemRefCon):
        if itemRefCon == "enabled" and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Checked:
            cls.disable()
        elif itemRefCon == "enabled" and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Unchecked:
            cls.enable()
        if itemRefCon == SETTING_SERVICE_DOOR_OPEN and xp.checkMenuItemState(cls.id, 2) == xp.Menu_Checked:
            Config.set(f".settings.{SETTING_SERVICE_DOOR_OPEN}", False)
            AcfMonitor.service_door_open = Config.get(f".settings.{SETTING_SERVICE_DOOR_OPEN}")
            xp.checkMenuItem(cls.id, 2, xp.Menu_Unchecked)
        elif itemRefCon == SETTING_SERVICE_DOOR_OPEN and xp.checkMenuItemState(cls.id, 2) == xp.Menu_Unchecked:
            Config.set(f".settings.{SETTING_SERVICE_DOOR_OPEN}", True)
            AcfMonitor.service_door_open = Config.get(f".settings.{SETTING_SERVICE_DOOR_OPEN}")
            AcfMonitor.reset_cache()
            xp.checkMenuItem(cls.id, 2, xp.Menu_Checked)


class PythonInterface:
    xp_jetway_connected = 0

    @staticmethod
    def handler(func, *args):
        return func(*args)

    def read_xp_jetway_connected(self, read_ref_con):
        return self.xp_jetway_connected

    def write_xp_jetway_connected(self, write_ref_con, value):
        if value in [0, 1]:
            self.xp_jetway_connected = value

    def __init__(self):
        self.Name = "AutoGHDforZibo"
        self.Sig = "autoghdforzibo.xppython3"
        self.Desc = "Plugin to handle GHD automatically for Zibomod B737"

        self.xp_jetway_connected_accessor = None
        self.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL

    def XPluginStart(self):
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

        self.xp_jetway_connected_accessor = xp.registerDataAccessor(
                    XP_JETWAY_CONNECTED_DATAREF_NAME, 
                    readInt=self.read_xp_jetway_connected,
                    writeInt=self.write_xp_jetway_connected,
                    readRefCon=0
                )
        setattr(AcfMonitor, "xp_jetway_connected_dataref", xp.findDataRef(XP_JETWAY_CONNECTED_DATAREF_NAME))
        Menu.create()
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        # Called once by X-Plane on quit (or when plugins are exiting as part of reload)
        # Return is ignored

        Menu.destroy()

    def XPluginEnable(self):
        # Required by XPPython3
        # Called once by X-Plane, after all plugins have "Started" (including during reload sequence).
        # You need to return an integer 1, if you have successfully enabled, 0 otherwise.

        return 1 if Config.load() and Menu.enable() else 0

    def XPluginDisable(self):
        # Called once by X-Plane, when plugin is requested to be disabled. All plugins
        # are disabled prior to Stop.
        # Return is ignored

        Config.unload()
        Menu.disable()

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        # Called by X-Plane whenever a plugin message is being sent to your
        # plugin. Messages include MSG_PLANE_LOADED, MSG_ENTERED_VR, etc., as
        # described in XPLMPlugin module.
        # Messages may be custom inter-plugin messages, as defined by other plugins.
        # Return is ignored
        if (inMessage == xp.MSG_PLANE_LOADED):
            if Menu.is_enabled:
                AcfSelector.reload()
            else:
                Menu.enable()