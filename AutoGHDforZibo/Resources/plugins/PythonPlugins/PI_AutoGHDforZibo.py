################################################################################
#                                                                              #
#    PI_AutoGHDforZibo.py                            #####     ####            #
#                                                    ##   ##   ##   ##         #
#    By: Bruno Costa <support@bybrunocosta.com>      ##  ##    ##              #
#                                                    ##   ##   ##              #
#    Created: 15/03/2024 22:08:48                    ##   ##   ##   ##         #
#    Updated: 21/03/2024 11:16:48                    #####     ####            #
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
        Aircraft.doors_dataref = xp.findDataRef('laminar/B738/doors/status')

        # Dataref containing bool, if aircraft is using own stairs
        Aircraft.not_airstairs_dataref = xp.findDataRef('laminar/B738/not_airstairs')

        # Dataref containing bool, if aircraft is loading
        Aircraft.loading_dataref = xp.findDataRef('laminar/b738/fmodpack/fmod_play_cargo')

        # Dataref containing bool, if aircraft is boarding
        Aircraft.boarding_dataref = xp.findDataRef('laminar/b738/fmodpack/leg_started')

        # Dataref containing bool, if boarding is complete
        Aircraft.pax_board_dataref = xp.findDataRef('laminar/b738/fmodpack/pax_board')
        
        Aircraft.jetway_distance_dataref = xp.findDataRef("laminar/B738/jetway_nearest")

        Aircraft.beacon_dataref = xp.findDataRef('sim/cockpit/electrical/beacon_lights_on')

        Aircraft.chocks_dataref = xp.findDataRef('laminar/B738/fms/chock_status')
        Aircraft.chocks_command = xp.findCommand('laminar/B738/toggle_switch/chock')

    supported_dir = {
        "B737-800X": b738X
    }

    acf_plugins = {
        "zibomod.by.Zibo": b738X
    }


class Aircraft:
    configuration_name = None
    doors_dataref = None
    not_airstairs_dataref = None
    loading_dataref = None
    boarding_dataref = None
    pax_board_dataref = None
    jetway_distance_dataref = None
    beacon_dataref = None
    chocks_dataref = None
    chocks_command = None
    door_open_value = 0
    door_closed_value = 0

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

VERSION = "v1.0.0"
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
CARGO_BELT_FWD = "Loader(B)-1"
CARGO_BELT_AFT = "Loader(B)-2"
BAGGAGE_FWD = "Baggage-1"
BAGGAGE_AFT = "Baggage-2"

