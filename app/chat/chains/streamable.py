from flask import current_app
from threading import Thread
from queue import Queue
from app.chat.callbacks.stream import StreamingHandler


class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        print(input)
        def task(app_context):  
            app_context.push()            
            self(input, callbacks=[handler])

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token