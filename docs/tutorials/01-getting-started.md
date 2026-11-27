---
doc:
  quadrant: tutorial
  verified_on: "not re-run on software 1.8.0.9"
---
# Getting started

> [!info] [UNVERIFIED] on software 1.8.0.9.

## 1. Power on

1. Connect the robot to power with cable.
2. Press the black power button, located above the power port.
3. Wait 1-2 minutes. A loud start-up sound means the robot has finished booting.


## 2. Connect over SSH

Put your laptop on the same wireless network as the robot, then log in to the perception board:

```bash
ssh <user>@<robot-ip>
```

For `<user>` and the initial password, ask a team member. 

`<robot-ip>` is the robot's wireless address, which is written on the robot. Accept the host key fingerprint on the first connection. Leave the session with `exit`.
