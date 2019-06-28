# netatmo-gateway
Netatmo API gateway for retrieving station data and make them directly accessible in your local network without authentication.
Sensible information is redacted.

## Usage

Retrieve your netatmo *client id*, *client secret* for your netatmo app (https://dev.netatmo.com/myaccount/) and your *device id*; i.e. your station mac address.
Start the container 
```
$ docker run -ti --rm -e CLIENT_ID=... -e CLIENT_SECRET=... -e PASSWORD=... -e "USERNAME=..." -e "DEVICE_ID=..." -p 5000:5000 ntim/netatmo-gateway:latest
```

On raspbian, use the `armhf` tag.

The result looks like this:
```
$ curl http://localhost:5000 -s | jq
{
  "devices": [
    {
      "co2_calibrating": false,
      "dashboard_data": {
        "AbsolutePressure": 1002.1,
        "CO2": 523,
        "Humidity": 46,
        "Noise": 40,
        "Pressure": 1024,
        "Temperature": 25.5,
        "date_max_temp": 1561731479,
        "date_min_temp": 1561673036,
        "max_temp": 25.8,
        "min_temp": 22.9,
        "pressure_trend": "down",
        "temp_trend": "stable",
        "time_utc": 1561739046
      },
      "firmware": 140,
      "module_name": "...",
      "modules": [
        {
          "battery_percent": 100,
          "battery_vp": 6182,
          "dashboard_data": {
            "Humidity": 39,
            "Temperature": 24.9,
            "date_max_temp": 1561736903,
            "date_min_temp": 1561696263,
            "max_temp": 25,
            "min_temp": 14.5,
            "temp_trend": "stable",
            "time_utc": 1561739004
          },
          "firmware": 46,
          "last_message": 1561739055,
          "last_seen": 1561739055,
          "module_name": "...",
          "rf_status": 85
        }
      ],
      "station_name": "...",
      "wifi_status": 49
    }
  ]
}
```
