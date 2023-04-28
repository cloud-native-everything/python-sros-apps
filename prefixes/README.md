# usage

```
A:admin@R1# /pol-change "{10.2.2.5/32, 172.3.8.3/32}"
Adding prefix to policy-options prefix-list 'ntp server list':  10.2.2.5/32
Adding prefix to policy-options prefix-list 'ntp server list':  172.3.8.3/32
Adding prefix to filter match-list ip-prefix-list 'ntp server list':  10.2.2.5/32
Adding prefix to filter match-list ip-prefix-list 'ntp server list':  172.3.8.3/32

[/]
A:admin@R1# admin show configuration /configure filter match-list ip-prefix-list "ntp server list"
    prefix 2.2.2.0/24 { }
    prefix 3.3.3.3/32 { }
    prefix 10.2.2.5/32 { }
    prefix 172.3.8.3/32 { }

[/]
A:admin@R1# admin show configuration /configure policy-options prefix-list "ntp server list"
    prefix 2.2.2.0/24 type exact {
    }
    prefix 3.3.3.3/32 type exact {
    }
    prefix 10.2.2.5/32 type exact {
    }
    prefix 172.3.8.3/32 type exact {
    }
```
