#gnmic -a 172.18.100.9:57400 -u admin -p admin --insecure get --path nokia:state/filter
gnmic -a 172.18.100.9:57400 -u admin -p admin --insecure get --path state/filter/match-list/ip-prefix-list[prefix-list-name="ntp server list"]
