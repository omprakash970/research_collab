"""
Phase 5 — Final Smoke Test
Validates all phases (1-4) + Phase 5 polish (messages, access control, navigation).
"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'researchcollab.settings')
django.setup()

log = open('smoke_log.txt', 'w', encoding='utf-8')
_out, _err = sys.stdout, sys.stderr
sys.stdout = sys.stderr = log

from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.accounts.models import Profile
from apps.projects.models import ResearchProject
from apps.documents.models import Document
from apps.communication.models import ProjectMessage

passed = failed = 0

def check(label, condition):
    global passed, failed
    if condition:
        passed += 1; print(f"  [PASS] {label}")
    else:
        failed += 1; print(f"  [FAIL] {label}")

client = Client()

# ── Phase 1: Auth ──
print("\n=== Phase 1: Authentication & Roles ===")

r = client.get('/login/')
check("Login page loads (200)", r.status_code == 200)

r = client.get('/dashboard/')
check("Dashboard requires auth (302→login)", r.status_code == 302 and '/login/' in r.get('Location', ''))

# Admin login
r = client.post('/login/', {'username': 'admin', 'password': 'admin123'})
check("Admin login (302→dashboard)", r.status_code == 302)
r = client.get('/dashboard/')
check("Admin dashboard redirect (302→admin)", r.status_code == 302 and 'admin' in r.get('Location', ''))
r = client.get('/dashboard/admin/')
check("Admin dashboard loads (200)", r.status_code == 200)
html = r.content.decode()
check("Admin dashboard: no 'coming soon' text", 'coming soon' not in html.lower())

# Admin tries researcher dashboard
r = client.get('/dashboard/researcher/')
check("Admin blocked from researcher dashboard (302)", r.status_code == 302)

client.get('/logout/')

# Researcher login
r = client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
check("Researcher login (302)", r.status_code == 302)
r = client.get('/dashboard/researcher/')
check("Researcher dashboard loads (200)", r.status_code == 200)
html = r.content.decode()
check("Researcher dashboard: no 'coming soon' text", 'coming soon' not in html.lower())

# Researcher tries admin dashboard
r = client.get('/dashboard/admin/')
check("Researcher blocked from admin dashboard (302)", r.status_code == 302)

client.get('/logout/')

# ── Phase 2: Projects ──
print("\n=== Phase 2: Project Management ===")

client.post('/login/', {'username': 'admin', 'password': 'admin123'})
ResearchProject.objects.filter(title__startswith='P5 Smoke').delete()

r = client.post('/projects/create/', {
    'title': 'P5 Smoke: Final Test Project',
    'description': 'Phase 5 comprehensive test.',
    'status': 'ACTIVE',
})
check("Admin: create project (302)", r.status_code == 302)
project = ResearchProject.objects.get(title='P5 Smoke: Final Test Project')
client.get(f'/projects/{project.pk}/')  # consume message

r = client.get(f'/projects/{project.pk}/')
check("Admin: project detail (200)", r.status_code == 200)

r = client.get(f'/projects/{project.pk}/edit/')
check("Admin: project edit page (200)", r.status_code == 200)

researcher = User.objects.get(username='researcher1')
project.researchers.add(researcher)
client.get('/logout/')

client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
r = client.get(f'/projects/{project.pk}/')
check("Researcher: assigned project detail (200)", r.status_code == 200)
client.get('/logout/')

# ── Phase 3: Documents ──
print("\n=== Phase 3: Document Sharing ===")

client.post('/login/', {'username': 'admin', 'password': 'admin123'})
f = SimpleUploadedFile('report.pdf', b'content', content_type='application/pdf')
r = client.post(f'/documents/project/{project.pk}/upload/', {'title': 'P5 Smoke Report', 'file': f})
check("Admin: upload document (302)", r.status_code == 302)
client.get(f'/documents/project/{project.pk}/')  # consume message

r = client.get(f'/documents/project/{project.pk}/')
check("Admin: doc list shows upload (200)", r.status_code == 200 and 'P5 Smoke Report' in r.content.decode())
client.get('/logout/')

client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
r = client.get(f'/documents/project/{project.pk}/')
check("Researcher (assigned): doc list (200)", r.status_code == 200)

# Researcher uploads
f2 = SimpleUploadedFile('notes.txt', b'data', content_type='text/plain')
r = client.post(f'/documents/project/{project.pk}/upload/', {'title': 'P5 Smoke Notes', 'file': f2})
check("Researcher (assigned): upload doc (302)", r.status_code == 302)
client.get('/logout/')

# ── Phase 4: Communication ──
print("\n=== Phase 4: Communication ===")

client.post('/login/', {'username': 'admin', 'password': 'admin123'})
r = client.get(f'/communication/project/{project.pk}/messages/')
check("Admin: messages page (200)", r.status_code == 200)

r = client.post(f'/communication/project/{project.pk}/messages/', {'message': 'Admin test msg'})
check("Admin: post message (302)", r.status_code == 302)

# Consume message flash, then verify thread
client.get(f'/communication/project/{project.pk}/messages/')
r = client.get(f'/communication/project/{project.pk}/messages/')
check("Admin: thread shows message", 'Admin test msg' in r.content.decode())
client.get('/logout/')

client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
r = client.get(f'/communication/project/{project.pk}/messages/')
check("Researcher (assigned): messages page (200)", r.status_code == 200)

r = client.post(f'/communication/project/{project.pk}/messages/', {'message': 'Researcher reply'})
check("Researcher: post message (302)", r.status_code == 302)
client.get('/logout/')

# ── Phase 5: Security & Polish ──
print("\n=== Phase 5: Security & Access Control ===")

# Unauthenticated access — all routes should redirect
unauth_routes = [
    '/dashboard/',
    '/projects/',
    '/projects/create/',
    f'/projects/{project.pk}/',
    f'/projects/{project.pk}/edit/',
    f'/documents/project/{project.pk}/',
    f'/documents/project/{project.pk}/upload/',
    f'/communication/project/{project.pk}/messages/',
]
for route in unauth_routes:
    r = client.get(route, follow=False)
    check(f"Unauth: {route} → login (302)", r.status_code == 302 and '/login/' in r.get('Location', ''))

# Non-assigned researcher blocked from non-assigned project
client.post('/login/', {'username': 'admin', 'password': 'admin123'})
r = client.post('/projects/create/', {
    'title': 'P5 Smoke: Secret Project',
    'description': 'Restricted.',
    'status': 'ACTIVE',
})
secret = ResearchProject.objects.get(title='P5 Smoke: Secret Project')
client.get(f'/projects/{secret.pk}/')  # consume message
client.get('/logout/')

client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
r = client.get(f'/projects/{secret.pk}/')
check("Researcher: unassigned project detail (403)", r.status_code == 403)

r = client.get(f'/projects/{secret.pk}/edit/')
check("Researcher: edit any project (403)", r.status_code == 403)

r = client.get(f'/documents/project/{secret.pk}/')
check("Researcher: unassigned docs (403)", r.status_code == 403)

r = client.get(f'/documents/project/{secret.pk}/upload/')
check("Researcher: unassigned upload (403)", r.status_code == 403)

r = client.get(f'/communication/project/{secret.pk}/messages/')
check("Researcher: unassigned messages (403)", r.status_code == 403)

r = client.post(f'/communication/project/{secret.pk}/messages/', {'message': 'Sneaky'})
check("Researcher: unassigned POST message (403)", r.status_code == 403)

r = client.get('/projects/create/')
check("Researcher: create project (403)", r.status_code == 403)
client.get('/logout/')

# Invalid IDs → 404
print("\n=== Phase 5: Error Handling (404s) ===")
client.post('/login/', {'username': 'admin', 'password': 'admin123'})
r = client.get('/projects/99999/')
check("Invalid project ID → 404", r.status_code == 404)

r = client.get('/documents/project/99999/')
check("Invalid doc project ID → 404", r.status_code == 404)

r = client.get('/communication/project/99999/messages/')
check("Invalid comm project ID → 404", r.status_code == 404)
client.get('/logout/')

# Messages framework — flash messages present
print("\n=== Phase 5: Django Messages Framework ===")
client.post('/login/', {'username': 'admin', 'password': 'admin123'})

# Login welcome message consumed on dashboard
r = client.get('/dashboard/', follow=True)
html = r.content.decode()
check("Login: success message displayed", 'Welcome back' in html)

# Create project → success message
r = client.post('/projects/create/', {
    'title': 'P5 Smoke: Msg Test',
    'description': 'Testing messages.',
    'status': 'ACTIVE',
}, follow=True)
html = r.content.decode()
check("Create project: success message displayed", 'created successfully' in html)
msg_proj = ResearchProject.objects.get(title='P5 Smoke: Msg Test')

# Upload doc → success message
f3 = SimpleUploadedFile('msg_test.pdf', b'x', content_type='application/pdf')
r = client.post(f'/documents/project/{msg_proj.pk}/upload/', {'title': 'P5 Msg Doc', 'file': f3}, follow=True)
html = r.content.decode()
check("Upload document: success message displayed", 'uploaded successfully' in html)

# Post discussion → success message
r = client.post(f'/communication/project/{msg_proj.pk}/messages/', {'message': 'Msg test'}, follow=True)
html = r.content.decode()
check("Post message: success message displayed", 'Message posted' in html)

client.get('/logout/')

# Logout message
r = client.get('/login/')
html = r.content.decode()
check("Logout: info message displayed", 'logged out' in html)

# Navigation checks
print("\n=== Phase 5: Navigation & UI ===")
client.post('/login/', {'username': 'admin', 'password': 'admin123'})
r = client.get(f'/projects/{project.pk}/')
html = r.content.decode()
check("Project detail: Documents card visible", 'View Documents' in html)
check("Project detail: Discussion card visible", 'Open Discussion' in html)
check("Project detail: Edit button for admin", 'Edit Project' in html)

r = client.get('/projects/')
html = r.content.decode()
check("Navbar: Projects link present", 'href="/projects/"' in html)
check("Navbar: + New Project for admin", 'New Project' in html)
check("Navbar: role badge shown", 'Admin' in html)
client.get('/logout/')

client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
r = client.get('/projects/')
html = r.content.decode()
check("Navbar: No + New Project for researcher", 'href="/projects/create/"' not in html)
check("Navbar: role badge shown for researcher", 'Researcher' in html)
client.get('/logout/')

# Footer
client.post('/login/', {'username': 'admin', 'password': 'admin123'})
r = client.get('/projects/')
html = r.content.decode()
check("Footer: contains project name", 'ResearchCollab' in html)
check("Footer: contains year", '2026' in html)
client.get('/logout/')

# ── Cleanup ──
ProjectMessage.objects.filter(project__title__startswith='P5 Smoke').delete()
Document.objects.filter(title__startswith='P5').delete()
ResearchProject.objects.filter(title__startswith='P5 Smoke').delete()

# ── Summary ──
total = passed + failed
print(f"\n{'='*60}")
print(f"  TOTAL: {total}  |  PASSED: {passed}  |  FAILED: {failed}")
print(f"{'='*60}")
if failed == 0:
    print("  ALL TESTS PASSED — Project is review-ready!")
else:
    print(f"  {failed} test(s) failed.")

sys.stdout, sys.stderr = _out, _err
log.close()

