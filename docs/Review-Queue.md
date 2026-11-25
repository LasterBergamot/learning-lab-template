# Review Queue

Recall questions for spaced repetition. Remembering something in a review session is what
moves it into long-term memory; re-reading notes does much less.

## How it works

- `session-log` adds two to five questions here at the end of each session, written from what
  *you* explained.
- `review-quiz` asks the questions whose **Next due** date has passed. It doesn't show the
  answer until you have tried.
- Answered well: the interval doubles (1 → 2 → 4 → 8 → 16 → 32 days). Missed: it goes back
  to 1 day.
- Each row links to where the answer lives: a lab's `NOTES.md` or an assessment competency ID.

## Format

| Question | Lab/Competency | Next due | Interval |
|---|---|---|---|
| *Example: Why does a client reject a certificate whose issuer it doesn't trust?* | *security/tls-pki* | *YYYY-MM-DD* | *1d* |

## Queue

<!-- review-queue:start -->
| Question | Lab/Competency | Next due | Interval |
|---|---|---|---|
<!-- review-queue:end -->

The queue is empty until the first learning session.
