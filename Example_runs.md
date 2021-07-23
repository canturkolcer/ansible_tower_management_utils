add host: 

```
% ./tower_api_add_host.py ********** hostname linux hostname.domain 10.1.1.1 10.2.2.2 none
Hostname:  hostname
OS type:  linux
ADM IP:   10.1.1.1
EP IP:    10.2.2.2
APP:      none
responsible_teams:
Starting host adding job - Success!!!
jobs/?id=637
pending
pending
pending
pending
running
running
running
running
running
running
running
running
running
running
successful
Host adding job executed, status=successful
Starting password change job - Success!!!
jobs/?id=640
pending
pending
pending
pending
running
running
running
running
running
running
running
running
running
running
running
running
running
running
running
successful
Password change job executed, status=successful
```


onboard server to cyberark
```
% ./tower_api_onboard_host_cya.py ********** hostname
Hostname:  hostname
Starting onboarding host to cyberark (GPAM) job - Success!!!
jobs/?id=646
pending
pending
pending
pending
running
running
running
running
successful
Onboarding host to cyberark (GPAM) job executed, status=successful
```

remove host
```
% ./tower_api_remove_host.py ********** hostname
Hostname:  hostname
Starting host removing job - Success!!!
jobs/?id=649
pending
pending
pending
pending
running
running
running
running
successful
Host removing job executed, status=successful
```

