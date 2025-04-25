# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2022/8/8 0008 13:30
import json
import amqpstorm
import orjson

from funboost.consumers.base_consumer import AbstractConsumer
from funboost.publishers.rabbitmq_amqpstorm_publisher import RabbitmqPublisherUsingAmqpStorm


class RabbitmqConsumerAmqpStorm(AbstractConsumer):
    """
    使用AmqpStorm实现的，多线程安全的，不用加锁。
    """
    BROKER_KIND = 0
    BROKER_EXCLUSIVE_CONFIG_KEYS = ['prefetch_count']

    def _shedual_task(self):
        # noinspection PyTypeChecker
        def callback(amqpstorm_message: amqpstorm.Message):
            body = amqpstorm_message.body
            # self.logger.debug(f'从rabbitmq的 [{self._queue_name}] 队列中 取出的消息是：  {body}')
            self._print_message_get_from_broker('rabbitmq', body)
            body = orjson.loads(body)
            kw = {'amqpstorm_message': amqpstorm_message, 'body': body}
            self._submit_task(kw)
            if self._stop_flag:
                rp.channel.stop_consuming()

        rp = RabbitmqPublisherUsingAmqpStorm(self.queue_name)
        rp.init_broker()
        prefetch_count = self.broker_exclusive_config.get('prefetch_count', self._concurrent_num)
        rp.channel_wrapper_by_ampqstormbaic.qos(prefetch_count)
        rp.channel_wrapper_by_ampqstormbaic.consume(callback=callback, queue=self.queue_name, no_ack=False)
        rp.channel.start_consuming(auto_decode=True)

    def _confirm_consume(self, kw):
        # noinspection PyBroadException
        try:
            kw['amqpstorm_message'].ack()  # 确认消费
        except BaseException as e:
            self.logger.error(f'AmqpStorm确认消费失败  {type(e)} {e}')

    def _requeue(self, kw):
        print(kw['amqpstorm_message'].delivery_tag)
        kw['amqpstorm_message'].nack(requeue=True)
