# Python SROS Apps

This repository contains a Python scripts that can be used with a router running SROS. The script measures the delay on different interfaces of the router.
Those scripts have been tested with 22.5R2 and 23.3.R3

Get into every folder to see more details of every script
* if-delay: see the delay measurements for different interfaces on the router.
* show-cpu: sort out apps based on cpu usage
* prefixes (pol-change): apply prefixes to two locations at once from arguments in the command line.

## Setup
Before using the script, make sure to copy the python file to the router. You can use the following command to copy the file using scp:

```
scp if-delay.py  admin@router:
```

Once the file is copied, follow the steps below to configure and run the script on the router:

1. Enter the router's configuration mode:

```
A:admin@R1# configure private
INFO: CLI #2070: Entering private configuration mode
INFO: CLI #2061: Uncommitted changes are discarded on configuration mode exit
```
2. Set the Python version for the script:

```
[pr:/configure]
A:admin@R1# python python-script "if-delay" version python3
```

3. Enable the script:

```

*[pr:/configure]
A:admin@R1# python python-script "if-delay" admin-state enable
```
4. Specify the location of the script file:

```
*[pr:/configure]
A:admin@R1# python python-script "if-delay" urls cf3:\if_delay.py
```
5. Configure the command alias for easier access:

```
*[pr:/configure]
A:admin@R1# /configure system management-interface cli md-cli environment command-alias alias "if-delay"
*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# admin-state enable
*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# python-script

 <python-script>
 "if-delay"

*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# python-script "if-delay"

```

6. Choose the mount point

```
*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# mount-point "/show"
```

7. Commit the changes

```
*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# commit
```
8. Exit the configuration mode:

```
[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# exit all
INFO: CLI #2074: Exiting private configuration mode
```

9. Execute the script:

```
[/]
A:admin@R1# pyexec "if-delay"
============================================================
Interface delay measurements
============================================================
Interface            Dynamic Delay        Operational Delay
------------------------------------------------------------
system               -                    -
to_R12               -                    10000
to_R11               -                    10000
------------------------------------------------------------
A status of "-" means delay is not configured for that interface
============================================================

[/]
A:admin@R1#
```

## Update script after changing the file

If you make any changes to the script file, follow these steps to update and enable the modified script:

```
configure private
python python-script "show-cpu-sort" admin-state disable
commit
python python-script "show-cpu-sort" admin-state enable
commit
```
## Troubleshooting
If you encounter the following error message while executing the script:

```
MINOR: MGMT_CORE #2507: Python execution failed - 'pol-change' is operational down
```
Here are some troubleshooting steps you can follow:

Check if you have copied the file to the correct location (cf3) using the `file list` command.
Ensure that you have enabled the command and alias using the `admin-state enable` command.
Double-check the file path and make sure to use backslashes `\` instead of forward slashes `/`.
If you continue to experience issues, feel free to seek further assistance.

## Testing

We have added a topology file you can use to test those scripts with containerlab.
Note: you would need a valid license file and sros image from your Nokia rep.

See ya!
