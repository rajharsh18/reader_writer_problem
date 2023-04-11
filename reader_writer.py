import threading
# import time

# Shared resources
readers_count = 0
readers_count_lock = threading.Semaphore()
can_read = threading.Semaphore(0)
can_write = threading.Semaphore(1)
mutex = threading.Semaphore(1)


NO_READERS = int(input("Enter the number of readers: "))
NO_WRITERS = int(input("Enter the number of writers: "))


# Reader function
def reader(id):
    global readers_count
    mutex.acquire()

    readers_count_lock.acquire()
    readers_count += 1
    if readers_count == 1:
        can_write.acquire()
    readers_count_lock.release()

    mutex.release()
    can_read.release()
    resource = open("text.txt", "r")
    content = resource.read()
    resource.close()
    
    print(f"Reader {id} is reading resource: \n{content}")
    can_read.acquire()
    
    readers_count_lock.acquire()
    readers_count -= 1
    if readers_count == 0:
        can_write.release()
    readers_count_lock.release()

# Writer function
def writer(id):
    can_write.acquire()
    mode = input("Enter the mode of writing:\na) append(a)\nb) write(w): ")
    resource = open("text.txt", mode)
    value = input(f"Enter the text you want to append by writer {id}:")
    value = "\n" + value
    resource.write(value)
    resource.close()
    can_read.release()
    can_write.release()
print("\n")
reader0 = threading.Thread(target=reader, args=(0,))
reader0.start()


reader_list = ["reader0", ]
writer_list = []
for i in range (1, NO_READERS):
    var = "reader" + str(i)
    reader_list.append(var)

for i in range (1, NO_WRITERS+1):
    var = "writer" + str(i)
    writer_list.append(var)

# Starting Function Threads
for i in writer_list:
    i = threading.Thread(target=writer, args=(int(i[-1]),))
    i.start()
    i.join()
    for j in reader_list:
        j = threading.Thread(target=reader, args=(int(j[-1]),))
        j.start()
        j.join()