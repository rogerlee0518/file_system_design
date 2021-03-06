import rpyc
# import socket
# from rpyc.utils.server import ThreadedServer
import configparser
import os
import math
import uuid
import random


def set_config():
    cur_folder = os.path.dirname(os.path.abspath(__file__))
    cf = os.path.join(cur_folder, 'configure.conf')
    config = configparser.ConfigParser()
    config.read(cf)
    MainServerService.block_size = \
        int(config.get('mainServer', 'block_size'))
    MainServerService.replication_factor = \
        int(config.get('mainServer', 'replication_factor'))
    # print(block_size, replication_factor)


# Main server service
class MainServerService(rpyc.Service):
    # expose main service to client
    class exposed_MainServer:
        block_size = 10             # size of each block
        replication_factor = 2     # number of replicates of each block
        subserver = {2510, 2511}             # unique id for each subserver
        file_table = {}            # {file_name: block_id-s} dictionary

        # Return file table entry corresponding to <target>
        def exposed_get_file_table(self, target):
            if target in self.__class__.file_table:
                return self.__class__.file_table[target]
            return None

        def exposed_get_sub_server(self, ids):
            return [self.__class__.subserver[_] for _ in ids]

        # Create file table entry (empty) for target file based on source file sizes
        # Return:
        #   block_table -> (block id, sub server id) tuple array
        #   
        def exposed_creat_file_table_entry(self, target, src_size):
            if target not in self.__class__.file_table:
                # Create entry for thix file 
                self.__class__.file_table[target] = []
            num_block = self.get_num_blocks(src_size)
            block_table = self.get_blocks_table(target, num_block)     
            return block_table

        # Return the number of block needed for storing file of size <size>
        def get_num_blocks(self, size):
            return int(math.ceil((float(size) / self.__class__.block_size)))

        def exposed_delete_file(self, target):
            del self.__class__.file_table[target]

        def exposed_rename_file(self, target, newname):
            self.__class__.file_table[newname] = self.__class__.file_table.pop(target)


        def exposed_get_block_size(self):
            return self.__class__.block_size

        # Assign a number of block with random sub servers
        # Return the (block id, subserver id) array of current target.
        def get_blocks_table(self, target, num_block):
            block_table = []
            for b in range(num_block):
                # get id for each block
                block_id = uuid.uuid1()
                # get id for target sub server 
                #subserver_ids = random.sample(self.__class__.subserver, self.__class__.replication_factor)
                subserver_ids = (2510, 2511)
                # add (block id, sub server id) as a tuple in <blocks>
                tpl = (block_id, subserver_ids)
                block_table.append(tpl)
                # add tuple to file table
                # Todo: What is target?
                self.__class__.file_table[target].append(tpl)
            return block_table


if __name__ == "__main__":
    set_config()
    port = 2220
    s = rpyc.utils.server.ThreadedServer(MainServerService, port=port)
    
    print("IP: localhost")
    print("Port: ", port)
    print("starting main server service...")
    s.start()
    # HOST = socket.gethostbyname(socket.gethostname())
    # print(HOST)

