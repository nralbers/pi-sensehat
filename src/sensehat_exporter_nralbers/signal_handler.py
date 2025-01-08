import signal

class SignalHandler:
    shutdown_requested = False
    
    def __init__(self):
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)
        
    def request_shutdown(self, *args):
        print("Shutdown request received, stopping...")
        self.shutdown_requested = True
        
    def can_run(self) -> bool:
        return not self.shutdown_requested