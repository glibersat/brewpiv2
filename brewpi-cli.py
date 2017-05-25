#!/usr/bin/env python3
import logging
import time

import coloredlogs

from brewpiv2.controller import (
    BrewPiController,
    BrewPiControllerManager
)

from brewpiv2.commands import (
    BeerModeCommand, FridgeModeCommand,
    ProfileModeCommand,
    OffModeCommand, VersionRequestCommand,
    ListAvailableDevicesCommand,
    ListInstalledDevicesCommand,
    InstallDeviceCommand,
    UninstallDeviceCommand
)

from brewpiv2.messages.decoder import RawMessageDecoder
from brewpiv2.messages import (
    VersionMessage,
)
from brewpiv2.constants import (
    DeviceFunction, DeviceType,
    HardwareType
)

from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import HSplit, Container
from prompt_toolkit.layout.margins import PromptMargin


from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.shortcuts import create_eventloop

from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FillControl, UIControl, TokenListControl
from prompt_toolkit.layout.controls import UIContent
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.margins import NumberredMargin, ScrollbarMargin

from pygments.token import Token

from prompt_toolkit.contrib.completers import WordCompleter

command_completer = WordCompleter([
    'mode',
    'fridge',
    'beer',
    'profile',
    'macro'
], ignore_case=True)





from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.keys import Keys


from logging import Handler

class ConsoleHandler(Handler):
    def __init__(self, buffer, cli):
        super().__init__(level=logging.DEBUG)
        self.buffer = buffer
        self.cli = cli

    def emit(self, record):
        log_entry = self.format(record)
        self.buffer.insert_text(log_entry)
        self.buffer.newline()
        self.cli.request_redraw()

import argparse
from argparse import ArgumentParser
from prompt_toolkit.buffer import AcceptAction


class StatusBarArgumentParser(ArgumentParser):
    def __init__(self, prog, app):
        self.app = app
        super().__init__(prog=prog, add_help=False)

    def error(self, message):
        raise Exception(message)


class BrewPiCommandParser:
    def __init__(self, app):
        self.app = app

        self.parser = StatusBarArgumentParser(prog="brewpi", app=app)
        subparsers = self.parser.add_subparsers(dest="cmd")

        # Mode
        parser_mode = subparsers.add_parser(name='mode', app=app, help="switch control mode")
        parser_mode.add_argument('mode', help="switch to mode", choices=['profile', 'beer', 'fridge'])
        parser_mode.add_argument('setpoint', help="mode setpoint", type=float)

        # Devices
        parser_mode = subparsers.add_parser(name='devices', app=app, help="query and install devices")
        parser_mode.add_argument('action', help="switch to mode", choices=['list', 'install', 'uninstall'])

        # Macro
        parser_mode = subparsers.add_parser(name='macro', app=app, help="run a macro")
        parser_mode.add_argument('file', help="Name of macro file")
        parser_mode.add_argument('name', help="Name of the macro")

    def parse(self, cli, buffer):
        curr_line = buffer.document.current_line
        self.parse_line(cli, curr_line, buffer)

    def parse_line(self, cli, line, buffer):
        args = None
        line = line.split()
        try:
            args, leftovers = self.parser.parse_known_args(args=line)
        except argparse.ArgumentError as e:
            cli.logger.error(e)
        except Exception as e:
            cli.logger.error(e)

        cmd_to_send = None
        if args is not None:
            if args.cmd == 'mode':
                if args.mode == "fridge":
                    cmd_to_send = FridgeModeCommand(setpoint=args.setpoint)
                elif args.mode == "beer":
                    cmd_to_send = BeerModeCommand(setpoint=args.setpoint)

            elif args.cmd == 'macro':
                import yaml
                try:
                    with open("{0}.bpm".format(args.file), 'r') as stream:
                        try:
                            data = yaml.load(stream)
                        except yaml.YAMLError as exc:
                            cli.logger.info(exc)

                        # now run macro
                        try:
                            cmds = data[args.name]

                            for cmd in cmds:
                                self.parse_line(cli, cmd, buffer)
                                cli.logger.info("[{0}] -> {1}".format(args.file, cmd))
                                time.sleep(0.1)
                        except KeyError:
                            cli.logger.warn("No macro named <{0}> in file <{1}.bpm>".format(args.name,
                                                                                            args.file))
                except FileNotFoundError as e:
                    cli.logger.warn("Coudln't open macro file <{0}.bpm>".format(args.file))

        if cmd_to_send is not None:
            cli.raw_msg_logger.info("> " + cmd_to_send.render())
            self.app.controller.send(cmd_to_send)

        buffer.reset(append_to_history=True)


        return True

