# AutoGHDforZibo 
  
## Description  
  
The AutoGHDforZibo plugin enhances the Zibomod B737 experience by automating JARDesign's Ground Handling Deluxe (GHD) services at critical stages of operation.
  
## Requirements  
  
- [X-Plane 12](https://www.x-plane.com/)  `v12.0.9-rc-5`  
- [XPPython3](https://xppython3.readthedocs.io/en/latest/)  `v4.2.1 for Python 3.12`  
- [JARDesign's GHD](https://main.jardesign.org/GHD.html)  `v.5_130922_XP12`  
- [XPUIPC](https://www.schiratti.com/xpuipc.html)  `v2.0.3.8`  
  
> [!NOTE]  
> The use of outdated or mismatched versions may affect AutoGHDforZibo's functionality due to changes in datarefs.  
  
### Supported Aircrafts  
 - [Zibomod B737-800X](https://forums.x-plane.org/index.php?/forums/forum/384-zibo-b738-800-modified/) `v4.01`  
  
## Installation  
  
1. **Drag & Drop**: Move the contents of the `Resources/` folder into your X-Plane 12 directory.  
  
## Features  
  
**Reduced Loop Overhead for Increased Performance:**
   This plugin optimizes loops during flight or while engines are running, resulting in enhanced performance. It ensures a smoother gaming experience without sacrificing realism.  
  
> [!NOTE]  
> A slight delay might occur after the termination of these phases.  
  
**Multi-Stage Aircraft Detection:**
   This plugin includes an integrated FPS monitor that provides real-time door monitoring.  
  
**Aircraft Detection via Multiple Parameters:**
   This plugin uses a comprehensive detection system to detect aircraft using parameters such as aircraft plugin, directory, and ICAO code. It ensures accurate identification of aircraft.  
  
**Interactive Door Handling:**
   This plugin allows users to interact with aircraft doors through the aircraft's system or manually edit datarefs for door manipulation.  
  
**Menu:**
   This plugin offers a plugin menu that enables users to control activation, deactivation, and the option to select 'Service on Door Open' effortlessly. 
  
**Service on Door Open:**
   This plugin enables vehicles to be called on door open for loading and boarding instead of restricting the use of 'Start Service Crews On Ground' and 'Start Flight Leg', respectively.  
  
**Persistent Settings:**
   This plugin provides persistent settings for 'Service on Door Open'.  
  
## FAQ  
  
**Q**: Why is there a slight delay sometimes when I open a door in the Zibomod B737-800X?  
**A**: The dataref used to monitor the doors on the Zibomod B737-800X is not a simple open or closed status. When the door is in motion, the dataref holds a value that indicates whether the door is in motion or not. This may prevent AutoGHDforZibo to detect the door movement accurately. At the latest, AutoGHDforZibo will update the value when the door has completed its motion.  
  
**Q**: When I arrive at the gate, why don't the services start unloading automatically?  
**A**: AutoGHDforZibo has a default setting of 'Service on Door Open' set to False. This means that the services won't be called when you open the doors. If you want the services to unload automatically upon arrival at the gate, you will need to turn on this setting.  
