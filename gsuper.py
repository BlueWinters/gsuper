
# import os
# import time
# import json
# import paramiko
import argparse
import nvidia_smi
from os import system
from time import sleep as time_sleep
from json import load as json_load
from paramiko import SSHClient, AutoAddPolicy
# from server import ServersDict


class Server:
    def __init__(self, name, config_dict:dict):
        self.name = name
        self.hostname = config_dict['hostname']
        self.username = config_dict['username']
        self.password = config_dict['password']
        self.num_gpus = config_dict['num_gpus']
        self.ssh = self.connect()
        self.info = '{host:12s} {name:10s}\n'
        self.stdout_src = '\t{id:d}: {usage:8s}/{memory:8s} {fraction:3s}\n'
        self.stdout_red = '\t\033[1;35m{id:d}: {usage:8s}/{memory:8s} {fraction:3s}\033[0m\n'

    def __del__(self):
        if self.ssh is not None:
            print('SSH to {} is closed'.format(self.hostname))
            self.ssh.close()

    def connect(self):
        if hasattr(self, 'ssh') == False:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
            return ssh

    def _to_int(self, fra):
        return int(fra.rstrip('%'))

    def nvidia_smi(self):
        if self.ssh is not None:
            stdin, stdout, stderr = self.ssh.exec_command('nvidia-smi')
            stdout_line_list = [line for line in stdout]
            version_dict, status_list = nvidia_smi.parse_nvidia_smi(stdout_line_list, self.num_gpus)
            # print information
            line = self.info.format(host=self.hostname, name=self.name)
            for n, status in enumerate(status_list):
                if self._to_int(status['Mem_Fra']) == 0:
                    line += self.stdout_red.format(
                        id=n, usage=status['Mem_Use'], memory=status['Mem_All'], fraction=status['Mem_Fra'])
                else:
                    line += self.stdout_src.format(
                        id=n, usage=status['Mem_Use'], memory=status['Mem_All'], fraction=status['Mem_Fra'])
            return line

            # print('nvidia-smi:{:16s} drive:{:16s} cuda:{:8s}'.format(
            #     version_dict['NVIDIA_SMI'], version_dict['Driver'], version_dict['CUDA']))
            # for status in status_list:
            #     print('Usage:{:16s} Fra:{:16s} All:{:16s}'.format(
            #         status['Mem_Use'], status['Mem_Fra'], status['Mem_All']))
        else:
            print('no ssh connect')
            return



def refresh(server_list, n, N):
    all_line = 'times: {}/{}\n'.format(n, N)
    for n in range(len(server_list)):
        server = server_list[n]
        all_line += server.nvidia_smi()
    system('cls\n')
    print(all_line)


def connect(json_file):
    server_list = list()
    with open(json_file, 'r') as file:
        ServersDict = json_load(file)
        for name in ServersDict:
            config = ServersDict[name]
            server_list.append(Server(name, config))
    return server_list



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=int, default='1', help='refresh times')
    parser.add_argument('-i', type=int, default='1', help='refresh intervals')
    parser.add_argument('-j', type=str, default='server.json', help='json file for servers')
    args = parser.parse_args()

    server_list = connect(args.j)
    for n in range(args.t):
        refresh(server_list, n+1, args.t)
        time_sleep(args.i)

    system('pause')