from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.styles.from_pygments import style_from_pygments
from pygments.styles import get_style_by_name

from brewpiv2.controller import MessageHandler


class UIMessageHandler(MessageHandler):
    def __init__(self, cli):
        self.cli = cli
        self.app = cli.app
        super()

    def available_device(self, anInstalledDeviceMessage):
        self.cli.logger.info("Available device")

    def installed_device(self, anAvailableDeviceMessage):
        self.cli.logger.info("Installed device")

    def log_message(self, aLogMessage):
        self.cli.logger.info("Read Log")

    def control_settings(self, aControlSettingsMessage):
        self.cli.logger.info("Read settings")

    def control_constants(self, aControlConstantsMessage):
        self.cli.logger.info("Read constants")

    def temperatures(self, aTemperaturesMessage):
        self.app.buffers['STATE'].reset()

        if aTemperaturesMessage.beer_setpoint:
            self.app.buffers['STATE'].insert_text("Beer Mode: {0}° -> {1}°".format(aTemperaturesMessage.beer_temp or "[not connected]",
                                                                                   aTemperaturesMessage.beer_setpoint))
        elif aTemperaturesMessage.fridge_setpoint:
            self.app.buffers['STATE'].insert_text("Fridge Mode: {0}° -> {1}°".format(aTemperaturesMessage.fridge_temp or "[not connected]",
                                                                                     aTemperaturesMessage.fridge_setpoint))
        if aTemperaturesMessage.room_temp:
            self.app.buffers['STATE'].insert_text(" | Room Temp: {0}".format(aTemperaturesMessage.room_temp))

        if aTemperaturesMessage.beer_annotation:
            self.cli.logger.info(aTemperaturesMessage.beer_annotation)

        if aTemperaturesMessage.fridge_annotation:
            self.cli.logger.info(aTemperaturesMessage.fridge_annotation)


