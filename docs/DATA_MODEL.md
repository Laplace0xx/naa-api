## user
id PK
f_name
l_name
email
phone_number
gender
dob
role
password_hash
joined_at

## Application
id PK
user id FK
status
business_name
business_address
document_id
applied_at

## Document 
id PK
user id FK
submitted_at
type
storage_id

## Membership
id PK
user id FK
status
issued_at

## userIdentity
id PK
user id FK
cred ENUM('BVN', 'NIN')UNIQUE
value_hmac
verified_at


enums
## Roles - admin, auctioneer
## Status - pending, approved, rejected
## cred - NIN, BVN