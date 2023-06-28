import os
from dotenv import load_dotenv
from hcloud import Client
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from pprint import pprint
from wait_until_finished import wait_until_finished
load_dotenv()

HETZNER_API_TOKEN = os.getenv('HETZNER_API_TOKEN')

# Create a client
client = Client(token=HETZNER_API_TOKEN)

servers_list = client.servers.get_list()

for server in servers_list.servers:
        print("deleting server" + server.name)
        delete_server_response = server.delete()
        if delete_server_response.action is not None:
                delete_server_response.action.wait_until_finished()
                print("server deleted")
        if delete_server_response.next_actions is not None:
                wait_until_finished(delete_server_response.next_actions, "waiting for server to be deleted")
                        

# volumes_list = client.volumes.get_list()

# for volume in volumes_list.volumes:
#         print("deleting volume" + volume.name)
#         delete_volume_response = volume.delete()
#         wait_until_finished(delete_volume_response.actions, "waiting for volume to be deleted")
#         wait_until_finished(delete_volume_response.next_actions, "waiting for volume to be deleted")
