# XP-SLC-Integration  
  
## Description  
  
The XP-SLC-Integration script facilitates seamless integration between X-Plane 12 (XP12) aircraft datasets and XPUIPC for compatibility with Self-Loading Cargo (SLC) and other related programs. Acting as a bridge, it enables real-time aircraft door data transfer from XP12 to XPUIPC.  
  
## Requirements  
  
- [X-Plane 12](https://www.x-plane.com/)  `v12.0.9-rc-5`  
- [XPPython3](https://xppython3.readthedocs.io/en/latest/)  `v4.2.1 for Python 3.12`  
- [Self-Loading Cargo](https://www.selfloadingcargo.com/)  `v1.6.0`  
- [XPUIPC](https://www.schiratti.com/xpuipc.html)  `v2.0.3.8`  
  
> [!NOTE]  
> The use of outdated or mismatched versions may affect the script's functionality due to changes in datarefs.  
  
### Supported Aircrafts  
 - Laminar Research A330-3  
 - Laminar Research B737-8  
 - Laminar Research MD-82  
   
 - [Zibomod B737-800X](https://forums.x-plane.org/index.php?/forums/forum/384-zibo-b738-800-modified/) `v4.01`  
  
### SLC Cabin Layouts  
> [!NOTE]  
> These cabin layouts are designed to accurately reflect the door dataref position, taking into account the variations that exist from one aircraft to another.  
  
- Zibomod B737-800X  
    - [B738 - Boeing 737-800 - 'Zibomod Dual Class (XP12)' - 189 Seats - 4 Crew](https://www.selfloadingcargo.com/cabinlayouts/view/10435)  
    - [B738 - Boeing 737-800 - 'Zibomod Dual Class (XP12)' - 180 Seats - 4 Crew](https://www.selfloadingcargo.com/cabinlayouts/view/10445)  
    - [B738 - Boeing 737-800 - 'Zibomod Triple Class (XP12)' - 160 Seats - 4 Crew](https://www.selfloadingcargo.com/cabinlayouts/view/10429)  
  
## Installation  
  
1. **Drag & Drop**: Move the contents of the `Resources/` folder into your X-Plane 12 directory.  
2. **Configuration**: Append the following code to the end of `XPUIPCOffsets.cfg` located in `X-Plane 12/Resources/plugins/XPUIPC/`  
  
```  
# XP-SLC-Integration dataset  
Dataref SLCDoorStatus slc/doors/status int  
Offset    0x3367    UINT8    1    rw    $SLCDoorStatus  
```  
  
> [!IMPORTANT]  
> Ensure 'Pilot Mode (Manual)' with 'Synchronise With Simulator' is enabled in the SLC Door Management Window.  
  
> [!NOTE]  
> The doors cannot be operated through SLC; it only reads from the dataset without the capability to write to it. Consequently, the 'Cabin Crew Mode (Automatic)' feature does not function with this integration.  
  
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
  
## FAQ  
  
**Q**: Why is there a slight delay sometimes when I open a door in the Zibomod B737-800X?  
**A**: The dataref used to monitor the doors on the Zibomod B737-800X is not a simple open or closed status. When the door is in motion, the dataref holds a value that indicates whether the door is in motion or not. This may prevent the script to detect the door movement accurately. At the latest, the script will update the value when the door has completed its motion.  
