import json
import logging
import time
import multiprocessing

from django.conf import settings

from kafka import KafkaConsumer, TopicPartition
from users.models import User

# Get an instance of a logger
logger = logging.getLogger('django')


class Consumer(multiprocessing.Process):
    """
    This class uses multiprocessing in order
    to not block the main threading
    """

    def __init__(self, num):
        self.num = num
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            consumer = KafkaConsumer(
                bootstrap_servers=settings.KAFKA_BROKERS,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='users-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')))

            consumer.subscribe(['user-updated', 'user-created'])
            while not self.stop_event.is_set():
                for message in consumer:
                    topic = message.topic
                    message = message.value

                    if topic == "user-updated":
                        try:
                            user = User.objects.filter(id=message['id'])
                            message.pop('id')
                            user.update(**message)
                        except User.DoesNotExist:
                            print('User does not exist')
                    elif topic == "user-created":
                        try:
                            User.objects.create(**message)
                        except BaseException:
                            pass
                    if self.stop_event.is_set():
                        break

            consumer.close()
        except KeyboardInterrupt:
            self.stop()


def main():
    # in the future we can pass the broker we want and
    # the topic so that we consume multiple topics with
    # multiprocessing
    tasks = [Consumer(0)]

    for t in tasks:
        t.start()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
