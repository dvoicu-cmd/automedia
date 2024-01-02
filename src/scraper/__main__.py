from lib.queue_pickle.queue import Queue


if __name__ == '__main__':
    print("hello scraper")


def main():
    q = Queue()
    q.load('save')
    print(q.__str__())


