from flexx import flx, ui
import psutil
from scapy.all import *

ifnames = list(psutil.net_if_addrs().keys())

class PanelSend(flx.PyWidget):
    def init(self):
        with ui.VBox():
            with ui.HFix():
                ui.Label(text="Port:", flex=2)
                iface = self.root.pnl_config.get_section_config("common", "iface", "lo")
                self.lst_ifnames = ui.ComboBox(editable=False, options=ifnames, selected_key=iface, flex=2)
                ui.Label(text=" ", flex=3)
                ui.Label(text='Count:', flex=2)
                self.txt_count = ui.LineEdit(text='1', flex=2)
                ui.Label(text=" ", flex=3)
                ui.Label(text='Interval(ms):', flex=3)
                self.txt_interval = ui.LineEdit(text='0', flex=2)
                ui.Label(text=" ", flex=3)
                self.btn_send = ui.Button(text='(S)end', flex=2)

    @flx.reaction('btn_send.pointer_click')
    def send_packet(self, *events):
        try:
            packet = self.root.pnl_tx.get_pkt()
            count = int(self.txt_count.text)
            inter = float(self.txt_interval.text) / 1000
            if type(packet) in (IP, IPv6):
                ret = send(packet, iface=self.lst_ifnames.text, count=count, inter=inter, return_packets=True)
            else:
                ret = sendp(packet, iface=self.lst_ifnames.text, count=count, inter=inter, return_packets=True)
        except Exception as e:
            self.root.set_status(str(e))
        else:
            self.root.set_status(f"sent {len(ret)} packets")
            self.root.pnl_config.set_section_config("common", "iface", self.lst_ifnames.text)

