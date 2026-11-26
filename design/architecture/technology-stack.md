# Technology Stack

## Decision

Use the following stack for the first implementation. This is an architecture
decision, not a change to the [approved requirements](../../analysis/requirements.md).
The initial dependency ranges and setup instructions are in the
[application foundation](../../implementation/src/README.md).

| Area | Choice | Purpose |
|---|---|---|
| Application | Python and Django | Server-rendered application, validation, business operations, and migrations |
| Interface | HTML, CSS, and JavaScript | Responsive pages, authentication interactions, polling, and connectivity handling |
| Authentication | Supabase Auth | Anonymous guests, email/password, Google and Apple sign-in, and password recovery |
| Database | PostgreSQL in the Supabase project | Relational application data, transactions, and archival |
| Pictures | Persistent storage accessible to the application | Event, beer, and profile pictures across restarts |
| Automated tests | Django test framework and Playwright | Business and integration tests plus browser-based tests |

The application can run on a locally owned server or in the cloud. Supabase
Auth can be managed or self-hosted, as permitted by S-017 and S-090. A
self-hosted Supabase deployment adds operational responsibilities; a managed
service adds a provider dependency. The hosting choice remains open.

## Why this stack

Django provides a straightforward server-rendered architecture and keeps
business logic in one application. PostgreSQL supports relational constraints
and transactional application changes. Supabase Auth provides the specified
sign-in methods while allowing Django to enforce application authorization.
Polling satisfies the leaderboard requirement without a separate real-time
infrastructure (S-070).

Alternatives considered:

- **Separate JavaScript frontend and API:** more independent deployment and
  interface flexibility, but more moving parts for this teaching application.
- **SQLite for application data:** simple for a single instance, but Supabase
  already uses PostgreSQL and PostgreSQL provides a consistent relational
  deployment target for local or cloud hosting.
- **Locally managed Django authentication:** simpler as a standalone Django
  deployment, but does not meet the approved Supabase Auth decision (S-017).

## Dependencies and development environment

Implementation will need Python, Django, a PostgreSQL driver, Supabase client
and server-side identity-verification support, an image-processing library, a
QR-code library, and Playwright with its browser dependencies. Choose
compatible, supported versions during setup.

Development also requires access to a Supabase project or a local Supabase
environment, PostgreSQL, a browser, and persistent development storage.
Docker can run a local Supabase environment. Google and Apple sign-in need
provider configuration; email-based recovery and verification need email
delivery. Store configuration and secrets outside source control.

## Deployment and storage

Deploy Django with HTTPS and access to PostgreSQL, Supabase Auth, and persistent
picture storage. A durable filesystem volume is suitable for a single-server
deployment; a host without such a volume needs persistent object storage or
another durable option. Keep the application database and pictures across
restarts and deployments.

Separate application database access from Supabase's authentication data;
use appropriately restricted credentials and do not expose privileged keys to
the browser. If direct database or storage APIs are enabled, configure their
access policies consistently with the application permissions.

## Verification strategy

- Unit-test scoring, eligibility, rounding, authorization, and validation
  against requirement IDs.
- Integration-test persistence, event lifecycle, archive/restore, guest
  claiming, transactional merges, and concurrent changes.
- Browser-test the supported sign-in flows, event participation, leaderboard
  refresh, timeout handling, mobile layouts, and 200% zoom.
- Exercise provider-dependent authentication flows in a configured test
  environment; use test credentials rather than committing secrets.

## Open decisions and risks

- Exact package versions, hosting provider, supported browser versions,
  image formats and size limits, and availability targets remain open.
- Name-only claims can impersonate another guest, and the inactivity
  threshold does not prove disconnection (S-029).
- Unverified email can leave address ownership unconfirmed; email recovery
  depends on access to that address (S-017, R-021).
- Cookie-based offline preservation is best effort, and automatic retries
  must obey the approved discard rules (S-091–093).
- Persistent storage is required, but backups are not required. Data loss
  may therefore be unrecoverable (S-084).
