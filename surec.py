#!/usr/bin/python3
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess, contextlib



class SurecThread(QThread):
    update = pyqtSignal(str)
    def __init__(self, ebeveyn=None):
        super(SurecThread, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.komut = self.ebeveyn.komut

    def run(self):
        try:
            proc = subprocess.Popen(self.komut.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            for line in self.unbuffered(proc):
                self.update.emit(line)
        except:
            self.update.emit("> Hata")

    def unbuffered(self, proc, stream='stdout'):
        newlines = ['\n', '\r\n', '\r']
        stream = getattr(proc, stream)
        with contextlib.closing(stream):
            while True:
                out = []
                last = stream.read(1)
                if last == '' and proc.poll() is not None:
                    break
                while last not in newlines:
                    if last == '' and proc.poll() is not None:
                        break
                    out.append(last)
                    last = stream.read(1)
                out = ''.join(out)
                yield out
