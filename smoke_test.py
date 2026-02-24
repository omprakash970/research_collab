"""End-to-end smoke test for Phase 1 + Phase 2 + Phase 3."""
import os, sys, django, tempfile
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'researchcollab.settings')
django.setup()

# Write output to UTF-8 log file to bypass PowerShell encoding issues
log_file = open('smoke_log.txt', 'w', encoding='utf-8')
_orig_stdout = sys.stdout
_orig_stderr = sys.stderr
sys.stdout = log_file
sys.stderr = log_file

from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.accounts.models import Profile
from apps.projects.models import ResearchProject
from apps.documents.models import Document

passed = 0
failed = 0

def check(label, condition):
    global passed, failed
    status = "PASS" if condition else "FAIL"
    if condition:
        passed += 1
    else:
        failed += 1
    print(f"  [{status}] {label}")

client = Client()

# ── Phase 1: Auth ──
print("\n=== Phase 1: Authentication ===")

r = client.get('/login/')
check("Login page loads (200)", r.status_code == 200)

r = client.get('/dashboard/')
check("Dashboard redirects to login when unauthenticated (302)", r.status_code == 302 and '/login/' in r.get('Location', ''))

r = client.post('/login/', {'username': 'admin', 'password': 'admin123'})
check("Admin login succeeds (302 to dashboard)", r.status_code == 302 and '/dashboard/' in r.get('Location', ''))

r = client.get('/dashboard/')
check("Admin dashboard redirect (302)", r.status_code == 302 and 'admin' in r.get('Location', ''))

r = client.get('/dashboard/admin/')
check("Admin dashboard page loads (200)", r.status_code == 200)

client.get('/logout/')

r = client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
check("Researcher login succeeds (302)", r.status_code == 302)

r = client.get('/dashboard/researcher/')
check("Researcher dashboard page loads (200)", r.status_code == 200)

client.get('/logout/')

# ── Phase 2: Projects ──
print("\n=== Phase 2: Projects ===")

client.post('/login/', {'username': 'admin', 'password': 'admin123'})

# Clean up old test data
ResearchProject.objects.filter(title__startswith='Smoke Test').delete()

r = client.post('/projects/create/', {
    'title': 'Smoke Test: AI Research',
    'description': 'Phase 3 smoke test project.',
    'status': 'ACTIVE',
})
check("Admin: create project (302 redirect)", r.status_code == 302)

project = ResearchProject.objects.get(title='Smoke Test: AI Research')
# Consume the success message by visiting the detail page
client.get(f'/projects/{project.pk}/')

r = client.get(f'/projects/{project.pk}/')
check("Admin: project detail loads (200)", r.status_code == 200)

client.get('/logout/')

# Login as researcher (not assigned yet)
client.post('/login/', {'username': 'researcher1', 'password': 'research123'})

r = client.get(f'/projects/{project.pk}/')
check("Researcher: cannot view unassigned project (403)", r.status_code == 403)

client.get('/logout/')

# Assign researcher to project
researcher = User.objects.get(username='researcher1')
project.researchers.add(researcher)

client.post('/login/', {'username': 'researcher1', 'password': 'research123'})
r = client.get(f'/projects/{project.pk}/')
check("Researcher: can view assigned project (200)", r.status_code == 200)
client.get('/logout/')


# ── Phase 3: Documents ──
print("\n=== Phase 3: Documents ===")

# --- Admin tests ---
client.post('/login/', {'username': 'admin', 'password': 'admin123'})

r = client.get(f'/documents/project/{project.pk}/')
check("Admin: document list loads (200)", r.status_code == 200)
check("Admin: document list shows project title", 'AI Research' in r.content.decode())

r = client.get(f'/documents/project/{project.pk}/upload/')
check("Admin: document upload page loads (200)", r.status_code == 200)

# Upload a file
test_file = SimpleUploadedFile('test_paper.pdf', b'fake pdf content', content_type='application/pdf')
r = client.post(f'/documents/project/{project.pk}/upload/', {
    'title': 'Smoke Test Paper',
    'file': test_file,
})
check("Admin: upload document succeeds (302 redirect)", r.status_code == 302)

