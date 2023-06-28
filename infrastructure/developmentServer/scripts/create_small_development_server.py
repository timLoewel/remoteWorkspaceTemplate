import os
from dotenv import load_dotenv
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.ssh_keys.client import SSHKeysClient
from wait_until_finished import wait_until_finished

load_dotenv()

HETZNER_API_TOKEN = os.getenv('HETZNER_API_TOKEN')
SSH_PUBLIC_KEY = os.getenv('SSH_PUBLIC_KEY')

VOLUME_NAME="TimDevelopmentDrive"
SERVER_NAME="TimDevelopmentServer"

client = Client(token=HETZNER_API_TOKEN)
existing_keys = client.ssh_keys.get_all()

if (len(existing_keys) == 0):
    print("no ssh key found, creating new key")
    client.ssh_keys.create("root key", SSH_PUBLIC_KEY)

keys = client.ssh_keys.get_all()
existing_servers = client.servers.get_all()

dc = client.datacenters.get_by_name("nbg1-dc3")
print("creating server " + SERVER_NAME )


create_server_response = client.servers.create(
    name = SERVER_NAME,
    server_type=ServerType(name="cx11"),
    image=Image(name="ubuntu-20.04"),
    ssh_keys=keys,
    datacenter=dc,
)
create_server_response.action.wait_until_finished()
wait_until_finished(create_server_response.next_actions, "waiting for server next actions to be finished")



new_server = client.servers.get_by_name(SERVER_NAME)

volume = client.volumes.get_by_name(VOLUME_NAME)
print("volume " + str(volume.model.name))
# create_volume_response = client.volumes.create(name=volume_name, size=10, server=new_server, format="ext4", automount=True,
# )
# wait_until_finished(create_volume_response.actions, "waiting for server to be created")
# wait_until_finished(create_volume_response.next_actions, "waiting for server next actions to be finished")
                                               

volume.attach(new_server, automount=True)

# client.volumes.attach(volume=volume, server=new_server, automount=True)

print("new server can be found under")
print(new_server.public_net.ipv4.dns_ptr)