class BrewPiApplication(Application):
    def get_prompt_tokens(self, cli):
        tokens = []
        if self.controller:
            tokens += [
                (Token.Name, 'BrewPi'),
                (Token.At,       '@'),
                (Token.Host,     'localhost'),
                (Token.Colon,    ':'),
                (Token.Path,     self.controller.serial.port)
            ]
            if self.controller.is_connected:
                tokens += [
                    (Token.IsConnected, '[OK]')
                ]
        else:
            tokens += [
                (Token.Toolbar, "No BrewPi Connected."),
            ]

        tokens += [
            (Token.Pound, '> ')
        ]

        return tokens


    def __init__(self):
        self.command_parser = BrewPiCommandParser(self)

        self.buffers = {
            DEFAULT_BUFFER: Buffer(completer=command_completer, enable_history_search=True, history=InMemoryHistory(), accept_action=AcceptAction(self.command_parser.parse)),
            'MESSAGES': Buffer(),
            'RESULT': Buffer(),
            'STATE': Buffer(),
        }

        self.registry = load_key_bindings()
        self.registry.add_binding(Keys.ControlC, eager=True)(self._on_request_shutdown)
        self.registry.add_binding(Keys.ControlQ, eager=True)(self._on_request_shutdown)


        self.layout = HSplit([
            # One window that holds the BufferControl with the default buffer on the
            # left.
            VSplit([
                HSplit([
                    Window(content=TokenListControl(get_tokens=lambda cli: [(Token.Title, 'Command Result')]), height=D.exact(1)),
                    Window(content=BufferControl(buffer_name='RESULT'),
                           wrap_lines=True,
                           left_margins=[ScrollbarMargin()]),
                ]),

                Window(width=D.exact(1), content=FillControl('|', token=Token.Line)),
                HSplit([
                    Window(content=TokenListControl(get_tokens=lambda cli: [(Token.Title, 'Raw Protocol Messages')]), height=D.exact(1)),
                    Window(content=BufferControl(buffer_name='MESSAGES', lexer=PygmentsLexer(JsonLexer)),
                           wrap_lines=True,
                           left_margins=[NumberredMargin()],
                           right_margins=[ScrollbarMargin()])
                ])

            ]),

            VSplit([
                Window(content=TokenListControl(get_tokens=self.get_prompt_tokens), height=D.exact(1), dont_extend_width=True),
                Window(content=BufferControl(buffer_name=DEFAULT_BUFFER), height=D.exact(1), dont_extend_height=True),
            ]),
            Window(content=BufferControl(buffer_name='STATE'), height=D.exact(1), dont_extend_height=True)
        ])

        super().__init__(layout=self.layout,
                         buffers=self.buffers,
                         key_bindings_registry=self.registry,
                         mouse_support=True,
                         style=style_from_pygments(get_style_by_name('emacs'),
                                                   style_dict={
                                                       Token.Toolbar: '#ffffff bg:#333333',
                                                       Token.Title: '#ffffff bg:#000088',
                                                       # User input.
                                                       Token:          '#ff0066',

                                                       # Prompt.
                                                       Token.Name: '#884444 italic',
                                                       Token.At:       '#00aa00',
                                                       Token.Colon:    '#00aa00',
                                                       Token.Pound:    '#00aa00',
                                                       Token.Host:     '#000088 bg:#aaaaff',
                                                       Token.Path:     '#884444 underline',
                                                       # Make a selection reverse/underlined.
                                                       # (Use Control-Space to select.)
                                                       Token.SelectedText: 'reverse underline',
                                                   }),
                         use_alternate_screen=True)


        # BrewPi Stuff
        self.controller_manager = BrewPiControllerManager()
        self.msg_decoder = RawMessageDecoder()

        self.controller = None


    def _on_request_shutdown(self, event):
        """
        Pressing Ctrl-Q or Ctrl-C will exit the user interface.
        Setting a return value means: quit the event loop that drives the user
        interface and return this value from the `CommandLineInterface.run()` call.
        Note that Ctrl-Q does not work on all terminals. Sometimes it requires
        executing `stty -ixon`.
        """
        event.cli.set_return_value(None)

from pygments.lexers import JsonLexer

class BrewPiShell(CommandLineInterface):
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument("device_uri", help="physical device (i.e. /dev/ttyACM0) or address (e.g. socket://10.1.1.1:6666)")

        self.app = BrewPiApplication()
        self.loop = create_eventloop()

        # Logging
        self.logger = logging.getLogger("brewpiv2")
        self.logger.setLevel(level=logging.INFO)
        self.logger.handlers = []

        self.logger.addHandler(ConsoleHandler(self.app.buffers['RESULT'], self))

        self.raw_msg_logger = logging.getLogger("raw-messages")
        self.raw_msg_logger.setLevel(level=logging.DEBUG)
        handler = ConsoleHandler(self.app.buffers['MESSAGES'], self)
        # handler.setFormatter(coloredlogs.ColoredFormatter('%(message)s'))
        self.raw_msg_logger.addHandler(handler)

        super().__init__(application=self.app, eventloop=self.loop)

        self.patch_stdout_context(raw=False, patch_stdout=True, patch_stderr=True)

        self.msg_handler = UIMessageHandler(self)

    def run(self):
        args = self.parser.parse_args()

        self.loop.run_in_executor(self._listen_for_events)

        try:
            self.app.controller = BrewPiController(args.device_uri)
            self.app.controller.connect()

            self.app.controller.send(ListAvailableDevicesCommand())

            super().run()
        finally:
            self.loop.close()


    def _listen_for_events(self):
        while not self.is_returning:
            if self.app.controller:
                if self.app.controller.is_connected:
                    for raw_message in self.app.controller.process_messages():
                        self.raw_msg_logger.info(raw_message)
                        for msg in self.app.msg_decoder.decode_controller_message(raw_message):
                            self.msg_handler.accept(msg)

            time.sleep(0.1)




