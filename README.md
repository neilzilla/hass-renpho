# Renpho Weight

This is a custom component to import weight and last weigh time from the Renpho app into Home Assistant.

### Installation

Copy this folder to `<config_dir>/custom_components/renpho_weight/`.


### Configuration

- `email` is **mandatory** and represent the email you use to log in the app
- `password_hash` is **mandatory** and represent the hash of your password.  See note below to get it.
- `refresh` is **mandatory** and represent the time to check for update. 
- `weight_units` is **mandatory** and represent the unit of every MASS sensor.  Possible values are 'kg' or 'lb'.

For example, add the following entry in your `configuration.yaml`:

```yaml
renpho_weight:
  email: <email address>
  password_hash: <password hash>
  refresh: 600
  weight_units: kg / lb

sensor:
  platform: renpho_weight
```


#### Find you password hash

The password hash is a hash generated from your password, which has to be sniffed from traffic of yourself logging in, until I get a better way to generate it.
You can check the blog of the original author of this integration https://neilgaryallen.dev/blog/reverse-engineering-renpho-app

The principle is to install an app that snif https request on your phone (I used NetKeeper) and then open your Renpho application and find your hash password.
Be aware that for Android, you need to have Android 6 or less as web certificate validation changed in Android 7.

### Important information
- Bear in mind everytime you log in it logs you out of the app, so in my example it gives me ten minutes between checking in case I ever wish to browse the app.
- The MASS data are stored in Kg on the renpho API.  So, if you select the weight_units, in lb, a conversion will be made by a factor of 2.2046226218


### RoadMap / What's to come

Change the config value to make refresh and weight_units optional with default value (Use CONFIG_SCHEMA ?)
