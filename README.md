# XP-SLC-Integration
## Description
This script facilitates seamless integration between X-Plane 12 (XP12) aircraft datasets and XPUIPC for compatibility with Self-Loading Cargo (SLC) and other related programs. The script serves as a bridge, enabling aircraft door data transfer from XP12 to XPUIPC in real time.

## Requirements  
- [XPPython3](https://xppython3.readthedocs.io/en/latest/)  
- [Self-Loading Cargo](https://www.selfloadingcargo.com/)  
- [XPUIPC](https://www.schiratti.com/xpuipc.html) 2.0.3.8  

## Installation  
1. **Drag & Drop**: Move the contents of the ```Resources/``` folder into your X-Plane 12 directory.  
2. **Configuration**: Append the following code to the end of ```XPUIPCOffsets.cfg``` located in ```X-Plane 12/Resources/plugins/XPUIPC/```

```cfg
# XP-SLC-Integration dataset
Dataref SLCDoorStatus slc/doors/status int
Offset    0x3367    UINT8    1    rw    $SLCDoorStatus
```

> [!IMPORTANT]
> Ensure you have 'Pilot Mode (Manual)' with 'Synchronise With Simulator' enabled in the SLC Door Management Window.

> [!NOTE]
> Please note that the doors cannot be operated through SLC, as it solely reads from the dataset without the capability to write to it.
> Consequently, the 'Cabin Crew Mode (Automatic)' feature does not function with this integration.

## Supported Aircrafts
 - Laminar Research A330-3
 - Laminar Research B737-8
 - Laminar Research MD-82
   
 - Zibo Mod B737-800X
