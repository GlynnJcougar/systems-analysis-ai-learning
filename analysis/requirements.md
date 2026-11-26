# Beer Tasting Event System: Requirements

**Status: Approved by the sponsor on 2026-11-25.** This document is the
authoritative source for approved application requirements and business rules.
Decisions marked open are not approved requirements.

## Source and interpretation

- **S** identifies a statement explicitly provided or confirmed by the
  sponsor during elicitation.
- **R** identifies an analyst recommendation accepted by the sponsor during
  elicitation. The sponsor confirmed that responses of "1" meant acceptance.
- The sponsor approved the requirements on 2026-11-25 and authorized the
  Supabase Auth amendments on the same date. Existing identifiers are retained
  for amended requirements; retired identifiers are not reused.

## Business context

The sponsor wants technology that facilitates face-to-face social interaction
with friends and family. Previous tastings were organized through text
messages, ratings were collected in PowerPoint, and results were calculated
in Excel. The process was manual.

The desired outcome is an easier way to organize and run tastings, capture
independent ratings, display statistics, and declare winners. Venues are
potential future stakeholders. A future freemium model may help cover
operating costs, but pricing has not been decided.

## First-release scope

- **S-001:** Support beer tasting events from creation and invitation through
  participation, scoring, closing, and review of results.
- **S-002:** Provide all first-release features without payment or subscription.
- **S-003:** Defer social sharing, premium features, graphs, criterion
  comments, and the directory for selecting existing profile users.
- **S-004:** Support beer only in the first release. Non-beer categories and
  venue use are possible future capabilities.
- **S-005:** The typical event has approximately 10 participants and 10 beers.
  Support for larger events is not a stated first-release requirement; no
  maximum has been specified.

## Roles and accounts

- **S-010:** A profile user can create an event and becomes its host. Only
  users with profiles can host.
- **S-011:** An invited person can join as a guest. A guest identity is limited
  to one event; participation in a subsequent event requires a new guest
  identity or a profile.
- **S-012:** Guest names are globally unique. A guest receives a default name
  such as Guest01 and can override it. Guests use Supabase Auth anonymous
  sign-in rather than a guest password.
- **S-013:** A guest can return using their existing anonymous session in the
  same browser. If the session is lost before conversion, the guest identity
  cannot be recovered; its event participation and ratings remain in the
  event. The person can join as a new guest only while joining is allowed.
  Do not provide the former name-and-password guest return link.
- **S-014:** A guest can convert to a profile during or after the event. The
  guest's existing participation and ratings remain associated with the
  profile, and the event remains available for future review, subject to the
  merge rules below.
- **S-015:** Provide profile sign-in through Supabase Auth using email and
  password, Google, and Apple in the first release. Google and Apple sign-in
  must be highly secure. A profile requires a globally unique name; email is
  required for email/password sign-in and otherwise is optional. Location,
  phone number, and picture are optional. A profile user can edit their own
  name and optional details and manage their sign-in credentials, but cannot
  delete their own profile.
- **S-016:** Event members can view participants' profiles, except that
  participants' email addresses and phone numbers are hidden from other
  members.
- **S-017:** Use Supabase Auth to manage authentication and store profile
  passwords as hashes. Either managed or self-hosted Supabase Auth is
  acceptable. Do not require email verification where Supabase permits it;
  verification is required before an anonymous guest adds a password.
- **S-018:** On first system run, prompt the person running the system to
  create the initial administrator account. Administrators can create or
  appoint additional administrators.
- **R-019:** Administrators can view and manage all events, beers, and
  profiles, including host actions, but cannot create or change another
  participant's ratings.
- **R-020:** Administrators can appoint or remove administrators; at least one
  active administrator must remain.
- **R-021:** Provide self-service password reset by email for profile users
  who sign in with email and password.
- **R-022:** Record who performed administrative changes and when, without
  recording passwords.
- **R-023: Retired.** Administrator-assisted guest sign-in with a
  name-matching password is replaced by S-012 and S-013.
- **S-024:** Support transferring or merging a guest's event participation into
  an existing profile. Require the guest to sign in to that profile to prove
  ownership before the transfer or merge.
