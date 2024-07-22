
import time
import numpy as np
import random

from multiprocessing import Process, Queue, Manager, Barrier
from typing import Literal, Union, Dict, List, Tuple

MAP_SIZE = 100

class Worker:
    def __init__(self, 
                    id:int, 
                    pose:np.array, 
                    sleep_time:float,
                ):
        self.id             = id
        self.name           = f"Agent_{id}"
        self.msg_buffer     = []
        self.value          = id
        self.pose           = pose
        self.time_list      = []
        self.comm_iter_list = []
        self.sleep_time     = sleep_time
        self.iknow_onot     = False
        self.iknow_oknow    = False
        
    def send_data(self, 
            msgs:int,
            worker_name_peer_2_queues__share:Dict[Tuple[str,str], Queue], 
            name_list:List, 
            worker_name_peer_2_comm_alive__share:Dict[Tuple[str,str],bool], 
            ):
        # 发送数据到其他进程
        for name in name_list:
            if name != self.name and worker_name_peer_2_comm_alive__share[(self.name, name)]: # 通信状态为 True
                queue = worker_name_peer_2_queues__share[(self.name, name)]
                try:
                    # while not queue.empty():
                        # queue.get_nowait()
                    queue.put(msgs)
                except OSError:
                    print(f"Process {self.name} failed to send message to {name}")
                
    def receive_data(self, 
            worker_name_peer_2_queues__share:Dict[Tuple[str,str], Queue], 
            name_list:List, 
            worker_name_peer_2_comm_alive__share:Dict[Tuple[str,str],bool],
            ):
        self.msg_buffer.clear()
        # 接收数据
        for name in name_list:
            if name != self.name and worker_name_peer_2_comm_alive__share[(name, self.name)]:
                queue = worker_name_peer_2_queues__share[(name, self.name)]
                try:
                    received_msg = []
                    while not queue.empty():
                        received_msg.append(queue.get())
                    # if len(received_msg) >= 2:
                    #     self.msg_buffer.append(received_msg[-1])
                    # elif len(received_msg) == 1:
                    #     self.msg_buffer.extend(received_msg)
                    # else:
                    #     print(f"Process {self.name} received empty message from {name}")
                    self.msg_buffer.extend(received_msg)
                except OSError:
                    print(f"Process {self.name} failed to receive message from {name}")
                    
    def consensus(self): #  find the max value 
        if len(self.msg_buffer) > 0:
            self.value = max(
                max(self.msg_buffer), 
                self.value
            )
            time.sleep(self.sleep_time)
    
#region singleprocess
    # def send(self):
    #     for sender, receiver in comm_alive_dict.keys():
    #         if sender == self.name and comm_alive_dict[(sender,receiver)]:
    #             wifi[receiver].append(self.value)
                
    # def receive(self):
    #     self.msg_buffer = []
    #     self.msg_buffer.extend(wifi[self.name])
        
    # def cons(self, start_cal_time): #  find the max value 
    #     if len(self.msg_buffer) > 0:
    #         self.value = max(max(self.msg_buffer), self.value)
    #         self.comm_iter_list.append(self.value)
    #         time.sleep(self.sleep_time)
    #         end_cal_time = datetime.datetime.now()
    #         self.time_list.append((end_cal_time-start_cal_time).total_seconds())
#endregion
