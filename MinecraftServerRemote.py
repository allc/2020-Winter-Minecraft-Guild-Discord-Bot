import socket
import struct
import json
from utils.minecraft_server import pack_varint, unpack_varint

class MinecraftServerRemote:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

        self.server_list_ping_data = None


    def update_server_list_ping_data_cache(self) -> None:
        '''Update Server List Ping data cache.'''
        self.server_list_ping_data = self._server_list_ping()


    def get_online_players_count(self, from_cache=False):
        server_list_ping_data = self._get_server_list_ping_data(from_cache)
        return int(server_list_ping_data['players']['online'])


    def get_online_players(self, from_cache=False):
        '''Get a list of online players

        Returns:
        List:List of online players

        '''
        server_list_ping_data = self._get_server_list_ping_data(from_cache)
        if 'sample' in server_list_ping_data['players']:
            players = [player['name'] for player in server_list_ping_data['players']['sample']]
        else:
            players = []
        return players


    def _server_list_ping(self) -> dict:
        '''Perform Server List Ping

        Returns:
        dict:Server List Ping data
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.connect((self.address, self.port))

            # Handshake
            protocol_version = pack_varint(754)
            server_address = pack_varint(len(self.address)) + self.address.encode('utf-8')
            port = struct.pack('!H', self.port)
            next_state = pack_varint(1) # next state 1 for status
            handshake = b'\x00' + protocol_version + server_address + port + next_state
            connection.send(pack_varint(len(handshake)) + handshake)
            
            # Request
            request = b'\x00'
            connection.send(pack_varint(len(request)) + request)

            # Response
            packet_length = unpack_varint(connection)
            packet_id = unpack_varint(connection)
            packet_length_remaining = unpack_varint(connection)
            response = connection.recv(packet_length_remaining)
            response = response.decode('utf-8')
            response = json.loads(response)
            return response


    def _get_server_list_ping_data(self, from_cache=False) -> dict:
        '''Get Server List Ping data. Update cache if fresh data is requested

        Returns:
        dict:Server List Ping data
        '''
        if not from_cache or self.server_list_ping_data is None:
            self.update_server_list_ping_data_cache()
        return self.server_list_ping_data