- **S-025:** When the guest and profile have conflicting ratings for the same
  beer and criterion, let the user choose which rating to keep. Also let the
  user choose when one identity rated a criterion and the other declined it.
- **S-026:** After a merge, count the guest and profile as one participant,
  including for the two-participant scoring threshold. Associate beers created
  by the guest with the profile, preserving the creator's permitted actions.
  Transfer non-conflicting participation and ratings to the profile.
- **S-027:** Permit a merge involving a closed event and recalculate its
  results and winners. This is an exception to the usual closed-event scoring
  restriction.

## Events, invitations, and participation

- **S-030:** An event requires a title, date, and location. Description,
  picture, and suggested start time are optional. The host can start the event
  at any time, regardless of the suggested date or time.
- **S-031:** Set a system default time zone when the initial administrator
  account is created. Administrators can change the default later, and hosts
  can override it for an event.
- **S-032:** In the first release, provide an event URL the host can copy and
  a QR code linking to the event. The host can share the URL using their own
  text or email application. Direct invitation sending is not required in the
  first release.
- **S-033:** Prompt a new person following an event link to create a profile,
  with joining as a guest as a secondary option. A returning profile user who
  signs in through the link returns to the event.
- **S-034:** Show created events as cards to signed-in profile users. Any
  signed-in profile user can join a visible event before it closes, including
  after it starts. A guest identity can access only its associated event.
- **S-035:** Within their event, guests can see the beers, criteria,
  participants, ratings, results, and live leaderboard, subject to the
  profile-contact visibility rule. Guests have the same contribution
  permissions as other participants.
- **S-036:** A person following a closed-event link can see the winner, if
  any, without signing in. Joining a closed event is not allowed.
- **S-037:** The host can start an event once at least one other participant
  has joined and at least two beers and one criterion have been added.
- **S-038:** Only the host can edit event details, subject to administrator
  permissions.
- **R-039:** The host can edit event details before and during the event; a
  closed event must be reopened first.

## Beers and criteria

- **S-040:** Participants and the host can add and edit beers before the event
  starts. During an event, only the host can add or edit beers. A closed
  event must be reopened before changing its beers.
- **S-041:** Beer name is required. Company or brewer, type, origin, and
  picture are optional. Display beers as cards on the event page.
- **S-042:** Before an event starts, any participant can add, rename, or
  remove criteria. During the event, only the host can do so. Only the host
  can change criterion weights, subject to administrator permissions.
- **S-043:** An event must have at least one criterion and cannot have
  duplicate criterion names.
- **S-044:** Initial beer criteria are Label Design, Aroma, Appearance,
  Flavor, Mouthfeel, and Overall.
- **S-045:** A person adding a criterion can mark it as a default for future
  events. Saved defaults are offered to all hosts for future events; saving
  one does not add it to other existing events. Defaults previously removed
  from an event remain removed.
- **S-046:** A criterion's weight is a whole number from 1 through 10 and
  defaults to 5.
- **S-047:** Removing a criterion removes its ratings from active results and
  recalculates totals. Renaming a criterion treats it as a new entry but copies
  its existing values within that event; the saved default remains unchanged.
  Changing a weight recalculates results.
- **R-048:** Archive removed criteria and their ratings so the host can restore
  them while the event is open.
- **R-049:** New saved defaults are not automatically added to an event that
  has ever been closed, even after reopening; the host can add criteria
  manually.
- **R-050:** Allow event and beer pictures to be uploaded from a device. Image
  format and size limits are deferred.

## Ratings and results

- **S-060:** Ratings become available only after the event starts. The host
  can rate beers like other participants.
- **S-061:** Ratings are whole numbers from 1 through 10 and default to 5.
  Opening a beer for rating immediately counts the participant's default
  ratings. While the event is open, participants can change their ratings.
- **S-062:** A participant can decline to rate an individual criterion or an
  entire beer and can later change that decision while the event is open.
- **S-063:** When a criterion is added to an active event, apply its default
  rating of 5 for participants who have opened the relevant beers and
  recalculate scores. Ratings that are not counted do not prevent other
  participants' ratings from being used.
