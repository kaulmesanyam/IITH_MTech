# TCP/UDP Pinger

This is a simple client-server implementation for sending ping messages over TCP/UDP protocols.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
    - [Part 1: UDP Pinger](#part-1-udp-pinger)
    - [Part 2: TCP Pinger](#part-2-tcp-pinger)
- [Requirements/Execution](#requirements)

## Introduction

This application consists of two parts:

- Part 1: A UDP Pinger Client and Server.
- Part 2: A TCP Pinger Client and Server.
- UDP_Pinger/ contains client and server code where UDP is used to send pings messages from client to server
- TCP_Pinger/ contains the same thing but TCP is used instead of UDP

## Features

### Part 1: UDP Pinger

- Supports UDP protocol.
- Measures round-trip time (RTT) for each ping.
- Handles packet loss simulation.
- UDPPingerServer.py has a logic in code to simulate packet drop
- UDPPingerModifiedServer.py is the same server code but without the packet drop simulation code snippet

### Part 2: TCP Pinger

- Supports TCP protocol.
- Measures round-trip time (RTT) for each ping.
- Handles packet loss simulation.
- TCPPingerServer.py has a logic in code to simulate packet drop
- TCPPingerModifiedServer.py is the same server code but without the packet drop simulation code snippet
- TCPPingerCOncurrentServer.py is the TCP server which can handle multiple clients simultaniously

## Requirements/Execution

- Python 3.x
- For simulating packet loss at NIC, you can use the following Bash command:

```bash
sudo tc qdisc change dev eth0 root netem loss 33%

