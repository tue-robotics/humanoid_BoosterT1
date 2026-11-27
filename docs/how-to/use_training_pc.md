---
doc:
  order: 5
  quadrant: how-to
---
# Use the training PC (draft)

> [!warning] Review needed
> This page has not been reviewed by the team yet.

The lab has one shared training PC (RTX 5090, 32 GB GPU memory). Everyone logs in as the same user. Trainings go through a queue, `tq`, that runs one job at a time.

## Connect

1. Turn on the TU/e VPN.
2. Log in. For the user, address and password, ask a team member.

```bash
ssh <user>@<training-pc>
```

3. Keep your work in your own folder in the home directory.

## Start a training

Go to your project folder, activate its environment, and put `tq submit --name <you> --` in front of the training command:

```bash
cd ~/<your-folder>/<project>
tq submit --name <you> -- uv run train <task> --num-envs 4096
```

The job starts from that folder, with the environment of your shell, when the GPU is free. You can log out: it runs in its own tmux session. `export TQ_NAME=<you>` replaces `--name`.

## Commands

| Command | Use |
|---|---|
| `tq submit --name <you> [--hours N] -- <command>` | Add a training to the queue |
| `tq list` | Running job, queue and GPU use |
| `tq logs <id> -f` | Follow the output of a job |
| `tq attach <id>` | Watch a running job, read-only (`Ctrl+B`, then `D` to leave) |
| `tq cancel <id> --name <you>` | Cancel your queued or running job |
| `tq board` | GPU hours per person |

## Rules

- Never start a training outside the queue: it blocks everyone's queued jobs and is reported in Discord.
- One training runs at a time. Each person can have one running and one queued job.
- First come, first served, but your second job waits behind everyone's first job.
- A job is stopped at its time limit: 24 hours by default, 72 at most (`--hours`).
- `--name` is not checked. Use `--force` on someone else's job only when the owner agrees or cannot be reached.
- The disk is shared and fills up: delete checkpoints, videos and environments you no longer need.
