# # coding=utf-8
# import sys
# import multiprocessing
# import time
# import threading
# import onedrive_operation as op		#if you don't have Onedrive operation code you can delete it
# op= op.str_operation()			#if you don't have Onedrive operation code you can delete it
#
# # global variable: Queue for putting tasks inside
# g_queue = multiprocessing.Queue()
#
# def init_queue():
#     print("init g_queue start")
#     while not g_queue.empty():
#         g_queue.get()
#     for _index in range(3):		#size of the queue:3  , you can adjust it if you like but also need to change size of thread_list and process_list below
#         g_queue.put(_index)
#     print("init g_queue end")
#     return
#
#
# # IO-bound task: download a file from Onedrive
# def task_io(task_id):
#     print("IOTask[%s] start" % task_id)
#     while not g_queue.empty():
#         op.download2(5)	         #IMPORTANT: special function only for test: download a file with index 5 from Onedrive， Or you can put another IO-bound type task here
#         try:
#             data = g_queue.get(block=True, timeout=1)
#             print("IOTask[%s] get data: %s" % (task_id, data))
#         except Exception as excep:
#             print("IOTask[%s] error: %s" % (task_id, str(excep)))
#     print("IOTask[%s] end" % task_id)
#     return
#
# if __name__ == '__main__':
#     print("cpu count:", multiprocessing.cpu_count(), "\n")
#
#     print(u"running the IO-bound task directly")
#     init_queue()
#     time_0 = time.time()
#     task_io(0)
#     print(u"END：", time.time() - time_0, "\n")
#
#     print("Running IO-bound task using Multi-thread")
#     init_queue()
#     time_0 = time.time()
#     thread_list = [threading.Thread(target=task_io, args=(i,)) for i in range(3)]
#     for t in thread_list:
#         t.start()
#     for t in thread_list:
#         if t.is_alive():
#             t.join()
#     print("END：", time.time() - time_0, "\n")
#
#     print("Running IO-bound task using Multi-processing")
#     init_queue()
#     time_0 = time.time()
#     process_list = [multiprocessing.Process(target=task_io, args=(i,)) for i in range(3)]
#     for p in process_list:
#         p.start()
#     for p in process_list:
#         if p.is_alive():
#             p.join()
#     print("END：", time.time() - time_0, "\n")
#
