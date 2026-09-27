# SE05 — Who's Asking?

**Category:** Social Engineering  
**Difficulty:** Easy–Medium  
**Points:** 150

---

## Description

Someone is asking for information.

They seem legitimate.

They sound legitimate.

They might even have the right credentials.

But there's one question you should always ask:

**Who's asking?**

Investigate the request and determine whether the person is actually authorized.

Find the flaw.

Find the flag.

**Flag format:** `cebroid{...}`

---

## Hint

> Authority can be forged. Context is harder to fake.

---

## Organizer Notes

The player receives a fictional request containing information such as:

- Name
- Position
- Department
- Employee ID
- Ticket number
- Manager
- Contact information

Most of the information should appear legitimate.

One or two details should subtly contradict the organization's actual structure.

The player must identify the inconsistency and use it to recover the flag.

### Example

**Caller:** Adrian Cole  
**Claimed role:** IT Security Administrator  
**Employee ID:** NX-2194  
**Ticket:** FIN-4821  
**Manager:** Marcus Bell

However, Finance tickets use the `SEC-` prefix, not `FIN-`.

The inconsistency points toward the flag.

> **The question isn't what they're asking. It's who's asking.**