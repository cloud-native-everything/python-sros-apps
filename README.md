# python-sros-apps

Remember to copy the python script to the router first:
```
scp if-delay.py  admin@router:
```

## Setup
Example of how to add the script

```
A:admin@R1# configure private
INFO: CLI #2070: Entering private configuration mode
INFO: CLI #2061: Uncommitted changes are discarded on configuration mode exit

[pr:/configure]
A:admin@R1# python python-script "if-delay" version python3

*[pr:/configure]
A:admin@R1# python python-script "if-delay" admin-state enable

*[pr:/configure]
A:admin@R1# python python-script "if-delay" urls cf3:\if_delay.py

*[pr:/configure]
A:admin@R1# /configure system management-interface cli md-cli environment

*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# admin-state enable

*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# python-script

 <python-script>
 "if-delay"

*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# python-script "if-delay"

*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# mount-point "/show"

*[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# commit

[pr:/configure system management-interface cli md-cli environment command-alias alias "if-delay"]
A:admin@R1# exit all
INFO: CLI #2074: Exiting private configuration mode

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

```
configure private
python python-script "show-cpu-sort" admin-state disable
commit
python python-script "show-cpu-sort" admin-state enable
commit
```
## Trouble shooting
You get this error message:
```
MINOR: MGMT_CORE #2507: Python execution failed - 'pol-change' is operational down
```

Then, probably you havent copied the file to cf3, you can check this using ```file list``` command
or you haven't enable the command and alias, use ```admin-state enable```
or you have an error in the path, you should use ```\``` instad of ```/```

See ya!