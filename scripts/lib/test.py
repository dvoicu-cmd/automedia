from queue_pickle import queue


def main():
    q = queue.Queue()
    q.put("HE HE")
    q.put("WHAT")
    q.put("GE GE")
    q.put("AAAAAAAA")
    q.put("YOOOOOO!")

    q.save("nananana")

    q.put("WHATS GOOD MY")
    q.put("THAT FUNNY")

    print("BEFORE LOAD: "+q.__str__())


    q.load("nananana")
    print("AFTER LOAD: "+q.__str__())

    print(q.contains("HE HE"))
    print(q.contains("MY Nice guy"))

    return 0

main()