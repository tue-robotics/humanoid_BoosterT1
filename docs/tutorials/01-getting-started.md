---
doc:
  quadrant: tutorial
  verified_on: "firmware T1 2.3.4, 2026-09-22 (steps 3-5); steps 1-2 from a 2026-09-08 session, not yet re-run"
---

## 1. Power on

1. Connect the robot to power with cable.
2. Press the black power button, located above the power port.
3. Wait 1-2 minutes. A loud start-up sound means has finished booting.


## 2. Connect over SSH

Put your laptop on the same wireless network as the robot (Tech_united), then log in to the perception board:

```bash
ssh <user>@<robot-ip>
```

`<user>` and the initial password are given in the vendor manual ([VD-[[]]01 §Operation Manual > Connect to Robot > Connect via Terminal]). `<robot-ip>` is the robot's wireless address on your network. Accept the host key fingerprint on the first connection. Leave the session with `exit`.

## Where to go next

--//--