import xp, os


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
    def extract_acf_dir(acf_path):
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
    def enable(cls):
        for _, name in cls.ghd_by_door.items():
            cls.remove(name, False)

        xp.setDatai(GHD.drf_control_dataref, 1)
        xp.setDatai(GHD.execute_dataref, 1)

    @classmethod
    def disable(cls):
        for _, name in cls.ghd_by_door.items():
            cls.remove(name, False)

        xp.setDatai(GHD.drf_control_dataref, 0)
        xp.setDatai(GHD.execute_dataref, 0)

    @classmethod
    def select(cls, name):
        if name in cls.ghd_dependencies:
            cls.select(cls.ghd_dependencies[name])
        xp.sys_log("Drive up " + name)
        xp.setDatai(cls.ghd_datarefs[name], 1)
        cls.execute()

    @classmethod
    def remove(cls, name, msg=True):
        if name in cls.ghd_dependencies:
            cls.remove(cls.ghd_dependencies[name], msg)
        if msg:
            xp.sys_log("Drive away " + name)
        xp.setDatai(cls.ghd_datarefs[name], 0)
        cls.execute()

    @classmethod
    def execute(cls):
        xp.setDatai(GHD.drf_control_dataref, 1)
        xp.setDatai(GHD.execute_dataref, 1)

    plugin_id = xp.findPluginBySignature('jardesign.crew.ground.handling')
    execute_dataref = xp.findDataRef('jd/ghd/execute')
    drf_control_dataref = xp.findDataRef('jd/ghd/drfcontrol')
    catering_fwd_dataref = xp.findDataRef('jd/ghd/select_01')
    catering_aft_dataref = xp.findDataRef('jd/ghd/select_02')
    stairs_fwd_dataref = xp.findDataRef('jd/ghd/select_04')
    stairs_aft_dataref = xp.findDataRef('jd/ghd/select_03')
    bus_dataref = xp.findDataRef('jd/ghd/select_08')
    cargo_belt_fwd_dataref = xp.findDataRef('jd/ghd/select_10')
    cargo_belt_aft_dataref = xp.findDataRef('jd/ghd/select_11')
    cargo_luggage_fwd_dataref = xp.findDataRef('jd/ghd/select_16')
    cargo_luggage_aft_dataref = xp.findDataRef('jd/ghd/select_17')

    ghd_datarefs = {
        CATERING_FWD: catering_fwd_dataref,
        CATERING_AFT: catering_aft_dataref,
        STAIRWAY_FWD: stairs_fwd_dataref,
        STAIRWAY_AFT: stairs_aft_dataref,
        BUS: bus_dataref,
        CARGO_BELT_FWD: cargo_belt_fwd_dataref,
        CARGO_BELT_AFT: cargo_belt_aft_dataref,
        BAGGAGE_FWD: cargo_luggage_fwd_dataref,
        BAGGAGE_AFT: cargo_luggage_aft_dataref
    }
    
    ghd_dependencies = {
        STAIRWAY_FWD: BUS,
        STAIRWAY_AFT: BUS,
        CARGO_BELT_FWD: BAGGAGE_FWD,
        CARGO_BELT_AFT: BAGGAGE_AFT
    }

    ghd_by_door = {
        0: STAIRWAY_FWD,
        1: CATERING_FWD,
        2: CARGO_BELT_FWD,
        3: STAIRWAY_AFT,
        4: CATERING_AFT,
        5: CARGO_BELT_AFT
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
        acf_dir = Utils.extract_acf_dir(acf_path)

        xp.sys_log("Trying to retrieve configuration for " + acf_icao + ".")
        is_supported_addon_acf = acf_icao in Aircraft.supported_acf and \
                                    Aircraft.supported_acf[acf_icao](acf_dir)
        if is_supported_addon_acf:
            if Aircraft.doors_dataref:
                xp.sys_log(Aircraft.configuration_name + " configuration loaded.")
            else:
                xp.sys_log(Aircraft.configuration_name + " configuration loaded, with errors.")
            return 1
        return 0

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        PythonInterface.handler(AcfMonitor.disable)

        acf_icao = xp.getDatas(cls.acf_icao_dataref)
        if not cls.retrieve_acf(acf_icao):
            cls.flight_loop_counter += 1
            if cls.flight_loop_counter < MAX_RETRIES:
                xp.sys_log("Unable to retrieve " + acf_icao + " configuration. " + \
                    "Will try again in 5 seconds.")
                PythonInterface.flight_loop_interval = 5 # seconds
                return PythonInterface.flight_loop_interval

            xp.sys_log("A valid configuration was not found. " + \
                "Ensure you're using a supported aircraft.")
            Menu.disable()
        else:
            PythonInterface.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL
            PythonInterface.handler(AcfMonitor.enable)
        return 0

    flight_loop = flight_loop_callback
    flight_loop_id = None

    acf_icao_dataref = xp.findDataRef('sim/aircraft/view/acf_ICAO')


class AcfMonitor:
    service_on_door_open = False
    loading = False
    boarding = 0
    sim_doors_data_cache = [0] * NUMBER_OF_DOORS

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
        cls.sim_doors_data_cache = [Aircraft.door_closed_value] * NUMBER_OF_DOORS

    @classmethod
    def reset_data(cls):
        cls.loading = False
        cls.boarding = 0
        cls.sim_doors_data_cache = [Aircraft.door_closed_value] * NUMBER_OF_DOORS

    @classmethod
    def enable(cls):
        if cls.flight_loop_id is None:
            PythonInterface.handler(GHD.enable)
            cls.reset_data()

            cls.flight_loop_id = xp.createFlightLoop(cls.flight_loop, phase=1)
            xp.scheduleFlightLoop(cls.flight_loop_id, interval=DEFAULT_FLIGHT_LOOP_INTERVAL)

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
        if name in {STAIRWAY_FWD, STAIRWAY_AFT, BUS}:
            if cls.near_jetway:
                return
            if name == STAIRWAY_FWD and cls.has_builtin_stairs:
                GHD.select(GHD.ghd_dependencies[name])
                return
        if not cls.has_chocks:
            xp.commandOnce(Aircraft.chocks_command)
        GHD.select(name)

    @classmethod
    def start_loading(cls):
        xp.sys_log("Started loading!")
        cls.call_service_crew(CATERING_FWD)
        cls.call_service_crew(CATERING_AFT)
        cls.call_service_crew(CARGO_BELT_FWD)
        cls.call_service_crew(CARGO_BELT_AFT)

        cls.call_service_crew(STAIRWAY_FWD)
        cls.call_service_crew(STAIRWAY_AFT)
        if not cls.near_jetway:
            GHD.remove(BUS)
        cls.loading = True

    @classmethod
    def start_boarding(cls):
        xp.sys_log("Started boarding!")
        cls.loading = False
        cls.call_service_crew(STAIRWAY_FWD)
        cls.call_service_crew(STAIRWAY_AFT)
        cls.call_service_crew(BUS)
        cls.boarding = 1

    @classmethod
    def check_doors(cls):
        sim_doors_data = []
        xp.getDatavi(Aircraft.doors_dataref, sim_doors_data, count=NUMBER_OF_DOORS)

        cached = sim_doors_data == cls.sim_doors_data_cache
        if not cached:
            for i, door_status in enumerate(sim_doors_data):
                if door_status != cls.sim_doors_data_cache[i]:
                    if door_status in {Aircraft.door_closed_value, Aircraft.door_open_value}:
                        cls.sim_doors_data_cache[i] = door_status

                        if cls.service_on_door_open:
                            if door_status == Aircraft.door_open_value:
                                cls.call_service_crew(GHD.ghd_by_door[i])
                        if door_status == Aircraft.door_closed_value:
                            GHD.remove(GHD.ghd_by_door[i])

    @classmethod
    def flight_loop_callback(cls, sinceLast, elapsedTime, counter, refCon):
        if cls.on_ground:
            if not cls.engines_running:
                if Aircraft.doors_dataref and Aircraft.not_airstairs_dataref and \
                    Aircraft.loading_dataref and Aircraft.boarding_dataref:
                    if GHD.is_enabled and cls.beacon_on:
                        GHD.disable()
                    if GHD.is_enabled:
                        cls.check_doors()
                        if not cls.loading and cls.requested_service_crew:
                            cls.start_loading()
                        if not cls.boarding and cls.started_flight_leg:
                            cls.start_boarding()
                        if cls.boarding == 1 and not cls.pax_onboard:
                            GHD.remove(BUS)
                            cls.boarding == 2
                    elif not cls.beacon_on:
                        GHD.enable()
                    PythonInterface.flight_loop_interval = -1 * FrameRateMonitor.frame_rate # Real-time
                else:
                    xp.sys_log("Identified an issue with the loaded configuration. " + \
                        "Initiating reload attempt.")
                    PythonInterface.handler(AcfSelector.enable)
                    PythonInterface.flight_loop_interval = 0 # seconds
            else:
                PythonInterface.handler(FrameRateMonitor.disable)
                PythonInterface.flight_loop_interval = 2 # seconds
        else:
            PythonInterface.handler(FrameRateMonitor.disable)
            PythonInterface.flight_loop_interval = 30 # seconds
        return PythonInterface.flight_loop_interval

    flight_loop = flight_loop_callback
    flight_loop_id = None

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
        cls.id = xp.createMenu('AutoGHDforZibo', handler=cls.callback)
        xp.appendMenuItem(cls.id, ' Enabled', 'enabled')
        xp.appendMenuSeparator(cls.id)
        xp.appendMenuItem(cls.id, ' Service On Door Open', 'service_on_door_open')

        xp.checkMenuItem(cls.id, 0, xp.Menu_Checked)
        xp.checkMenuItem(cls.id, 2, xp.Menu_Unchecked)
        return cls.id

    @classmethod
    def destroy(cls):
        if cls.id:
            xp.destroyMenu(cls.id)

    @classmethod
    def enable(cls):
        if AcfSelector.acf_icao_dataref is None or \
            AcfMonitor.gear_on_ground_dataref is None or \
            AcfMonitor.engines_is_burning_fuel_dataref is None or\
            cls.id is None:
            return 0

        if GHD.plugin_id == xp.NO_PLUGIN_ID:
            xp.sys_log("Unable to find JARDesign's Ground Handling Deluxe")

        for attr_name, attr_value in vars(GHD).items():
            if attr_name.endswith("_dataref") and not callable(attr_value):
                if attr_value is None:
                    xp.sys_log("Unable to find " + str(attr_name) + " dataref from GHD")
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
        if itemRefCon == 'enabled' and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Checked:
            cls.disable()
            xp.sys_log("Disabled")
        elif itemRefCon == 'enabled' and xp.checkMenuItemState(cls.id, 0) == xp.Menu_Unchecked:
            cls.enable()
            xp.sys_log("Enabled")
        if itemRefCon == 'service_on_door_open' and xp.checkMenuItemState(cls.id, 2) == xp.Menu_Checked:
            AcfMonitor.service_on_door_open = False
            xp.checkMenuItem(cls.id, 2, xp.Menu_Unchecked)
            xp.sys_log("Service On Door Open set to " + str(AcfMonitor.service_on_door_open))
        elif itemRefCon == 'service_on_door_open' and xp.checkMenuItemState(cls.id, 2) == xp.Menu_Unchecked:
            AcfMonitor.service_on_door_open = True
            AcfMonitor.reset_cache()
            xp.checkMenuItem(cls.id, 2, xp.Menu_Checked)
            xp.sys_log("Service On Door Open set to " + str(AcfMonitor.service_on_door_open))


class PythonInterface:

    @staticmethod
    def handler(func, *args):
        return func(*args)

    def __init__(self):
        self.Name = "AutoGHDforZibo"
        self.Sig = "autoghdforzibo.xppython3"
        self.Desc = "Plugin to handle GHD automatically for Zibomod B737"

        self.flight_loop_interval = DEFAULT_FLIGHT_LOOP_INTERVAL

    def XPluginStart(self):
        # Required by XPPython3
        # Called once by X-Plane on startup (or when plugins are re-starting as part of reload)
        # You need to return three strings

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
            xp.sys_log("Received MSG_PLANE_LOADED.")
            if Menu.is_enabled:
                AcfSelector.reload()
            else:
                Menu.enable()