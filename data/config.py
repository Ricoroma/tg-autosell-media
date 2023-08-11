import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
data = config["settings"]
token = data["token"]
admin_id = int(data["admin_id"])
admin_link = data["admin_link"]
link = data["link"]
cryptopay_token = data['cryptopay_token']

sub_channels = [int(i) for i in data['channels_to_sub'].split(',')]
