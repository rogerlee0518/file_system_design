import os
import sys
import argparse
import rpyc

from threading import Thread

from fuse import FUSE
from fuseFunction import FuseOperation
from Controller import Controller

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed file system client")
    parser.add_argument('-v','--virtual', required=True, help='Virtual mount point')
    parser.add_argument('-r','--real', required=True, help='Physical mount directory')
    parser.add_argument('-p','--port', required=True, help='Port for main server endpoint')

    args = parser.parse_args()

    # todo: advanced function
    # k = Thread(target)
    # k.start()
    # Build connection\
    # port = int(args.port)
    # con = rpyc.connect("localhost", port = port)
    # main_server_service_exposed = con.root.MainServer()

    # subserver = main_server_service_exposed.get_subserver_list()
    # print(subserver)
    # k.join()
    controller = Controller()

    FUSE(FuseOperation(args.real, controller), args.virtual, foreground=True)
