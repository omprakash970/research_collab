#!/usr/bin/env bash
# Render build script
# https://docs.render.com/deploy-django

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

# Auto-create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
from apps.accounts.models import Profile
User = get_user_model()
if not User.objects.filter(username='oppie_549').exists():
    u = User.objects.create_superuser('oppie_549', 'omprakashbandi583@gmail.com', 'Nancy123abc@')
    p = Profile.objects.get(user=u)
    p.role = 'ADMIN'
    p.save()
    print('Superuser oppie_549 created with ADMIN role')
else:
    print('Superuser oppie_549 already exists')
"
