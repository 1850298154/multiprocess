

不是所有agent不收敛， 因为没有 ack 确定， 必须每个agent都收到所有ack才能结束通信。


至少第一点通信不能写成简单的 while send recv阻塞 的组合， 需要修改一下通信方式。（比如，阻塞可能需要改成软阻塞， 因为 发送局部达成达成ack， 只接受一次  ）



https://github.com/JunfengChen-robotics/multiprocess/tree/master
俊峰师兄给出的 一致性算法 框架， 我完成了很详细的研读和测试，并总结了问题和下一步改进的几个地方。 下面总结的可能不全面，还需要随着工程的开展和适配，才能发现更多需要做的工作和问题。

问题记录：
1. 现在的代码仍然，缺少收到所有ack才能终止通信，认为达成一致，并退出。
2. 底层还是使用了 Barrier.wait 进行了同步操作。
3. 真实物理隔离的主机，不能使用共享进程变量 Manager Queue，需要替换所有，还需要设计很好的通信一致性协商协议。 根据协议 while send recv阻塞 的组合， 需要修改一下通信方式。
4. 实际物理世界中，因为不分物理实体agent无法通信，而导致 一致性算法 一直无法得到所有人的认同， 需要增加更多的处理机制。

计划展开工作：
* 针对问题4.假设： 通信可靠， 没有长时间断链不上的情况。
* 针对问题3、问题2和问题1：我这边需要再详细的写一下通信方法和协议，并测试一下。 


没有ack
导致自己先结束，
不进行通信诉别人

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
