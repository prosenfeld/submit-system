class Conference(models.Model):
    shortname = models.CharField(
        max_length=15)
    longname = models.CharField(
        max_length=50)
    open_signup = models.BooleanField()
    tech_contact = models.EmailField()
    admin_contact = models.EmailField()
    complete = models.BooleanField()
    participants = models.ManyToManyField(Organization)

class Track(models.Model):
    shortname = models.CharField(
        max_length=15)
    longname = models.CharField(
        max_length=50)
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE)

class SubmitTask(models.Model):
    shortname = models.CharField(
        max_length=15)
    longname = models.CharField(
        max_length=50)
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE)
    accepting = models.BooleanField()

class Submission(models.Model):
    runtag = models.CharField(
        max_length=15,
        help_text='A unique string identifying this submission')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT)
    submittor = models.ForeignKey(
        User,
        on_delete=models.PROTECT)
    task = models.ForeignKey(
        SubmitTask,
        on_delete=models.PROTECT)
    subfile = models.FileField()
    
