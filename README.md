# MMDactyl - RP2040w & RP2350 Japanese Duplex Matrix

Welcome to MMDactyl, your custom-designed Dactyl keyboard powered by the RP2040w/RP2350w microcontroller. This keyboard is not only a functional input device but also a testament to precision engineering and innovative coding. Below, you'll find details on its development, coding progress, lasercut designs, completed steps, and what's next on the agenda.

![MMDactyl Keyboard](https://github.com/SKZBadHabit/MMDactyl/assets/72281265/1e6f7bd4-ab28-4964-b751-b02aff36cae3)

## Coding Progress

The heart of MMDactyl lies in its meticulously crafted code. Currently at version 6.1, the code is fully functional, encompassing the fundamental layers, basic display functionality, and BIOS support. While wireless functionality is implemented with webserver and ntp integration, the focus remains on refining existing features and laying the groundwork for future enhancements, including energy-saving mechanisms. Now fresh with Raspberry Pi Pico 2 W support and with Circuitpython v9 firmware.

## Installation Guide:

Firmware + Libraries: [InstallFW+LIBS](firm_libs/readme.md)

Install to Raspberry Pi Pico: [InstallSoftware](code/README.md)

## Lasercut Design

Crafted with precision, the lasercut design of MMDactyl ensures both aesthetic appeal and functional integrity. While the current files are fully functional, ongoing efforts are directed towards refining the design for enhanced aesthetics and ease of assembly. (3mm black acryl was used in the example picture above) The file is for now not completed because you have to multiply some parts, will be changed soon.

Lasercut file: [Draft V6](hardware/lasercut_Draftv6.dxf)

Pics of the finished product: [pics](hardware/pics_of_keyboard)

## Cableing Layout

Guidance for cabeling the whole Layout: [wiring plan](hardware/begin_cable_plan.png)

Informations about the ideea: [information cabel plan](hardware/README.md)

## Completed Steps

MMDactyl has already achieved significant milestones, including:

- **Hardware Integration**: Successful integration into existing keyboard structures, replacing the Arduino Pro Micro seamlessly.
- **Code Adaptation**: The codebase has been tailored to suit the unique characteristics of MMDactyl, ensuring optimal performance.
- **Display Integration**: Display functionality is implemented, providing essential feedback without the need for wireless connectivity.
- **BIOS Compatibility**: MMDactyl operates seamlessly within BIOS environments, guaranteeing system-wide compatibility.
- **Layer Management**: The addition of a layer toggle button enhances user flexibility and workflow efficiency.
- **Data Management**: Runtime data tracking is functional, providing insights into keyboard usage patterns.
- **Web Interface Integration**: Creating a web interface accessible via the RP2040w/RP2350w for convenient settings adjustment and monitoring. --> Started with Version 3.04
- **Time Date**: Time and date synchronistation and displaying on oled from ntp server
- **Design Cleanup**: Refining the lasercut files to streamline production and enhance aesthetics.
- **Layer Expansion**: Implementing additional layers to accommodate diverse user preferences and workflows. --> stopped no need for my personal usage for now

## Next Steps

As we move forward, the focus will be on further refinement and feature expansion. Upcoming tasks include:

- **Changing out to RP2W with more security features**: Setting the Rp2w up with ciruitpython testing features and using new technology for storing the code!
- **Testing and Refinement**: Rigorous testing will ensure the stability and reliability of MMDactyl under various conditions. - Auto Reboot of keyboard after a Runtime over 1500 Minutes but could be my DHCP because i lose the wifi connection.
- **Wiring Plan Completion**: Finalizing the wiring plan to optimize functionality and ease of assembly.
- **Display Enhancements**: Introducing additional display functionalities such as weather updates and keyboard status indicators./ for now only one option
- **Energy Management**: Introducing hibernation and energy-saving features to extend battery life and optimize power consumption. /started nearly finished - CPU reducing and Display clearing --> Missing wireless on/off
- **Data Expansion**: Further expanding data management capabilities, including key counter functionalities and customizable settings. --> Key counter implemented customizable settings planed (Keyboard layout definition over file (perhaps))

Stay tuned as MMDactyl evolves into a pinnacle of ergonomic design, technological innovation, and user-centric functionality.

## Version Infos

**3.13**:

- fully functioning Version3

**5.x**:

- in the folder but not released fully functioning with some extra performance patches, nof fully documented last Update of the RP2040 Version with Circuitpython Version 8

**6.0:**

- First version for RP2350 w

**6.1:**

- Smoothing out some parts, adding multiple retrys to connect to wifi. Buggy start fixed.

## Bugfix

**3.13**:

- with Version 3.13 comes the first bugfix and not only feature update. When NTP not reaching the keyboard got stuck until it reached the timeout -- fixed now it only gets it time from the ntp when initializing and then it counts itself so no delay from internet needed

## Known Bugs

**3.13**:

- with Version 3.13 the bugfix for NTP is perfect but, another problem occured with long time use, the flash storage is getting really slow so with the next big Version Step which is already staged will fix this issue.
- after a really long runtime over 2000+ minutes of Runtime, the keyboard sometimes looses its wireless connection (could be also my DHCP)

**6.0:**

- on some starts buggy - no reason why for now.

**6.1:**

- nothing for now

## Example of Layer layout:

### Layer 1

![MMDactyl Keyboard](hardware/mmdactyl_rp2040_layer1.png)

### Layer 2

![MMDactyl Keyboard](hardware/mmdactyl_rp2040_layer2.png)
