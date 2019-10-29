#!/usr/bin/env python
# encoding: utf-8

import mastersyncronizer as mtsync
import slavesyncronizer as svsync

if __name__ == "__main__":
    print("Enter the choice 1 - for Master Setup")
    print("Enter the choice 2 - for Slave Setup")
    choice = int(input("Enter Your Choice: "))

    if choice == 1 : 
        mtsync.MasterInitializer()
    elif choice == 2:
        svsync.SlaveIntializer()
    else:
        print("Please Try again...")
