"""Provide support for Nanosurf Accessory Interface Electronics
Copyright (C) Nanosurf AG - All Rights Reserved (2021)
License - MIT"""

from array import array
from dataclasses import dataclass

import nanosurf.lib.devices.i2c.bus_master as i2c
from nanosurf.lib.devices.i2c import chip_24LC32A
from nanosurf.lib.devices.i2c import chip_PCA9548
from nanosurf.lib.devices.i2c.config_eeprom import DataSerializer, ConfigEEPROM


class GenericIDEEPROM(ConfigEEPROM):

    def __init__(self, bus_addr:int = 0x57) -> None: 
        super().__init__(bus_addr, version=1)
        self.bt_number = "BT00000"   
        self.sn_number = "000-00-000"

    def serialize(self) -> bytearray:
        self._serialize_version()
        self._serialize(self.bt_number, DataSerializer.Formats.String)
        self._serialize(self.sn_number, DataSerializer.Formats.String)
        return self._write_data_bytes

    def deserialize(self, data:bytearray) -> bool:
        if self._deserialize_version(data) == 1:
            self.bt_number = self._deserialize(DataSerializer.Formats.String)
            self.sn_number = self._deserialize(DataSerializer.Formats.String)
        else:
            raise ValueError(f"Unknown layout version: {self._read_layout_version}")
        return True


@dataclass
class AccessoryNode:
    bus : 'AccessoryBus' = None
    port : int = -1
    sub_port : int = -1

class AccessoryDevice():
    """ This class is the base class for all accessory compatible devices

    A minimal device implementation is the ID_EEPROM at reserved bus addr 0x57.
    Most of all other addresses are free for other device chips.
    Exceptions are: 0x70, 0x71, these are reserved to the bus multiplexers
    """

    def __init__(self, bt_number:str, serial_no:str = "", id_eeprom_version:int = 1):
        """ This class stores the information found in the id eeprom of each slave device

            As standard identification a bt-number is read from the device
            Optional a serial number is provided

        Parameters
        ----------
        bt_number : string
            identifier number of the device type. it has to be in the form of "BT00000"
        id_eeprom_version : int, optional
            configuration version of the id-eeprom section. If not provided its assumed 
            to be version 1 which has a BTNumber ad a SerialNo as content.
        bus_node 
        """

        self._version = id_eeprom_version
        self._assigned_bt_number = bt_number
        self._assigned_serial_no = serial_no
        self._bt_number = ""
        self._serial_no = ""
        self._bus_node:AccessoryNode = None
        self._is_connected = False
        self._id_eeprom = chip_24LC32A.Chip_24LC32A(0x57)

    def assign_bus_node(self, bus_node : AccessoryNode):
        self._bus_node = bus_node
        if self._bus_node is not None:
            self._bus_node.bus.assign_chip(self._id_eeprom)
        else:
            self._id_eeprom.bus_address = None
    
    def connect(self, check_assigned_bt_number:bool=True, init_device:bool = True) -> bool:
        try:
            if self.is_connected(check_assigned_bt_number=check_assigned_bt_number, dont_use_cached_connection=True):
                if self._assigned_serial_no != "":
                    self._is_connected = self._serial_no == self._assigned_serial_no
            if self._is_connected and init_device:
                self.init_device()
                
            return self._is_connected
        except IOError:
            return False

    def is_connected(self, check_assigned_bt_number:bool=True, dont_use_cached_connection:bool = False) -> bool:
        if self._bus_node is None:
            raise IOError("Access to device without assigned bus_node!")
        
        if not self._is_connected or not dont_use_cached_connection:
            self._is_connected = self._id_eeprom.is_connected()

        if self._is_connected and check_assigned_bt_number:
            self._read_id_eeprom()
            self._is_connected = self._bt_number == self._assigned_bt_number

        return self._is_connected

    def init_device(self):
        raise Warning("This Function should be reimplemented by Device implementation class")

    def get_bt_number(self) -> str:
        """ Returns the slave devices identification string.
            It's usual form is "BTxxxxx"

        Returns
        -------
        bt_number: str
            identification string

        """
        # check if bt number is already read, otherwise read eeprom content
        if len(self._bt_number) <= 0:
            self._read_id_eeprom()
        return self._bt_number

    def get_serial_number(self) -> str:
        """ Return the slave devices (optional) serial number.
            It's usual form is "xxx-xx-xxx"

         Returns
         -------
            serial_number: str
                 serial number as string or empty string if no serial number is defined

        """
        # check if bt number is already read, otherwise read eeprom content
        if len(self._bt_number) <= 0: 
            self._read_id_eeprom()
        return self._serial_no

    def get_assigned_serial_number(self) -> str:
        return self._assigned_serial_no

    def get_assigned_bt_number(self) -> str:
        return self._assigned_bt_number

    def _read_id_eeprom(self) -> bool:
        if self._bus_node is None:
            raise IOError("Access to device without assigned bus_node!")
        
        if not self._is_connected:
            raise IOError("Access to device without assigned bus_node!")
        
        self._serial_no = ""
        self._bt_number = ""
        
        id_eeprom_data = self._id_eeprom.memory_read_bytes(0, 20)

        if len(id_eeprom_data) > 10:
            self._version = id_eeprom_data[0]
            
            if self._version != 1:
                raise IOError("AccessoryDevice: Unknown id header version detected.")
            
            try:
                self._bt_number = array('B', id_eeprom_data[2:2+id_eeprom_data[1]]).tobytes().decode()
                if id_eeprom_data[9] > 0:
                    self._serial_no = array('B', id_eeprom_data[10:10+id_eeprom_data[9]]).tobytes().decode()
                else:
                    self._serial_no = ""
            except Exception:
                self._serial_no = ""
                self._bt_number = ""
        return len(self._bt_number) > 0
    
    def initialize_id_eeprom(self, bt_number:str, serial_no:str, config:ConfigEEPROM = None, overwrite_already_initialized_eeprom:bool = False) -> bool:
        """ Writes a initial configuration to eeprom. Handle with care!
            If a configuration is passed then this is written to the eeprom.
            seriasl_no and bt_number is needed when no configuration is passed
            To force a reprogramming of the eeprom, 'overwrite_already_initialized_eeprom' has to be set to True,
            otherwise only empty eeproms are written
        """
        if self._bus_node is None:
            raise IOError("Access to device without assigned bus_node!")
        
        # check if eeprom contains data, abort if overwrite is not enabled
        if not overwrite_already_initialized_eeprom:
            if self._read_id_eeprom():
                return False
            
        if config is None:
            if not bt_number.startswith("BT") or len(bt_number) != 7:
                raise ValueError("bt_number must have the format BT01234")
            if len(serial_no) < 10 or len(serial_no) > 11:
                raise ValueError("serial_no must have the format 000-00-000")
            config = GenericIDEEPROM()
            config.bt_number = bt_number
            config.sn_number = serial_no
            
        self._bus_node.bus.assign_chip(config)
        done = config.store_config()
        return done


