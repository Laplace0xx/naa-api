## ACTORS
- Auctioneer
- Admin
- Verification provider

## USE CASE
### Auctioneers
  - register
  - Authenticate
  - reset password
  - upload documents
  - update application
  - submit application
  - check membership status

### Admin
- Authenticate
- View applications
- Review application
- Approve application
- Reject application
- upload applications(csv or json)
- notify user

## Verification provider
- Verify NIN
- Verify BVN
- Return verification result

# Flow
## Registration and application
user enters details -> creates account -> salt and hash password -> save details in db -> user applies for NAA membership -> submits NIN/BVN -> verification provider verifies credentials -> admin reviews application -> approve/reject, if reject restart flow or contact support, if approved -> go to dashboard, if provider verification fails -> retry | report to support

## authentication 
user enters details -> validate user credentials -> dashboard, if validation fails -> contact support or reset password

## Admin review
admin login -> view application -> reject/approve -> notification sent to user 




