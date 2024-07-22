from multiprocessing import Process, Queue, Manager, Barrier
import datetime
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import matplotlib.dates as mdates
from typing import Literal, Union, Dict, List, Tuple


from entity import Worker
from entity import MAP_SIZE
from net_plt import plot_comm_topoloty
from net_plt import plot_agent_value
from msg_log import save_msg_vol
from process_job import run_worker



    





def multiprocess_create():
    
    num_worker = 20
    num_worker = 5
    np.random.seed(42)
    # sleep_time = [random.randint(1, 5) for _ in range(num_worker)]
    sleep_time = [1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2]
    print(f"sleep time -------------------- {sleep_time}")
    workers = [
        Worker(
                id          = i+1, 
                pose        = np.random.rand(2)*MAP_SIZE, 
                sleep_time  = sleep_time[i]
            ) 
        for i in range(num_worker)]
    worker_name_peer_2_queues__share:Dict[Tuple[str,str], Queue] = {
            (worker1.name, worker2.name): Queue() 
            for worker1 in workers 
            for worker2 in workers 
            if worker1 != worker2
        }
    name_list = [
            worker.name 
            for worker in workers
        ]
    # comm_alive_dict = Manager().dict({(worker.name, other_worker.name): True if ((worker.id == (other_worker.id-1)) or (worker.id == (other_worker.id + 1))) and (worker.id != other_worker.id) == (other_worker.id+1) else False for worker in workers for other_worker in workers })
    worker_name_peer_2_comm_alive__share:Dict[Tuple[str,str],bool] = Manager().dict()
    agent_queue = Queue()
    NumAdj = 3
    NumAdj = 5
    for worker in workers:
        self_rel_dist = [
                [other, np.linalg.norm(worker.pose - other.pose)] 
                for other in workers 
                if worker != other
            ]
        soreted_worker_list:List[List[Union[Worker, float]]] = sorted(self_rel_dist, key=lambda x: x[1], reverse=False)
        for i in range(len(soreted_worker_list)):
            if i < NumAdj:
                worker_name_peer_2_comm_alive__share[(worker.name, soreted_worker_list[i][0].name)] = True
                worker_name_peer_2_comm_alive__share[(soreted_worker_list[i][0].name, worker.name)] = True
            else:
                worker_name_peer_2_comm_alive__share[(worker.name, soreted_worker_list[i][0].name)] = False  
        
    # plot communication topology
    # plot_comm_topoloty(workers, comm_alive_dict)

    consensus_list__share = Manager().list()
    consensus_list__share.extend([0 for _ in range(len(workers))])
    process_time_begin = datetime.datetime.now()
    

    
    processes = []
    final_workers = []
    barrier = Barrier(num_worker)
    for i,worker in enumerate(workers):
        p = Process(
                    target=run_worker, 
                    args=(
                        worker, 
                        worker_name_peer_2_queues__share, 
                        name_list, 
                        worker_name_peer_2_comm_alive__share, 
                        consensus_list__share, 
                        agent_queue, 
                        barrier
                    )
                )
        p.start()
        processes.append(p)
        
    for _ in range(num_worker):
        final_workers.append(agent_queue.get())

    for p in processes:
        p.join()
        
    process_time_end = datetime.datetime.now()
    
    print(f">>>>>>>>>>>>>>>>> process time: {process_time_end - process_time_begin} <<<<<<<<<<<<<<<")

    plot_agent_value(final_workers)

#region singleprocess
# def singleprocess():
#     global wifi
#     global comm_alive_dict
#     num_worker = 20
#     NumAdj = 3
#     NumAdj = 20
#     np.random.seed(42)
#     # sleep_time = [random.randint(1,5) for _ in range(num_worker)]
#     sleep_time = [1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2]
#     print(f"sleep time -------------------- {sleep_time}")
#     workers = [Worker(i+1, pose=np.random.rand(2)*MAP_SIZE, sleep_time=sleep_time[i]) for i in range(num_worker)]
#     wifi = {worker.name:[] for worker in workers}
#     comm_alive_dict = {}
#     for worker in workers:
#         self_rel_dist = [[other, np.linalg.norm(worker.pose - other.pose)] for other in workers if worker != other]
#         soreted_worker_list = sorted(self_rel_dist, key=lambda x: x[1], reverse=False)
#         for i in range(len(soreted_worker_list)):
#             if i < NumAdj:
#                 comm_alive_dict[(worker.name, soreted_worker_list[i][0].name)] = True
#                 comm_alive_dict[(soreted_worker_list[i][0].name, worker.name)] = True
#             else:
#                 comm_alive_dict[(worker.name, soreted_worker_list[i][0].name)] = False  
    

#     # plot_comm_topoloty(workers, comm_alive_dict)

#     comm_iter = 0
#     # while comm_iter < max_iter:
    
#     start_cal_time = datetime.datetime.now()
#     while True:
#         print("="*30)
#         print(f"comm iteration = {comm_iter}")
        
#         for worker in workers:
#             worker.send()
        
#         for worker in workers:
#             worker.receive()
            
#         for worker in workers:
#             worker.cons(start_cal_time)
        
#         agent_comm_cost = [worker.comm_iter_list[-1] for worker in workers]
#         print(f"comm_iter: {comm_iter}, consensus value: {agent_comm_cost}\n")
#         if len(set(agent_comm_cost)) == 1:
#             end_single_time = datetime.datetime.now()
#             print(f">>>>>>>>>>>>>>>>> process time: {end_single_time - start_cal_time} <<<<<<<<<<<<<<<")
#             break
        
#         comm_iter += 1
    
#     plot_agent_value(workers)

#endregion

if __name__ == "__main__":
    multiprocess_create()
    # singleprocess()
