# Renpho Weight

This is a custom component to import weight and last weight time from the Renpho app into Home Assistant.

### Installation

> :+1: Some things have changed, notably folder name (not sure if it makes a difference) and you noo longer have to sniff the hash as I reverse engineered the password hashing!

Copy this folder to `<config_dir>/custom_components/hass_renpho/`.

Add the following entry in your `configuration.yaml`:

```yaml
renpho:
  email: test@test.com       # email address
  password: MySecurePassword # password
  refresh: 600               # time to poll (ms)

sensor:
  platform: renpho
```

Your email address and password are what you would use to log into the app.

Refresh is the time in seconds to check for updates, bear in mind everytime you log in it logs you out of the app, so in my example it gives me ten minutes between checking in case I ever wish to browse the app.

### Updates
Changed some of the naming conventions, so it might be best to just reinstall the component.

I reversed engineered the apk and found the hashing/encryption methods for generating the hashes, this means we no longer have to sniff the hash and as such, makaing the component much more accessible.

### Roadmap
Some ideas as to where this is going.
1. Add all user information.  My dream is something along the lines of adding the following to config:
```yaml
sensor:
  platform: renpho
  user: neilzilla  # username, email, or something identifiable
```
2. Finding a way to not log you out of the mobile app, although this might not be feasible.


