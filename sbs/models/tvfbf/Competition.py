import enum

from django.db import models

class Competition(models.Model):
    TURKEY = 0
    WORLD = 1
    OLYMPIAD = 2
    EUROPE = 3

    COMPGENERALTYPE = (
        (TURKEY, 'Türkiye'),
        (WORLD, 'Dünya'),
        (OLYMPIAD, 'Olimpiyat'),
        (EUROPE, 'Avrupa')
    )

    INTERUNIVERSITY = 0
    INTERSCHOOL = 1
    PERSONAL = 2
    GRANDPRIX = 3
    INTERCLUB = 4


    COMPTYPE = (
        (INTERUNIVERSITY, 'Üniversiteler Arası'),
        (INTERSCHOOL, 'Okullar Arası'),
        (PERSONAL, 'Ferdi'),
        (GRANDPRIX, 'Grand Prix'),
        (INTERCLUB, 'Kulüpler Arası')
    )

    compType = models.IntegerField(db_column='compType', blank=True, null=True, choices=COMPTYPE)  # Field name made lowercase.
    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    finishDate = models.DateTimeField(db_column='finishDate', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    startDate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    eventPlace = models.CharField(db_column='eventPlace', max_length=45, blank=True, null=True)  # Field name made lowercase.
    eventDate = models.CharField(db_column='eventDate', max_length=45, blank=True, null=True)  # Field name made lowercase.
    juryCount = models.IntegerField(db_column='juryCount', blank=True, null=True)  # Field name made lowercase.
    compGeneralType = models.IntegerField(db_column='compGeneralType', blank=True, null=True, choices=COMPGENERALTYPE)  # Field name made lowercase.
    eskimi = models.BooleanField(default=False)
    isOpen = models.BooleanField(db_column='isOpen', default=False)  # Field name made lowercase.
    registerStartDate = models.DateTimeField(db_column='registerStartDate', blank=True, null=True)  # Field name made lowercase.
    registerFinishDate = models.DateTimeField(db_column='registerFinishDate', blank=True, null=True)  # Field name made lowercase.
    kobilId = models.IntegerField(db_column='kobilId',default=0)  # Field name made lowercase.
    year = models.IntegerField( blank=True, null=True,)  # Field name made lowercase.
    isTransfered=models.BooleanField(default=False)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
        db_table = 'competition'
        managed = False
    # def save(self, force_insert=False, force_update=False):
    #     if self.name:
    #         self.name = self.name.upper()
    #     super(Competition, self).save(force_insert, force_update)





