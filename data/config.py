import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
data = config["settings"]
token = data["token"]
admin_id = int(data["admin_id"])
admin_link = data["admin_link"]
link = data["link"]
cryptopay_token = data['cryptopay_token']
qiwi_token = data['qiwi_token']
media_folder = data['media_folder']

sub_channels = list(map(int, data['channels_to_sub'].split(','))) if data['channels_to_sub'] else ''
