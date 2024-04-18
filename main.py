import asyncio
import threading
import time


class Processor:
    def __init__(self, batch_size=10, latency=0.1):
        self.queue = asyncio.Queue()
        self.batch_size = batch_size
        self.latency = latency
        asyncio.create_task(self.process())

    async def process(self):
        while True:
            batch_data = []
            start_time = time.time()

            while len(batch_data) < self.batch_size and (time.time() - start_time) < self.latency:
                try:
                    batch_data.append(await asyncio.wait_for(self.queue.get(), timeout=0.01))
                except Exception as e:
                    await asyncio.sleep(0.001)

            if batch_data:
                print("Batch: {}".format(
                   " ".join([i[0] for i in batch_data])
                ))
                thread = threading.Thread(target=self.embedding, args=(batch_data,))
                thread.start()
                # asyncio.create_task(self.embedding(batch_data)) # Async

    def embedding(self, batch):
        time.sleep(1)
        results = {req_id: transcript[0] * 2 for req_id, transcript in batch}
        for req_id, transcript in batch:
            transcript[1].set_result(results[req_id])

    async def add_request(self, request_id, transcript):
        future = asyncio.Future()
        await self.queue.put((request_id, [transcript, future]))
        return future


async def http_request(processor, request_id, transcript):
    future = await processor.add_request(request_id, transcript)
    response = await future
    print(f"(Request: {request_id}) Result: {response}")


async def main():
    processor = Processor()
    tasks = []
    for i in range(30):
        task = asyncio.create_task(http_request(processor, str(i), "ABCED" + str(i)))
        tasks.append(task)
        await asyncio.sleep(0.04)

    await asyncio.gather(*tasks)


asyncio.run(main())
