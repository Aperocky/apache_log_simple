# APACHE LOG SIMPLE

Log processing and data analysis, made *simple*

This is a utility tool that let you know in the shortest time possible of the big picture, while still allowing you to dig deep into individual logs.

I'll make this a pypl repository - working on it.

## Syntax

`> log_processor $your_log_file $utility_command`

example: 

`log_processor ../access.log.2018-07-02 os_type_count`

## Utilities Command List.

Command | Usage | Output
--- | --- | ---
unique_ip_num | Prints out the number of unique ip found in the log | `600`
unique_ip | Prints out all unique IPs | `[8.8.8.8, 8.8.4.4, ...]`
unique_ip_sorted | Prints out all unique IP in sorted manner | `[8.8.4.4, 8.8.8.8, ...]`
os_type_count | Prints out count for different OSes |  `Windows: 301 Mac: 116 Linux: 66 Android: 84 iOS: 63 Others: 133`
os_type_full_count | Prints out count for fully considered OS strings | `Linux; Android 8.1.0; Pixel XL Build/OPM4.171019.021.D1: 2, iPad; CPU OS 11_2_6 like Mac OS X: 1 ....`
os_type_ip | Prints out ip associated with different OS full strings | `Linux; Android 8.1.0; Pixel XL Build/OPM4.171019.021.D1: [8.8.8.8, 8.8.4.4], iPad; CPU OS 11_2_6 like Mac OS X: [69.69.69.69] ....`
Expanding ... | Coming soon | `I'll KISS`