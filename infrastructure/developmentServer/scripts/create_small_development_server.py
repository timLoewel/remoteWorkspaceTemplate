import os
from dotenv import load_dotenv
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.ssh_keys.client import SSHKeysClient
from wait_until_finished import wait_until_finished

load_dotenv()

HETZNER_API_TOKEN = os.getenv('HETZNER_API_TOKEN')
DEVELOPMENT_SERVER_SSH_PUBLIC_KEY = os.getenv('DEVELOPMENT_SERVER_SSH_PUBLIC_KEY')
DEVELOPMENT_SERVER_SSH_KEY_NAME = "rootKey"
VOLUME_NAME="TimDevelopmentDrive"
SERVER_NAME="TimDevelopmentServer"

client = Client(token=HETZNER_API_TOKEN)

if (client.ssh_keys.get_by_name(DEVELOPMENT_SERVER_SSH_KEY_NAME) is None):
    print("no ssh key found, creating new key")
    client.ssh_keys.create(DEVELOPMENT_SERVER_SSH_KEY_NAME, DEVELOPMENT_SERVER_SSH_PUBLIC_KEY)


keys_for_server = client.ssh_keys.get_all()
existing_servers = client.servers.get_all()

dc = client.datacenters.get_by_name("nbg1-dc3")
print("creating server " + SERVER_NAME )


create_server_response = client.servers.create(
    name = SERVER_NAME,
    server_type=ServerType(name="cx11"),
    image=Image(name="ubuntu-20.04"),
    ssh_keys=keys_for_server,
    datacenter=dc,
)
create_server_response.action.wait_until_finished()
wait_until_finished(create_server_response.next_actions, "waiting for server next actions to be finished")



new_server = client.servers.get_by_name(SERVER_NAME)
new_server.model.
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

#  write the new server to the inventory file
f = open('../ansible/inventory', 'w', encoding="utf-8")
f.write(new_server.public_net.ipv4.dns_ptr + "\n")
f.close()