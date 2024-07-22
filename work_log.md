

不是所有agent不收敛， 因为没有 ack 确定， 必须每个agent都收到所有ack才能结束通信。

问题记录：缺少收到所有ack才能终止通信，认为达成一致。

~~~shell
Microsoft Windows [版本 10.0.19045.2846]
(c) Microsoft Corporation。保留所有权利。

(base) F:\project\2023\07\GuoMeng\ZhuoZhi\github-collaborate\multiprocess>python test_consensu.py
sleep time -------------------- [1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2]
Worker Agent_1, comm_iter: 0, consensus value: [1, 0, 0, 0, 0]

Worker Agent_5, comm_iter: 0, consensus value: [1, 0, 0, 0, 5]

Worker Agent_2, comm_iter: 0, consensus value: [1, 2, 0, 0, 5]

Worker Agent_3, comm_iter: 0, consensus value: [1, 2, 3, 0, 5]

Worker Agent_4, comm_iter: 0, consensus value: [1, 2, 3, 4, 5]

Worker Agent_5, comm_iter: 1, consensus value: [5, 2, 3, 4, 5]
Worker Agent_1, comm_iter: 1, consensus value: [5, 2, 3, 4, 5]


Worker Agent_4, comm_iter: 1, consensus value: [5, 5, 5, 5, 5]
Worker Agent_3, comm_iter: 1, consensus value: [5, 5, 5, 5, 5]
Worker Agent_2, comm_iter: 1, consensus value: [5, 5, 5, 5, 5]



len(set(consensus_list__share)) == 1
consensus
len(set(consensus_list__share)) == 1
len(set(consensus_list__share)) == 1
consensus
consensus




~~~shell
