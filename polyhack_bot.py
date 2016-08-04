"""
Polyhack bot: IRC bot
"""

#!/usr/bin/env python3

# PolyHack bot
# Copyright (C) 2011 : Robert L Szkutak II - http://robertszkutak.com
# Copyright (C) 2016 : Hugo Genesse - https://github.com/svieg
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import socket
import requests

HOST = "irc.freenode.org"
PORT = 6667

NICK = "PolyHackBot"
IDENT = "PolyHackBot"
REALNAME = "Url bot pour shorten les liens par ton maitre Svieg"
MASTER = "svieg"
CHANNEL = "#polyhack_"

PAYLOAD = {"longUrl": "",
           "apiKey": "YOUR PO.ST API KEY",  # You need to change that
           "format": "txt"}

GIRLS = {"fille", "chick", "femme"}

READ_BUFFER = ""

S = socket.socket()
S.connect((HOST, PORT))

S.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
S.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
S.send(bytes("JOIN <YOUR_CHANNEL>\r\n", "UTF-8"))
S.send(bytes("PRIVMSG %s :Hello Master\r\n" % MASTER, "UTF-8"))

while 1:
    MESSAGE = S.recv(1024)
    try:
        READ_BUFFER = MESSAGE.decode('UTF-8')
    except UnicodeDecodeError:
        try:
            READ_BUFFER = MESSAGE.decode('iso-8859-1')
        except UnicodeDecodeError:
            READ_BUFFER = MESSAGE.decode('cp1252')
    TEMP = str.split(READ_BUFFER, "\n")
    READ_BUFFER = TEMP.pop()

    for line in TEMP:
        line = str.rstrip(line)
        line = str.split(line)

        if len(line) > 1:
            if line[0] == "PING":
                S.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        if len(line) >= 4:
            if line[3] == ":!bot":
                sender = ""
                for char in line[0]:
                    if char == "!":
                        break
                    if char != ":":
                        sender += char
                size = len(line)
                i = 3
                MESSAGE = ""
                while i < size:
                    MESSAGE += line[i] + " "
                    i = i + 1
                MESSAGE.lstrip(":")
                S.send(bytes("PRIVMSG {} Yo :{} \r\n".format(CHANNEL, line[0]),
                             "UTF-8"))
            if line[3].find("http") is not -1:
                if line[3][0] is ":":
                    line[3] = line[3][1:]
                PAYLOAD["longUrl"] = line[3]
                r = requests.get("http://po.st/api/shorten", params=PAYLOAD)
                S.send(bytes("PRIVMSG {} {} \r\n".format(CHANNEL, r.text),
                             "UTF-8"))
            for index, i in enumerate(line):
                if line[index] in GIRLS:
                    S.send(bytes("PRIVMSG {} :{} \r\n".format(CHANNEL,
                                                              "JOKE SEXISTE"),
                                 "UTF-8"))
                print(line[index])
