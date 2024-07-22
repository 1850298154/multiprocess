from multiprocessing import Process, Queue, Manager, Barrier
import datetime
import networkx as nx
from typing import Literal, Union, Dict, List, Tuple


from entity import Worker
from entity import MAP_SIZE
from net_plt import plot_comm_topoloty
from net_plt import plot_agent_value
from msg_log import save_msg_vol


def run_worker(
            worker:Worker, 
            worker_name_peer_2_queues__share:Dict[Tuple[str,str], Queue], 
            name_list:List, 
            worker_name_peer_2_comm_alive__share:Dict[Tuple[str,str],bool], 
            consensus_list__share:List, 
            agent_queue:Queue, 
            barrier:Barrier,
        ):
    comm_iter = 0
    # while comm_iter < max_iter:
    start_cal_time = datetime.datetime.now()
    while True:
        # 发送数据
        worker.send_data(
            msgs                                 = worker.value, 
            worker_name_peer_2_queues__share     = worker_name_peer_2_queues__share, 
            name_list                            = name_list, 
            worker_name_peer_2_comm_alive__share = worker_name_peer_2_comm_alive__share,
        )


        if False:
            pass
        elif worker.iknow_onot == True:
            pass
        elif worker.iknow_onot == False:
            # 接收数据
            worker.receive_data(
                    worker_name_peer_2_queues__share        = worker_name_peer_2_queues__share, 
                    name_list                               = name_list, 
                    worker_name_peer_2_comm_alive__share    = worker_name_peer_2_comm_alive__share,
                )
        
        barrier.wait()
        # 实现consensus
        worker.consensus()
        if worker.value ==0:
            raise("value")
        consensus_list__share[worker.id - 1] = worker.value
        worker.comm_iter_list.append(worker.value)
        
        
        # 打印接收到的数据
        print(f"Worker {worker.name}, comm_iter: {comm_iter}, consensus value: {consensus_list__share}\n")
        end_cal_time = datetime.datetime.now()
        worker.time_list.append((end_cal_time - start_cal_time).total_seconds())
        if len(set(consensus_list__share)) == 1:
            worker.iknow_onot = True
            
            print('len(set(consensus_list__share)) == 1')
            print('consensus')
            if self.only
            
            if worker.iknow_oknow == True:
                agent_queue.put(worker)
                break
        
        comm_iter += 1
    
    # plot_agent_value(time_list, comm_iter_list)
    # agent_queue.put(worker)