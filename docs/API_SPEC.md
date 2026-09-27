POST /api/v1/auth/register - create auctioneer account
POST /api/v1/auth/login - Login
POST /api/v1/auth/reset-password - Reset auctioneer account password
POST /api/v1/applications/{id}/documents - Upload NIN document
PATCH /api/v1/applications/{id} - update applications
POST /api/v1/applications/{id}/submit - submit applications
GET /api/v1/membership - check membership status
GET /api/v1/admin/applications - view applicationss
PATCH /api/v1/admin/applicationss/{id}/ - update applications(approve/reject)
POST /api/v1/admin/applications/bulk - bulk upload applicationss
POST /api/v1/admin/notifications - send user notification 


user schema
POST /api/v1/auth/register - create auctioneer account
POST /api/v1/auth/login - Login
POST /api/v1/auth/reset-password - Reset auctioneer account password

application schema
POST /api/v1/applications/{id}/upload-document - Upload NIN document
POST /api/v1/applications/{id}/submit - submit applications
PATCH /api/v1/applications/{id} - update applications

admin schema
GET /api/v1/admin/applications - view applications
PATCH /api/v1/admin/applications/{id}/ - set applications status(approve/reject)
POST /api/v1/admin/applications/bulk - bulk upload applications
POST /api/v1/admin/notifications - send user notification 

membership schema
GET /api/v1/membership - check membership status

