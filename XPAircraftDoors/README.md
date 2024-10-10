# XP Aircraft Doors  
  
## Description  
  
The XP Aircraft Doors plugin facilitates seamless integration between X-Plane 12 (XP12) aircraft datasets and XPUIPC for compatibility with Self-Loading Cargo (SLC) and other related programs. Acting as a bridge, it enables real-time aircraft door data transfer from XP12 to XPUIPC.  
  
## Requirements  
  
- [X-Plane 12](https://www.x-plane.com/)  `v12.1.2`  
- [XPPython3](https://xppython3.readthedocs.io/en/latest/)  `v4.4.1`  
- [XPUIPC](https://www.schiratti.com/xpuipc.html)  `v2.0.3.8`  
  
> [!NOTE]  
> The use of outdated or mismatched versions may affect XP Aircraft Doors's functionality due to possible changes in datarefs.  
  
### Supported Aircrafts  
 - Laminar Research A330-3  
 - Laminar Research B737-8  
   
 - [Zibomod B737-800X](https://forums.x-plane.org/index.php?/forums/forum/384-zibo-b738-800-modified/) `v4.02`  
  
### Self-Loading Cargo Cabin Layouts  
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
# Declarations of all doors datarefs
Dataref XPTKDoorStatus xptk/doors/status int
Offset    0x3367    UINT8    1    rw    $XPTKDoorStatus
```  

### Self-Loading Cargo Quick Notes  
> [!IMPORTANT]  
> Ensure 'Pilot Mode (Manual)' with 'Synchronise With Simulator' is enabled in the SLC Door Management Window.  
  
> [!NOTE]  
> The doors cannot be operated through SLC; it only reads from the dataset without the capability to write to it. Consequently, the 'Cabin Crew Mode (Automatic)' feature does not function with this integration.  
  
## Features  
  
### Performance Optimization  
**Reduced Loop Overhead:** This plugin enhances overall performance by optimizing loops during flight or engine operation phases.  
  
> [!NOTE]  
> A slight delay might occur after the termination of these phases.  
  
### Monitoring and Detection  
**Real-Time Aircraft Monitoring:** An integrated FPS monitor provides real-time updates on aircraft door statuses, ensuring accurate and timely information.  
  
**Multi-Stage Aircraft Detection:** Utilizes multiple parameters, including aircraft plugin, directory, and ICAO code, for precise and reliable aircraft identification.  
  
### Door Management  
**Interactive Door Handling:** This plugin allows users to interact with aircraft doors through the aircraft's system or manually edit datarefs for door manipulation. 
  
### Settings and Preferences  
**Persistent Settings:** The plugin retains user preferences and settings, providing a consistent and personalized experience.  
  
## Bug Reports  
   Please report any bugs you encounter in the comment section below, or at the github repository <https://github.com/BrunoCostaGH/XP-Toolkit>  
