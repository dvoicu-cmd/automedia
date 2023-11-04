from project_automatic.scripts.lib.queue_pickle import queue

def main():
    q = queue.Queue()
    q.load('save')
    print(q.__str__())


main()


