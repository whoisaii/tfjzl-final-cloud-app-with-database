# Django OnlineCourse

A runnable course and exam application built from the seven supplied assignment requirements. The repository was empty; this is a new implementation rather than a patch to an IBM starter.

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ for administration and http://127.0.0.1:8000/onlinecourse/ for the course. Log in with the account you created. Run `python manage.py test` to check grading and access control.

## Submission files

1. `onlinecourse/models.py`
2. `onlinecourse/admin.py`
3. Screenshot of `/admin/` named `03-admin-site.png`.
4. `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
5. `onlinecourse/views.py`
6. `onlinecourse/urls.py`
7. Complete the demo exam and capture its actual results as `07-final.png`.

Grading requires exactly all correct choices for each question and an overall score of at least 80%. Result snapshots preserve the original grade if questions later change. Only the submitting user can view a result. Bootstrap is loaded from a CDN. Development settings are local-only; configure a secret key, HTTPS, hosts, and production deployment settings before publishing a live service.
