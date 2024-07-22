
import os


def save_msg_vol(file_name, msg_data, comm_iter):
    save_path = os.path.join(os.path.abspath(
                        os.path.join(os.path.abspath(__file__), "..","..")),
                        "data/", 
                        file_name)
    
    with open(save_path, 'a+') as f:
        f.write(f"Communication Iter={comm_iter}\n")
        for agent, msg_nums in msg_data.items():
            write_data = f"agent={agent}\tmsg_nums={msg_nums}\n\n"
            f.write(write_data)
            