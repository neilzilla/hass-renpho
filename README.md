# Renpho Weight

This is a custom component to import weight and last weigh time from the Renpho app into Home Assistant.

### Installation

Copy this folder to `<config_dir>/custom_components/renpho_weight/`.

Add the following entry in your `configuration.yaml`:

```yaml
renpho_weight:
  email: <email address>
  password_hash: <password hash>
  refresh: 600

sensor:
  platform: renpho_weight
```

Your email address is the email you would use to log into the app.

The password hash is a hash generated from your password, which has to be sniffed from traffic of yourself logging in, until I get a better way to generate it.

Refresh is the time in seconds to check for updates, bear in mind everytime you log in it logs you out of the app, so in my example it gives me ten minutes between checking in case I ever wish to browse the app.