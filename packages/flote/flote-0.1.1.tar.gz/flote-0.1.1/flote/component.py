from datetime import datetime
from abc import ABC, abstractmethod


VERSION = '0.1.1'
CODENAME = 'Gambiarra'
VALID_UNITS = ['fs', 'ps', 'ns', 'us', 'ms', 's']


class Sample:
    """This class represents a sample of the waves in the .vcd file."""
    def __init__(self, time, signals):
        self.time = time

        # signals is a tuple of signal name and value
        self.signals: list[tuple[str, str]] = signals


class Bus(ABC):
    """This class represents a bus in the circuit."""

    def __init__(self):
        self.assignment = None  # The assignment of the bus. It can be an expression or None.
        self.value = False  # The value of the bus.
        self.sensitivity_list: list[str] = []  # The list of buses that the current bus depends on.

    @abstractmethod
    def get_valid_values(self) -> list[str]:
        """This method returns the valid values for the bus."""

        pass

    @abstractmethod
    def insert_value(self, value) -> None:
        """This method inserts a value into the bus if it is valid"""

        pass

    def assign(self):
        """Do the assignment of the bus when not None."""

        if self.assignment:
            self.value = self.assignment()


class BitBus(Bus):
    """This class represents a bit bus in the circuit."""

    def get_valid_values(self):
        return ['0', '1']

    def insert_value(self, value) -> None:
        if value not in self.get_valid_values():
            raise ValueError(f"Invalid value '{value}'. Valid values are: {self.get_valid_values()}")

        self.value = bool(int(value))

    #* Operators overloading
    def __invert__(self) -> bool:
        return not self.value
 
    def __and__(self, other: 'BitBus') -> bool:
        return self.value and other.value

    def __or__(self, other: 'BitBus') -> bool:
        return self.value or other.value

    def __xor__(self, other: 'BitBus') -> bool:
        return self.value ^ other.value
    #* End of operators overloading

    def __repr__(self):
        return f'Assigned: {'Yes' if self.assignment else 'No'}, Current Value: {self.value}, SL: {self.sensitivity_list}'


class Component:
    """
    This class represents a circuit component.

    Attributes:
        id (str): The component id/Name.
        bits_dict (dict[str, Bit]): A dictionary with the bits of the component.
        influence_list (dict[str, list[str]]): The list of bits that each bit influences.
        time (int): The current time of the simulation.
        vcd (str): The vcd file of the simulation.
    """

    def __init__(self, id) -> None:
        self.id: str = id
        self.bus_dict: dict[str, BitBus] = {}
        self.inputs: list[str] = []
        self.influence_list: dict[str, list[str]] = {}
        self.s_time = 0
        self.time_unit: str = 'ns'
        self.samples: list[Sample] = []

    def __repr__(self):
        return f'Component {self.id}: {self.bus_dict}'

    def make_influence_list(self):
        """
        This method creates an adjacency list of the bits of the component.

        Each bit signal is a key and the value is a list of bits that the key bit influences.
        The adjacency list is used to make the bits stabilization. If a bit is changed,
        all bits that depend on it are added to the queue.
        """

        for bit in self.bus_dict:  # Create a list in the dict for each bit
            self.influence_list[bit] = []

        for bit in self.bus_dict:  # For each bit in the component
            for sensibility_signal in self.bus_dict[bit].sensitivity_list:  # For each bit that the current bit are influenced by
                self.influence_list[sensibility_signal].append(bit)  # Add the current bit to the list of bits that the sensibility bit influences

    def stabilize(self):
        """
        This method stabilizes the bits of the component.

        It is wanted new values (an input stimulus) to the component.
        """

        queue = list(self.bus_dict.keys())  #todo make dont add inputs

        while queue:
            bit_name = queue.pop(0)
            bit = self.bus_dict[bit_name]

            p_value = bit.value
            bit.assign()
            a_value = bit.value

            if p_value != a_value:  # Dynamic programming: Only add the bits that changed
                for bit_influenced in self.influence_list[bit_name]:
                    if bit_influenced not in queue:
                        queue.append(bit_influenced)

    def stimulate(self, new_values: dict[str, bool]) -> None:
        for id, new_value in new_values.items():
            if id in self.inputs:
                self.bus_dict[id].insert_value(new_value)  # Insert the new value into the bus
            else:
                raise KeyError(f"Bit signal '{id}' not found in the component.")

        self.stabilize()

        sample = Sample(self.s_time, [])

        for id, bit in self.bus_dict.items():
            sample.signals.append((bit.value, id))

        self.samples.append(sample)

    def set_time_unit(self, time_unit: str) -> str:
        if time_unit not in VALID_UNITS:
            raise ValueError(f"Invalid time unit '{time_unit}'. Valid units are: {VALID_UNITS}")

        else:
            self.time_unit = time_unit

    def wait(self, time: int) -> None:
        """This method waits for a certain time."""
        self.s_time += time

    def add_sample(self, sample: Sample):
        self.samples.append(sample)

    def dump_vcd(self):
        header_metadata = '' \
            f'$version Generated by Flote v{VERSION} - {CODENAME} $end\n' \
            f'$date {datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')} $end\n' \
            f'$timescale 1{self.time_unit} $end\n'

        header_metadata += '\n$comment Hello from Theresina. $end\n'

        header_declaration = f'\n$scope module {self.id} $end\n'

        for bit in self.bus_dict:
            header_declaration += f'\t$var wire 1 {bit} {bit} $end\n'

        header_declaration += f'$upscope $end\n\n' \

        header = header_metadata + header_declaration + f'$enddefinitions $end\n'

        datasec = ''

        for sample in self.samples:
            datasec += f"\n#{sample.time}\n\n"

            for signal in sample.signals:
                datasec += f"{int(signal[0])}{signal[1]}\n"

        return header + datasec + f'\n#{self.s_time}\n'

    def save_vcd(self, file_path: str) -> None:
        """This method saves the vcd file."""
        with open(file_path, 'w') as f:
            f.write(self.dump_vcd())
            f.close()