doc = Document.objects.get(title='Smoke Test Paper')
check("Document saved in database", doc is not None)
check("Document project is correct", doc.project == project)
check("Document uploaded_by is admin", doc.uploaded_by.username == 'admin')
check("Document file exists", bool(doc.file))

# Consume message
client.get(f'/documents/project/{project.pk}/')

r = client.get(f'/documents/project/{project.pk}/')
check("Admin: document list now shows uploaded doc", 'Smoke Test Paper' in r.content.decode())
check("Admin: download link present", 'Download' in r.content.decode())

client.get('/logout/')

# --- Researcher tests (assigned) ---
client.post('/login/', {'username': 'researcher1', 'password': 'research123'})

r = client.get(f'/documents/project/{project.pk}/')
check("Researcher (assigned): document list loads (200)", r.status_code == 200)
check("Researcher (assigned): sees uploaded doc", 'Smoke Test Paper' in r.content.decode())

r = client.get(f'/documents/project/{project.pk}/upload/')
check("Researcher (assigned): upload page loads (200)", r.status_code == 200)

# Researcher uploads a file
test_file2 = SimpleUploadedFile('researcher_notes.txt', b'some notes', content_type='text/plain')
r = client.post(f'/documents/project/{project.pk}/upload/', {
    'title': 'Researcher Notes',
    'file': test_file2,
})
check("Researcher (assigned): upload succeeds (302)", r.status_code == 302)

doc2 = Document.objects.get(title='Researcher Notes')
check("Researcher document uploaded_by correct", doc2.uploaded_by.username == 'researcher1')

client.get('/logout/')

# --- Researcher tests (NOT assigned to a different project) ---
client.post('/login/', {'username': 'admin', 'password': 'admin123'})
r = client.post('/projects/create/', {
    'title': 'Smoke Test: Secret Project',
    'description': 'Researcher should not access this.',
    'status': 'ACTIVE',
})
secret_project = ResearchProject.objects.get(title='Smoke Test: Secret Project')
client.get(f'/projects/{secret_project.pk}/')  # consume message
client.get('/logout/')

client.post('/login/', {'username': 'researcher1', 'password': 'research123'})

r = client.get(f'/documents/project/{secret_project.pk}/')
check("Researcher (not assigned): document list forbidden (403)", r.status_code == 403)

r = client.get(f'/documents/project/{secret_project.pk}/upload/')
check("Researcher (not assigned): upload forbidden (403)", r.status_code == 403)

client.get('/logout/')

# --- Unauthenticated access ---
r = client.get(f'/documents/project/{project.pk}/', follow=False)
check("Unauthenticated: document list redirects to login (302)", r.status_code == 302 and '/login/' in r.get('Location', ''))

r = client.get(f'/documents/project/{project.pk}/upload/', follow=False)
check("Unauthenticated: upload redirects to login (302)", r.status_code == 302 and '/login/' in r.get('Location', ''))

# --- Project detail has documents link ---
print("\n=== Navigation: Documents in Project Detail ===")
client.post('/login/', {'username': 'admin', 'password': 'admin123'})
r = client.get(f'/projects/{project.pk}/')
html = r.content.decode()
check("Project detail: 'Documents' section visible", 'Documents' in html)
check("Project detail: View Documents link present", f'/documents/project/{project.pk}/' in html)
check("Project detail: Upload New link present", f'/documents/project/{project.pk}/upload/' in html)
client.get('/logout/')

# ── Cleanup ──
Document.objects.filter(title__startswith='Smoke Test').delete()
Document.objects.filter(title='Researcher Notes').delete()
ResearchProject.objects.filter(title__startswith='Smoke Test').delete()

# ── Summary ──
print(f"\n{'='*50}")
print(f"  TOTAL: {passed + failed}  |  PASSED: {passed}  |  FAILED: {failed}")
print(f"{'='*50}")
if failed == 0:
    print("  ✅ ALL TESTS PASSED — Phase 1 + 2 + 3 fully functional!")
else:
    print(f"  ❌ {failed} test(s) failed. Review above.")

sys.stdout = _orig_stdout
sys.stderr = _orig_stderr
log_file.close()

