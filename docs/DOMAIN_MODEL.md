## Entities
- User
- Verification provider
- Application
- Membership
- Document

## Attributes
- user(id, f_name, l_name, dob, joined_at, phone_number, gender, password_hash, email, role)
- verification provider(id, provider_name, joined_at)
- application(id, user_id, applied_at, status)
- membership(id, user_id, status, issued_at)
- Document(id, user_id, type)

enums
role - admin, auctioneer
status - pending, aproved, rejected
cred - NIN, BVN
membership - active, expired

## Relationsips
- one verification provider serves all users
- a user cannot have more than one active applications at a time
- a single membership belongs to a user
- a document is submitted as part of an application
- 