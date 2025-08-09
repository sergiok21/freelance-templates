class ProcessMonitor:
    def open_window(self, port):
        """Знаходить PID процесу, що слухає заданий порт."""
        for proc in psutil.process_iter(attrs=["connections"]):
            for conn in proc.info["connections"]:
                if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
                    app = Application().connect(process=proc.pid)
                    app.top_window().set_focus()
                    return proc.pid
        return None
