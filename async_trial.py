import timeit
import asyncio


class Struct:
    def __init__(self, val):
        self.val = val

    def decr(self, amt):
        self.val = self.val - amt

    def print_val(self):
        print(self.val)


async def change_val(struct, n):
    struct.print_val()
    for _ in range(n):
        await asyncio.sleep(5)
        struct.decr(3)
        struct.print_val()


async def main():
    task1 = asyncio.create_task(asyncio.sleep(20))

    s1 = Struct(5)
    s2 = Struct(4)
    s3 = Struct(6)

    await asyncio.gather(change_val(s1, 0), change_val(s2, 1), change_val(s3, 2), asyncio.sleep(10))
    await(task1)

if __name__ == "__main__":
    start = timeit.default_timer()

    asyncio.run(main())

    stop = timeit.default_timer()
    execution_time = stop - start
    print("Program Executed in "+str(execution_time))
