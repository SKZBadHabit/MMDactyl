# Installation for MMDactyl on Raspberry pi pico on Circuitpython Firmware

## Download

downlad the latest Version from github all needed files for the appropiate version is included

## (example: 6.0) raspberry RP2350

- copy the Files under MMdactyl/code/6.0 to your RP2350(w) AFTER you prepared your RP with Circuitpython V9.
- Please pay attention when copy libs folder look up under readme of [firm_libs](firm_libs/readme.md) to use the right version

### file Information:

boot.py for bios mode and write to file on rp

settings.toml --> saved secrets (add your Wifi credentials,...)

### Final Result

should look like this:

![1736237468619](image/README/1736237468619.png)

pus the lib folder:

![1736237541124](image/README/1736237541124.png)

## (example: 3.13) raspberry RP2040

- copy the Files under MMdactyl/code/3.13 to your RP2040 AFTER you prepared your RP with Circuitpython V8.
- Please pay attention when copy libs folder look up under readme of [firm_libs](firm_libs/readme.md) to use the right version

### files for store data

create manually for installation

- /runtime.txt
- /keypress.txt
- /settings.toml

### file Information:

boot.py for bios mode and write to file on rp

settings.toml --> saved secrets (add your Wifi credentials,...)

### Final Result

should look like this:

![1734438267554](image/README/1734438267554.png)

within static:

![1734438079221](image/README/1734438079221.png)

within libs:

![1734438102630](image/README/1734438102630.png)
