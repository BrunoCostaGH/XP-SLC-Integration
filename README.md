# XP-SLC-Integration

## Description

The XP-SLC-Integration script facilitates seamless integration between X-Plane 12 (XP12) aircraft datasets and XPUIPC for compatibility with Self-Loading Cargo (SLC) and other related programs. Acting as a bridge, it enables real-time aircraft door data transfer from XP12 to XPUIPC.

## Requirements  

- [X-Plane 12](https://www.x-plane.com/)  `v12.0.9-rc-5`
- [XPPython3](https://xppython3.readthedocs.io/en/latest/)  `v4.2.1 for Python 3.12`
- [Self-Loading Cargo](https://www.selfloadingcargo.com/)  `v1.6.3`
- [XPUIPC](https://www.schiratti.com/xpuipc.html)  `v2.0.3.8`

> [!NOTE]
> The use of outdated or mismatched versions may affect the script's functionality due to changes in datarefs.

### Supported Aircrafts
 - Laminar Research A330-3
 - Laminar Research B737-8
 - Laminar Research MD-82
   
 - [Zibo B737-800X](https://forums.x-plane.org/index.php?/forums/forum/384-zibo-b738-800-modified/) `v4.01`

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

## FAQ  

**Q**: Why does SLC not update when I open a door?  
**A**: Ensure you are using a Supported Aircraft and have not changed the default folder name from the aircraft. For example, Zibo's must be the default 'B737-800X'.
