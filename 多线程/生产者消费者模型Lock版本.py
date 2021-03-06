import threading
import random
import time
import logging
logging.basicConfig(level=logging.INFO)
repertory = 1000
Lock = threading.Lock()
Times = 1


class Producer(threading.Thread):
    def run(self):
        global repertory
        global Times
        while True:
            money = random.randint(100,1000)
            Lock.acquire()
            if Times >= 10:
                Lock.release()
                break
            repertory += money
            logging.info("生产者第{}次，{}挣了{}元钱,剩余{}元钱".format(Times,threading.current_thread(),money,repertory))
            Times += 1
            Lock.release()
            time.sleep(1)
class Consumer(threading.Thread):
    def run(self):
        global repertory
        global Times
        while True:
            money = random.randint(100, 1000)
            Lock.acquire()
            if repertory > money:
                repertory -= money
                logging.info("消费者第{}次，{}消耗{}元钱,剩余{}元钱".format(Times,threading.current_thread(), money, repertory))
            else:
                if Times >= 10:
                    Lock.release()
                    break
                logging.info("消费者第{}次，{}准备消耗{}元钱,剩余{}元钱，没钱啦！".format(Times,threading.current_thread(), money, repertory))
            Times +=1
            Lock.release()
            time.sleep(1)

def main():
    for x in range(3):
        t = Consumer(name="消费者线程{}".format(x))
        t.start()
    for x in range(5):
        t = Producer(name="生产者线程{}".format(x))
        t.start()
if __name__ == '__main__':
    main()
