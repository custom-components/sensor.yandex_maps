# sensor.yandex_maps

[![BuyMeCoffee][buymecoffeebedge]][buymecoffee]
[![custom_updater](https://img.shields.io/badge/custom__updater-true-success.svg)](https://github.com/custom-components/custom_updater)

_A platform which give you the time it will take to drive._

**Data is fetched from yandex.ru.**

![example][exampleimg]

## Installation

To get started put `/custom_components/yandex_maps/sensor.py` here:  
`<config directory>/custom_components/yandex_maps/sensor.py`

## Example configuration.yaml

```yaml
sensor:
  platform: yandex_maps
  start: 'device_tracker.my_phone'
  destination: '29.361133,54.991133'
  name: Time to work
```

## Configuration variables
  
key | type | description  
:--- | :--- | :---  
**platform (Required)** | string | The platform name.
**start (Required)** | string | ID of an entity which have `latitude` and `longitude` attributes, or GPS coordinates like `'29.361133,54.991133'`.
**destination (Required)** | string | ID of an entity which have `latitude` and `longitude` attributes, or GPS coordinates like `'29.361133,54.991133'`.
**name (Required)** | string | Name of the sensor.

***

[exampleimg]: example.png
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
