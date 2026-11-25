# Teardown: <Lab title>

Run these at the end of every session that started something. Check that nothing is left.

## Before you start the lab

- Note the baseline: the output of `docker system df` or `podman system df`.

## Remove

- [ ] Containers, networks and volumes of the compose project `<track>-<lab>`
- [ ] Images pulled or built only for this lab (if disk is tight)
- [ ] kind cluster `<track>-<lab>` (T4)
- [ ] VMs and their disks (T3)
- [ ] Cloud resources, through the IaC tool's destroy, and then check the console (T5)
- [ ] Trials or accounts to cancel, with their end dates (T5)

## Check

- [ ] No containers left: `docker ps -a` or `podman ps -a`, filtered by the project name
- [ ] Disk back to the baseline: `docker system df` or `podman system df`
- [ ] For cloud labs: the billing page shows no running resources
