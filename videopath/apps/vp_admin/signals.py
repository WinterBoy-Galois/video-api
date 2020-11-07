from django.dispatch import Signal

JOB_PRIORITY_DEFAULT = 1
JOB_PRIORITY_HIGH = 10

# run daily and hourly jobs
hourly_jobs = Signal(providing_args=["priority"])
daily_jobs = Signal(providing_args=["priority"])