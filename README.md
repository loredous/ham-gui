# Ham GUI/HamPI

![example image of project in use](/images/20230523_125758.jpg)

## Overview
This project is designed around the concept of including a Raspberry Pi with a small touchscreen in my amateur radio setup. The pi will act as a digital interface for the radios, as well as providing Winlink (and eventually Packet BBS) functionality via a local wifi hotspot and web interface. The eventual goal of the project is to provide the ability to have a centralized radio "stack" that can be utilized by multiple resources in an EOC/field deployment situation, without requiring each resource have a fully featured radio + interface + laptop available and dedicated to them. 

## Software Stack
The touch interface and main logic/functionality are provided by the custom `hamgui` python application maintained in this repository. In addition, the following software packages are utilized:

* [Pat Winlink Client](https://getpat.io) - Winlink interface and message handling
* [Direwolf Software TNC](https://github.com/wb2osz/direwolf) - AX.25 TNC/Modem
* dnsmasq - DHCP/DNS provider for local hotspot
* hostapd - Linux AP setup software

## Hardware
The current hardware that the software is being developed for and tested on is:

* Raspberry Pi 4 - 4GB
* [Miuzei 4" touchscreen](https://www.amazon.com/Miuzei-Raspberry-Full-Angle-Heatsinks-Raspbian/dp/B07XBVF1C9)
* 2x [Digirig](https://digirig.net/) audio interfaces
* Yaesu FT8900r - VHF/UHF Communications
* Xiegu G90 - HF Communications

