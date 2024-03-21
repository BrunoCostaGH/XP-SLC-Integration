# AutoGHD for Zibo 
  
## Description  
  
The AutoGHD for Zibo script enhances the Zibomod B737 experience by automating JARDesign's Ground Handling Deluxe (GHD) plugin services at critical stages of operation. By integrating with GHD, this script streamlines ground handling tasks, improving realism and immersion for users.  
  
## Requirements  
  
- [X-Plane 12](https://www.x-plane.com/)  `v12.0.9-rc-5`  
- [XPPython3](https://xppython3.readthedocs.io/en/latest/)  `v4.2.1 for Python 3.12`  
- [JARDesign's GHD](https://main.jardesign.org/GHD.html)  `v.5_130922_XP12`  
- [XPUIPC](https://www.schiratti.com/xpuipc.html)  `v2.0.3.8`  
  
> [!NOTE]  
> The use of outdated or mismatched versions may affect the script's functionality due to changes in datarefs.  
  
### Supported Aircrafts  
 - [Zibomod B737-800X](https://forums.x-plane.org/index.php?/forums/forum/384-zibo-b738-800-modified/) `v4.01`  
  
## Installation  
  
1. **Drag & Drop**: Move the contents of the `Resources/` folder into your X-Plane 12 directory.  
  
## Features  
  
**Reduced Loop Overhead for Increased Performance:**
   Enhance performance by optimizing loops during flight or while engines are running. This optimization ensures a smoother gameplay experience without sacrificing realism.  
  
> [!NOTE]  
> A slight delay might occur after the termination of these phases.  
  
**Multi-Stage Aircraft Detection:**
   Integrate an FPS monitor to provide real-time door monitoring.  
  
**Aircraft Detection via Multiple Parameters:**
   Implement system to detect aircraft using various parameters such as aircraft script, directory, and ICAO code. This comprehensive detection system ensures accurate identification of aircraft.  
  
**Interactive Door Handling:**
   Enable users to interact with aircraft doors through the aircraft's system or manually edit datarefs for door manipulation.  
  
**Menu:**
   Enable users to effortlessly control script activation, deactivation, and the option to enable Service on Door Open through a user-friendly menu interface. 

**Service on Door Open:**
   Allow vehicles to be called on door open, instead of restricting to the use of 'Start Service Crews On Ground' and 'Start Flight Leg', for loading and boarding, respectively.
  
## FAQ  
  
**Q**: Why is there a slight delay sometimes when I open a door in the Zibomod B737-800X?  
**A**: The dataref used to monitor the doors on the Zibomod B737-800X is not a simple open or closed status. When the door is in motion, the dataref holds a value that indicates whether the door is in motion or not. This may prevent the script to detect the door movement accurately. At the latest, the script will update the value when the door has completed its motion.  
