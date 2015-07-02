

from datetime import datetime, timedelta
import socket

from .opus20 import Frame

class Opus20FakeServer(object):
    """
    A TCP server imitating (faking) the
    behaviour of a Lufft OPUS20 device.
    """
    def __init__(self, host='', port=52015):
        self.host = host
        self.port = port
        self.communication_samples = []

    def bind_and_serve(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(1)
        try:
            while True:
                conn, addr = self.s.accept()
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    input_frame = Frame(data)
                    output_frame = self.react_to_input_frame(input_frame)
                    conn.sendall(output_frame.data)
                conn.close()
        except KeyboardInterrupt:
            pass
        finally:
            self.s.close()

    def react_to_input_frame(self, input_frame):
        output_frame = None
        input_frame.validate()
        in_props = input_frame.props
        for sample in self.communication_samples:
            sample_props = sample['in'].props
            if in_props.cmd != sample_props.cmd:
                continue
            if in_props.payload != sample_props.payload:
                continue
            output_frame = sample['out']
            break
        if output_frame is None:
            # 0x10 - Unknown CMD
            output_frame = Frame.from_cmd_and_payload(in_props.cmd, b"\x10")
        return output_frame

    def feed_with_communication_log(self, l2p_frames_file):
        """ Feed the fake server with l2p frames stored in a communication log file """
        num_incoming, num_outgoing = 0, 0
        num_short, num_long = 0, 0


        def gt(dt_str):
            dt, _, us= dt_str.partition(".")
            dt= datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
            us= int(us.rstrip("Z"), 10)
            return dt + timedelta(microseconds=us)
            #return dt
        
        with open(l2p_frames_file) as fp:

            timestamp = None
            incoming = None
            outgoing = None

            for line in fp:

                line = line.strip()
                if not line: continue

                kind = None
                if line.startswith('Timestamp'):
                    kind = 'timestamp'
                    timestamp = gt(line.split('  ')[1].replace(' ', 'T'))
                elif line.startswith('<- '):
                    kind = 'incoming'
                    num_incoming += 1
                elif line.startswith('-> '):
                    kind = 'outgoing'
                    num_outgoing += 1

                if kind in ('incoming', 'outgoing'):
                    frame_bytes = bytes(int(byte, 16) for byte in line[3:].split())
                    frm = Frame(frame_bytes)
                    try:
                        frm.validate()
                    except Exception as e:
                        print(e)
                        pdb.set_trace()

                if kind == 'incoming':
                    incoming = frm
                elif kind == 'outgoing':
                    outgoing = frm
                    self.communication_samples.append({'ts': timestamp, 'in': incoming, 'out': outgoing})