class AccessoryBus(i2c.I2CBusMaster):
    """ This is the main class to get access to accessory devices connected to an accessory bus (AB). 
        Devices can be connected directly to the bus, after a bus multiplexer or even a secondary multiplexer

        Connect to a AB by its bus number. Then access to a slave device of this AI can be granted by select_port()

        slave devices are identified by get_slave_device_id().
        To talk to a slave device, specific class drivers have to be build.

    """
    def __init__(self, bus_id:i2c._I2CBusID):
        """ This is the main class to get access to an accessory interface (AI) and its slave devices.

        Parameters
        ----------
        spm
            reference to the connected spm COM class for MobileS or a reference to studio 

        """
        super().__init__(spm_root=None, bus_id=bus_id, 
            instance_id=i2c.I2CInstances.CONTROLLER, 
            master_type=i2c.I2CMasterType.ACCESSORY_MASTER, 
            bus_speed=i2c.I2CBusSpeed.kHz_Default)
        self._active_port = -1
        self._active_sub_port = -1
        self._chip_mux_primary:chip_PCA9548.Chip_PCA9548= None 
        self._chip_mux_secondary:chip_PCA9548.Chip_PCA9548 = None 
        self._available_ports = 0

    def init_bus(self) -> bool:
        self._active_port = -1
        self._chip_mux_primary = None 
        self._chip_mux_secondary = None 

        # check if a bus multiplexer is there
        self._chip_mux_primary = chip_PCA9548.Chip_PCA9548(0x70)
        self.assign_chip(self._chip_mux_primary, port=0)
        if not self._chip_mux_primary.is_connected():
            self._chip_mux_primary = None
            self._available_ports = 1
        else:
            self._available_ports = self._read_primary_port_count()
        return self._available_ports >= 1

    def _read_primary_port_count(self) -> int:
        assert self._chip_mux_primary is not None, "No primary bus multiplexer chip is assigned."
        return 4

    def get_port_count(self) -> int:
        """ return the number of ports the connected interface has

        Returns
        -------
        int
            number of ports available on this accessory bus

        """
        return self._available_ports

    def get_bus_addr(self) -> int:
        """ returns the communication bus address. Used for further I2C communication with a slave

        Returns
        -------
        int
            bus_address - identification number to be used for I2C communication

        """
        return self._bus_id

    def select_port(self, port_nr: int, sub_port:int = -1):
        """ opens the port to communication with a slave device at port
            Only one port at a given time can be selected. all further slave communication goes through the selected port
            Port 0 is assigned to accessory interface internal configuration and should be used carefully

        Parameters
        ----------
        port_nr : int
            identification number of the port to be used
        """
        if self._chip_mux_primary is not None:
            self._active_port = port_nr
            self._chip_mux_primary.reg_control = 1 << port_nr

            if self._chip_mux_secondary is not None:
                self._active_sub_port = sub_port
                self._chip_mux_secondary.reg_control = 1 << sub_port
        else:
            self._active_port = -1
            self._active_sub_port = -1


    def is_device_connected(self) -> bool:
        """ check if a  device is connected to selected port

        Returns
        -------
        bool
            returns True if a device is found on selected port, otherwise False

        """
        device = self.get_generic_device()
        return device.is_connected(check_assigned_bt_number=False, dont_use_cached_connection=True)

    def get_generic_device(self) -> AccessoryDevice:
        """ read the identification information from the device on selected port
            The information is read from the id eeprom and stored in a AISlaveIDHeader class

         input:
            none
         return:
            device - a generic AccessoryDevice class 
        """
        device = AccessoryDevice(bt_number="")
        self.assign_device_to_current_port(device)
        return device
    
    def assign_device_to_current_port(self, device:AccessoryDevice):
        """ assign a device to current selected bus and port"""
        device.assign_bus_node(AccessoryNode(bus=self, port=self._active_port, sub_port=self._active_sub_port))
        device.is_connected(check_assigned_bt_number=False, dont_use_cached_connection=True)
        
    def find_device_by_serial_no(self, serial_nr: str, device: AccessoryDevice) -> bool:
        """ Auto select the port where a device with 'serial_nr' is connected

            Parameters:
            -----------
            serial_nr: str
                The serial number of the connected device to find. Need the form 'xxx-yy-zzz'

            returns True if found otherwise False
        """
        device_found = False
        try:
            for port_nr in range(1, self.get_port_count()+1):
                self.select_port(port_nr)
                self.assign_device_to_current_port(device)
                device.is_connected(check_assigned_bt_number=True, dont_use_cached_connection=True)
                if serial_nr == device.get_serial_number():
                    device_found = True
                    break
        except IOError:
            pass
        device.assign_bus_node(AccessoryNode())
        return device_found

    def find_device_by_bt_number(self, bt_number: str, device: AccessoryDevice) -> bool:
        """ Auto select the port where a device with 'serial_nr' is connected

            Parameters:
            -----------
            serial_nr: str
                The serial number of the connected device to find. Need the form 'xxx-yy-zzz'

            returns True if found otherwise False
        """
        device_found = False
        try:
            for port_nr in range(1, self.get_port_count()+1):
                self.select_port(port_nr)
                self.assign_device_to_current_port(device)
                device.is_connected(check_assigned_bt_number=False, dont_use_cached_connection=True)
                if bt_number == device.get_bt_number():
                    device_found = True
                    break
        except IOError:
            pass
        device.assign_bus_node(AccessoryNode())
        return device_found

    def find_device(self, device: AccessoryDevice) -> bool:
        """ Auto select the port where a device with 'serial_nr' is connected

            Parameters:
            -----------
            serial_nr: str
                The serial number of the connected device to find. Need the form 'xxx-yy-zzz'

            returns True if found otherwise False
        """
        device_found = False
        try:
            for port_nr in range(1, self.get_port_count()+1):
                self.select_port(port_nr)
                self.assign_device_to_current_port(device)
                device.is_connected(check_assigned_bt_number=False, dont_use_cached_connection=True)
                if device.get_assigned_serial_number() == device.get_serial_number():
                    device_found = True
                    break
        except IOError:
            pass
        device.assign_bus_node(AccessoryNode())
        return device_found

    def get_current_port(self) -> int:
        return self._active_port

    def assign_chip(self, chip: 'I2CChip', port: int = -1):
        """ Tell the software that a certain 'chip' is connected to current or specific port
        
        Parameters:
        -----------
        chip: class of I2CChip 
        port: int  
            if no port number is given (or -1) then  assume the chip is connected to current selected port
        """
        chip.assigned_ai_port = port if port>=0 else self._active_port
        super().assign_chip(chip)


    # overwrite base functions to support automatic port switching-----------------------------------------

    def activate_chip(self, chip: 'I2CChip'):
        if  chip.assigned_ai_port != self._active_port:
            self.select_port(chip.assigned_ai_port)
        super().activate_chip(chip)
