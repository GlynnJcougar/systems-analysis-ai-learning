# Application Architecture

## Purpose and scope

The first release is a web application for beer tasting events. This document
records the architecture selected from the implementation recommendation.
The [approved requirements](../../analysis/requirements.md) govern behavior;
open decisions in that document are not resolved by this design.

## Architectural decision

Use a **modular monolith**: one Django application renders the interface and
enforces business rules, backed by PostgreSQL and Supabase Auth. Small amounts
of browser-side JavaScript support authentication, the leaderboard, and
connectivity handling.

```text
Browser
  |-- HTTPS --> Django application --> PostgreSQL application data
  |                   |             --> Persistent picture storage
  |                   |
  +-- Supabase Auth --+--> Verified identity for Django
```

Supabase Auth handles identity and authentication. Django checks application
permissions and owns event and scoring operations. The browser does not
receive privileged database or Supabase service credentials.

This design supports a typical small event without introducing separate
frontend and backend applications, microservices, or a real-time messaging
service. A separate single-page application and API could be considered
later if requirements justify their additional complexity.

## Application responsibilities

| Component | Responsibility | Requirements |
|---|---|---|
| Identity and profiles | Integrate Supabase sign-in, guest sessions, profile management, recovery, and access checks. | S-010–018, R-021 |
| Administration | Set up and manage administrators, enforce their permissions, and audit their changes. | S-018, R-019–022 |
| Events and participation | Manage events, event links, QR codes, membership, lifecycle, and visibility. | S-030–038, R-039, S-071–072 |
| Beers and criteria | Manage beer details, pictures, criteria, weights, defaults, and archival. | S-040–047, R-048–050, S-080–082, R-083, S-084 |
| Ratings and results | Record ratings and declines, calculate statistics and winners, and serve the leaderboard. | S-060–067, R-068, S-069–070 |
| Guest claims and merges | Associate guest sessions with participants and support conversion and existing-profile merges. | S-013–014, S-024–029 |
| Connectivity | Preserve entries on a best-effort basis, warn on timeouts, and retry or discard as required. | S-091–093 |

Keep scoring and authorization logic separate from presentation and
persistence so they can be tested independently. Validate changes on the
server, not just in the browser.

## Identity and authorization

- Support Supabase anonymous sign-in and email/password, Google, and Apple
  profile sign-in. Verify identity at the server boundary before granting
  access. Apply the approved verification and recovery rules (S-012–018,
  R-021).
- Store application roles and event membership separately from the identity
  provider. Enforce host, participant, guest, and administrator permissions
  server-side; administrators cannot create or change another participant's
  ratings (S-010–011, S-016, R-019–020, S-034–035).
- Model the event participant separately from the authentication session.
  An inactive guest may be claimed by name during an active event. Multiple
  sessions can share that participant but count once; the last successfully
  saved change to the same rating wins (S-029).
- Enforce guest access at the session level as well as by identity. When a
  guest converts to a profile, end other guest sessions' access without
  granting them the new profile's privileges (S-029).
- For an existing-profile merge, verify the guest and profile ownership,
  collect the required conflict choices, and apply application-data changes
  atomically. Preserve enough protected state to resume an interrupted flow
  while the guest session remains available (S-024–028).

Supabase Auth and the application database are separate transactional
boundaries. Provider operations cannot be assumed to roll back with a database
transaction. The merge design must handle retries and recovery explicitly,
without applying participant or rating changes twice.

## Data, scoring, and lifecycle

PostgreSQL stores application records, including profiles, event membership,
beers, criteria, ratings, saved defaults, archives, and administrative
history. Django migrations manage application data structures; Supabase
manages its authentication data. Pictures require persistent storage.

Use transactions to protect rating changes, event transitions, archival, and
the application-data portion of merges. Derive statistics and winners from
counted ratings and current weights. Use exact arithmetic for comparisons and
round only for display. A closed-event merge is allowed to recalculate results
without reopening (S-024–028, S-060–067, R-068, S-069–072, S-080–082,
R-083, S-084).

Opening a beer must apply default ratings without resetting existing choices on
repeated requests. A whole-beer decline remains in effect when a new criterion
is added (S-061–063).

## Browser and connectivity

- Render event and beer cards in Django; use JavaScript to refresh the
  leaderboard every minute and on request (S-034, S-041, S-070).
- Make a best effort to preserve entered data in local cookies and retry
  when connectivity returns. A timeout on an update or screen refresh
  triggers the local warning. Apply the specified discard rules and status
  behavior (S-091–093).
- Cookie storage is limited and can be unavailable. Do not treat it as
  guaranteed delivery or store authentication secrets in pending entries.
  The host may close without knowing about data on a disconnected device.
- Design and test the interface for the supported device classes and 200%
  browser zoom (S-090, S-095, R-096).

## Security and operational boundaries

Use HTTPS, protect secrets, restrict database access, and validate identities
and permissions at the server. If database or storage APIs are exposed
outside Django, their access policies must also enforce the approved
permissions. Record administrative actions without passwords (R-022, S-097).

Name-only guest claims are an approved impersonation risk: one minute without
a successful request does not prove that the original guest is disconnected.
The one-minute leaderboard refresh can also coincide with the inactivity
threshold. Do not present inactivity as proof of identity.

Deployment must preserve the database and picture storage across restarts.
Indefinite retention is required, but backups are not; this does not guarantee
recovery from loss (S-084).

## Remaining design work

Detailed data models, screen flows, supported browser versions, image limits,
and deployment configuration remain to be developed. Define timeout values
and the implementation of session-level guest access and resumable merges
before implementing those flows; do not silently change approved behavior.