shell = BrewPiShell()
shell.run()

exit(0)





if __name__ == "__main__":

    manager = BrewPiControllerManager()

    msg_decoder = RawMessageDecoder()
#    controller = BrewPiController("socket://192.168.0.46:6666") # SOUDE
    controller = BrewPiController("socket://192.168.0.40:6666") # TEST
    controller.connect()

    #controller.send(UninstallDeviceCommand(slot=2))
    # time.sleep(1)

    # controller.send(ListAvailableDevicesCommand())

    controller.send(FridgeModeCommand(setpoint=63.0))

    # controller.send(InstallDeviceCommand(slot=1, address="28EEBCB816160144",
    #                                      assigned_to_chamber=True, assigned_to_beer=False,
    #                                      function=DeviceFunction.CHAMBER_TEMP,
    #                                      hardware_type=HardwareType.TEMP_SENSOR)


    # controller.send(InstallDeviceCommand(slot=2, assigned_to_chamber=True,
    #                                      assigned_to_beer=False, function=DeviceFunction.CHAMBER_HEATER,
    #                                      hardware_type=HardwareType.DIGITAL_PIN, pin=16))


    # while True:
    #     # Update manager
    #     for new_controller in manager.update():
    #         new_controller.connect()
    #         time.sleep(1.0)

    #         # new_controller.send(ListAvailableDevicesCommand(with_values=False))
    #         # new_controller.send(ListInstalledDevicesCommand(with_values=False))

    #         # new_controller.send(ProfileModeCommand(setpoint=10.0))
    #         # cmd = InstallDeviceCommand(slot=3, address="28CE4BC20700004F", assigned_to_chamber=1,
    #         #                            assigned_to_beer=1, function=DeviceFunction.ROOM_TEMP,
    #         #                            hardware_type=HardwareType.TEMP_SENSOR, pin=0)

    #         cmds = []
    #         # cmds.append(UninstallDeviceCommand(slot=3))
    #         # cmds.append(UninstallDeviceCommand(slot=0))
    #         # cmds.append(UninstallDeviceCommand(slot=2))



    #         # cmds.append(InstallDeviceCommand(slot=1, address="28EEBCB816160144", assigned_to_chamber=True,
    #         #                                  assigned_to_beer=False, function=DeviceFunction.CHAMBER_TEMP,
    #         #                                  hardware_type=HardwareType.TEMP_SENSOR))


    #         # cmds.append(InstallDeviceCommand(slot=2, assigned_to_chamber=True,
    #         #                                  assigned_to_beer=False, function=DeviceFunction.CHAMBER_HEATER,
    #         #                                  hardware_type=HardwareType.DIGITAL_PIN, pin=0))

    #         cmds.append(FridgeModeCommand(setpoint=80.0))

    #         for cmd in cmds:
    #             new_controller.send(cmd)
    #             time.sleep(.5)


    #         # cmd = UninstallDeviceCommand(slot=6, address="284B647F0800008A", assigned_to_chamber=0,
    #         #                              assigned_to_beer=1, hardware_type=HardwareType.TEMP_SENSOR, pin=0)
    #         # new_controller.send(cmd)

    #     for port, controller in manager.controllers.items():
    #         if controller.is_connected:
    #             for raw_message in controller.process_messages():
    #                 for msg in msg_decoder.decode_controller_message(raw_message):
    #                     LOGGER.debug(msg)

    #     time.sleep(0.1)