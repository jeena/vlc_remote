HomeAssistant VLC HTTP component
================================

This component let's you add a remote VLC as a media_player to your
HomeAssistant instance.

Preconditions
-------------

- A computer which is accessible via network by HomeAssistant running VLC
- The Web interface in VLC is enabled, [see this how-to](https://www.howtogeek.com/117261/how-to-activate-vlcs-web-interface-control-vlc-from-a-browser-use-any-smartphone-as-a-remote/)
- This component is installed in HomeAssistant (*config*/custom\_components/vlc_http)
- This component is enabled in the configuration.yaml like this:

```yaml
media_player:
  - platform: vlc_http
    host: 192.168.2.20
    port: 8080
    password: !secret vlc_http_password
```

After doing that you need to restart your HomeAssistant.

Notes
-----

It only works with HTTP because the VNC Web interface is only available via
HTTP and not HTTPS.

You can autostart VNC on your computer and it will play for example text to
speach messages from HomeAssistant on it while you're on the computer, without
the need of an additional speaker connected to HomeAssistant.

This component is basically a copy of [vlc_telnet](https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/vlc_telnet)
but it replaces the Telnet backend with a HTTP backend.

I hope I will be able to get it into HomeAssistant one day, perhaps by
extending the vlc_telnet component instead of having a copy of it.

License
-------

This code is under the same license as HomeAssistant: Apache License 2.0
