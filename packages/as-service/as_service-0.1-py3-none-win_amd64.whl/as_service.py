from abc import ABC, abstractmethod
import threading
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging
import traceback


# you need to add these to derived class
# _svc_name_ = "xxxxxService"
# _svc_display_name_ = "xxxxx Service"
# _svc_description_ = 'Python Service Description'
class AppServerSvc(win32serviceutil.ServiceFramework, ABC):
    def __init__(self, args):
        try:
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.client_thread = None
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)
            self.logger().info(f'Service {self.service_name()} initialized successfully')
        except Exception as e:
            self.logger().error(f'Service {self.service_name()} initialization error: {str(e)}')
            self.logger().error(traceback.format_exc())

    def SvcStop(self):
        try:
            win32event.SetEvent(self.hWaitStop)
            if self.client_thread:
                self.client_thread.join(10)
                if self.client_thread.is_alive():
                    self.logger().warning(f'{self.service_name()} Process did not terminate')
                self.client_thread = None
        except Exception as e:
            self.logger().error(f'Service {self.service_name()} stop error: {str(e)}')
            self.logger().error(traceback.format_exc())

    def SvcDoRun(self):
        try:
            self.logger().info(f'Service {self.service_name()} is starting...')
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self.service_name(),'')
            )
            self.main()
        except Exception as e:
            self.logger().error(f'Service {self.service_name()} run error: {str(e)}')
            self.logger().error(traceback.format_exc())
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    @classmethod
    def service_name(cls):
        return getattr(cls, "_svc_name_", "unknown service")
    
    @classmethod
    def logger(cls):
        ret = getattr(cls, "_logger_", None)
        if not ret:
            ret = logging.getLogger(f"_svc_logger_{cls.service_name()}")
            setattr(cls, "_logger_", ret)
        return ret

    @abstractmethod
    def client_main(self, event:threading.Event):
        # implement of your code, it must be a service like process (do not exit directly)
        pass
            
    def process_run(self, ev):
        try:
            self.client_main(ev)
        except Exception as e:
            self.logger().error(f'{self.service_name()} Process run error: {str(e)}')
            self.logger().error(traceback.format_exc())
        finally:
            self.logger().error(f'{self.service_name()} Process run ends:')
            
    def main(self):
        try:
            ev = threading.Event()
            self.logger().info(f'{self.service_name()} Starting client_main function')
            # Run client_main in a separate Process
            self.client_thread = threading.Thread(
                target=self.process_run,
                args=(ev,),
                daemon=True
            )
            self.client_thread.start()

            # Keep the service running until stop is requested
            while True:
                # Check if service should stop
                rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)
                if rc == win32event.WAIT_OBJECT_0:
                    self.logger().info(f'{self.service_name()} Stop event received')
                    ev.set()
                    break
                if not self.client_thread.is_alive():
                    self.logger().info(f'{self.service_name()} Process ended unexpectedly')
                    break
            
            self.logger().info(f'{self.service_name()} Main loop ended')
        except Exception as e:
            self.logger().error(f'{self.service_name()} Main function error: {str(e)}')
            self.logger().error(traceback.format_exc())
            
    @classmethod 
    def cli(cls):
        try:
            win32serviceutil.HandleCommandLine(cls)
        except Exception as e:
            cls.logger().error(f'{cls.service_name()} Main script error: {str(e)}')
            cls.logger().error(traceback.format_exc())
