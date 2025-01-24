import mido
import time

class MIDIOutput:
    def __init__(self, port_name=None):
        self.port = None
        self.open_port(port_name)

    def open_port(self, port_name=None):
        if port_name:
            try:
                self.port = mido.open_output(port_name)
            except IOError:
                print(f"Could not open MIDI port: {port_name}")
                self.port = None
        else:
            # Open the default MIDI output port
            try:
                self.port = mido.open_output()
            except IOError:
                print("Could not open default MIDI output port")
                self.port = None

    def close_port(self):
        if self.port:
            self.port.close()
            self.port = None

    def send_note_on(self, note, velocity=64, channel=0):
        if self.port:
            msg = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
            self.port.send(msg)

    def send_note_off(self, note, velocity=64, channel=0):
        if self.port:
            msg = mido.Message('note_off', note=note, velocity=velocity, channel=channel)
            self.port.send(msg)

    def send_control_change(self, control, value, channel=0):
        if self.port:
            msg = mido.Message('control_change', control=control, value=value, channel=channel)
            self.port.send(msg)

    def play_scale(self, scale, duration=0.5):
        if not self.port:
            print("MIDI output port is not open")
            return

        for note in scale:
            self.send_note_on(note)
            time.sleep(duration)
            self.send_note_off(note)
            time.sleep(0.1)  # Short pause between notes

def list_midi_output_ports():
    return mido.get_output_names()

# Example usage
if __name__ == "__main__":
    print("Available MIDI output ports:")
    ports = list_midi_output_ports()
    for i, port in enumerate(ports):
        print(f"{i+1}. {port}")

    midi_out = MIDIOutput()
    if midi_out.port:
        print(f"Opened MIDI port: {midi_out.port}")
        # Play a simple C major scale
        c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]
        midi_out.play_scale(c_major_scale)
        midi_out.close_port()
    else:
        print("Failed to open MIDI port")
