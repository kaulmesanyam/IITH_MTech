# Mininet Topology Setup Guide

This guide provides step-by-step instructions for setting up the Mininet environment and running a custom topology. Make sure you have the necessary dependencies installed before proceeding.

## Prerequisites

- [Mininet](http://mininet.org/download/) installed
- [Python 2.x or 3.x](https://www.python.org/downloads/) installed
- Basic understanding of Mininet and networking concepts

## Instructions

1. **Clone the Repository:**
   ```
   git clone https://bitbucket.org/jvimal/bgp/src/master/  

   ```
   cd mininet-topology
   If you want to run the scripts written by us then you can replace those those scripts in the code-base with ours and proceed 
   
2. **Navigate to the BGP Folder:**
   ```
   cd bgp
   ```
3. **Run mininet Topology Script:**
   ```
   sudo python bgp.py
   or
   sudo python bgp_modified.py
   ```
4. **Launch Rogue AS (Optional):**
   ```
   ./start_rogue.sh
   ```
5. **Launch webserver simulations using any one of the 3 scripts (Optional):**
   ```
   ./website.sh
   ./website2.sh

   ```
6. **Clean-up:**
   ```
    exit
    sudo mn -c
   ```

    
   