- **S-064:** For each beer and criterion, calculate the average of counted
  ratings multiplied by the criterion weight. Omit a criterion from that
  beer's total when it has no counted ratings.
- **S-065:** A beer qualifies for scoring after at least two participants
  each have a counted rating for at least one criterion on that beer.
  Automatic 5s count toward this threshold. Below it, show the beer as
  unscored, while allowing current statistics to be displayed.
- **S-066:** For each beer and criterion, show the minimum, maximum, and
  average using weighted scores.
- **S-067:** For each criterion, the winning beer has the highest weighted
  criterion score. The overall winning beer has the highest sum of weighted
  criterion scores. Declare a tie when the highest calculated values are equal.
- **R-068:** Exclude beers below the two-participant threshold from criterion
  and overall winners. If no beer qualifies when the event closes, show no
  winner.
- **S-069:** Display scores with zero decimal places; round halfway values up.
  Determine ties using full calculated values rather than displayed values.
- **S-070:** Show a live leaderboard with the leader for each criterion and
  the overall leader. Refresh it every minute and provide a manual refresh.
- **S-071:** The host can close a started event even if ratings are incomplete.
  Closing prevents further scoring and declares winners where eligible, except
  for the merge and recalculation allowed by S-027. A closed event with no
  counted ratings has no winner and remains available for review.
- **S-072:** Only the host can reopen an event, subject to administrator
  permissions. Existing ratings remain available; subsequent scoring can
  change the winners. S-027 also permits a merge to change winners without
  reopening.

## Deletion, restoration, and retention

- **S-080:** Only the host can delete an event, subject to administrator
  permissions. The host or a beer's creator can delete that beer while its
  event is open. Require two warnings before deleting an event or beer.
- **S-081:** Archive deleted events and beers and their associated information.
  The host can see deleted events and beers marked as deleted and can restore
  them. Other users cannot see them while deleted.
- **S-082:** A beer's event must be reopened before restoration when it is
  closed. Restored beer scores recalculate immediately using the restored
  ratings.
- **R-083:** Restoring an event returns it to its previous stage with its
  participants, beers, ratings, and results intact.
- **S-084:** Retain events, results, and archived information indefinitely.
  Backups are not required.

## Connectivity, validation, and usability

- **S-090:** The system is web-hosted and supports desktop and mobile browsers
  on PC, iOS, and Android. Either a locally owned server or cloud hosting is
  acceptable initially; no provider has been selected.
- **S-091:** An internet connection is required. If connectivity is lost,
  make a best effort to preserve entries in local cookies and otherwise tell
  the user that an internet connection is required. Automatically submit
  preserved entries when connectivity returns.
- **S-092:** Discard preserved entries if the event closed or the relevant
  beer or criterion changed or was removed while the participant was offline.
  Discarded entries disappear without a status or notification.
- **S-093:** Show participants whether entries are saved locally, submitted
  successfully, or unable to submit. Warn the host when closing with
  outstanding data using the wording "Disconnected participant error."
  The host may close before all data is collected.
- **S-094:** Alert users and ask them to try again when required information
  is missing or a duplicate name is entered.
- **S-095:** Text should be readable for older participants.
- **R-096:** Check that text remains readable and functionality remains usable
  at 200% browser zoom on supported devices.

## Open decisions and risks

- Exact supported browser versions, hosting provider, availability targets,
  and profile-user event limits are undecided.
- Image format and size limits remain undecided.
- The exact detection and circumstances for the disconnected-participant
  closing warning need clarification: a server may not know about entries
  stored only on a disconnected device.
- Guests who lose their anonymous session before conversion cannot recover
  their identity or use it to access their event; their existing ratings remain.
- Supabase-managed authentication requires service configuration and, for
  email recovery and verification, email delivery. Self-hosting also requires
  operating and maintaining Supabase.
- Where email verification is not required, address ownership may be
  unconfirmed. Email-based recovery still depends on access to that address.
- Indefinite retention without backups does not guarantee recovery after data
  loss.
