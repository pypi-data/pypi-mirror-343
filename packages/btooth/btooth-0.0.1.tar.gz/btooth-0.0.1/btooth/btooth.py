import asyncio
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from threading import Thread


class BluetoothEventLoop(metaclass=ABCMeta):
    @abstractmethod
    def run_async(self, coroutine):
        pass

    @abstractmethod
    def wrap_future(self, future):
        pass

    @abstractmethod
    def create_future(self):
        pass


class ThreadEventLoop(BluetoothEventLoop):
    _singleton = None

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        Thread(target=ThreadEventLoop._start_background_loop, args=(self.loop,), daemon=True).start()

    @staticmethod
    def _start_background_loop(loop):
        loop.run_forever()

    def run_async(self, coroutine):
        return asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    def wrap_future(self, future):
        return asyncio.wrap_future(future, loop=self.loop)

    def create_future(self):
        return self.loop.create_future()

    @staticmethod
    def single_thread():
        if not ThreadEventLoop._singleton:
            ThreadEventLoop._singleton = ThreadEventLoop()

        return ThreadEventLoop._singleton


class BluetoothDevice:
    _callback_executor = ThreadPoolExecutor()

    def __init__(self, client, loop = None):
        self._loop = loop if loop else ThreadEventLoop.single_thread()
        self._client = client

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        self._loop.run_async(self._client.connect()).result()

    def disconnect(self):
        self._loop.run_async(self._client.disconnect()).result()

    def read(self, service, characteristic):
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        result = self._loop.run_async(self._client.read_gatt_char(gatt_characteristic)).result()
        return result

    def write(self, service, characteristic, data):
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        self._loop.run_async(self._client.write_gatt_char(gatt_characteristic, data)).result()

    def notify(self, service, characteristic,
               callback):
        def wrap_try_catch(fn):
            def suggest(sender, data):
                try:
                    fn(sender, data)
                except RuntimeError as e:
                    message, = e.args
                    if message == "main thread is not in main loop":
                        raise RuntimeError(
                            """Error""") from e
                    raise e

            return suggest

        def do_on_callback_executor(fn):
            async def submit_to_executor(sender, data):
                await self._loop.wrap_future(BluetoothDevice._callback_executor.submit(fn, sender, data))

            return submit_to_executor

        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        self._loop.run_async(
            self._client.start_notify(gatt_characteristic, do_on_callback_executor(wrap_try_catch(callback)))
        ).result()

    def wait_for(self, service, characteristic):
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        asyncio_future = self._loop.create_future()

        def set_result_and_stop_notify(sender, data):
            asyncio_future.set_result(data)

        self._loop.run_async(self._client.start_notify(gatt_characteristic, set_result_and_stop_notify)).result()

        async def await_future_and_stop_notify():
            future = await asyncio_future
            await self._client.stop_notify(gatt_characteristic)
            return future

        return self._loop.run_async(await_future_and_stop_notify())

    def is_service_available(self, service):
        return not self._get_gatt_service(service) is None

    def address(self) -> str:
        return self._client.address

    def _find_gatt_attribute(self, service, characteristic):
        gatt_service = self._get_gatt_service(service)
        if not gatt_service:
            raise Exception("Bluetooth Service Not Found")

        gatt_characteristic = gatt_service.get_characteristic(characteristic)
        if not gatt_characteristic:
            raise Exception("Bluetooth Characteristic Not Found")

        return gatt_characteristic

    def _get_gatt_service(self, service):
        return self._client.services.get_service(service)
