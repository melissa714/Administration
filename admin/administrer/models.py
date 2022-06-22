from unicodedata import name
from django.db import models

# Create your models here.




class Type_Service(models.Model):
    lib_TypeServ = models.CharField(
        verbose_name='type de service', max_length=50)

    def __str__(self):
        return (self.lib_TypeServ)


class Entite(models.Model):

    SERVICE = (
        ('Choix du Service', (
            ('Interne', 'Interne'),
            ('Externe', 'Externe'),
        ))),

    PERSONNE = (
        ('Choix du Type de Personne', (
            ('Morale', 'Morale'),
            ('Physique', 'Physique'),
        ))),

    nom_Entite = models.CharField(
        verbose_name="destinataire ou expediteur", max_length=50)
    service = models.CharField(max_length=50, choices=SERVICE)
    personne = models.CharField(max_length=50, choices=PERSONNE)
    date_creat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.nom_Entite)


  


class Courrier(models.Model):
    CATEGORIE = (
        ('Choix de Type de Courrier', (
            ('TRANSMISSION', 'TRANSMISSION'),
            ('INTERNE', 'INTERNE'),
            ('ENTRANT', 'ENTRANT'),
            ('SORTANT', 'SORTANT'),
        ))),

    SEXE = (
        ('Choix du Sexe', (
            ('Feminin', 'feminin'),
            ('Masculin', 'masculin'),
        ))),

    num_ordre_cour = models.IntegerField(
        verbose_name="numero d ordre",unique=True,null=True)
    date_Emiss_cour = models.DateField('date Emission', null=True, blank=True)
    date_AccuseRecp_cour = models.DateField(
        'date de reception', null=True, blank=True)
    obj_cour = models.TextField()
    type_cour = models.CharField(max_length=20, null=True, choices=CATEGORIE)
    num_AccRecp_cour = models.PositiveIntegerField(
        verbose_name="numero accusé de reception", null=True, blank=True)
    file_cour = models.FileField(
        verbose_name="fichier", upload_to='static/upload', null=True)
    DestRecp = models.ForeignKey(
        Entite, verbose_name="destinataire ou recepteur", on_delete=models.CASCADE, null=True, related_name="DestRecp")
    date_ajout = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_ajout']

    class Meta:
        permissions = [("view_courrier_dashboard", "peut etre vu uniquement par le tableau de bords")]

    def __str__(self):
        return (self.type_cour)


class Arme(models.Model):
    lib_arm = models.CharField(max_length=150, verbose_name="nom d'Arme")

    def __str__(self):
        return (self.lib_arm)


class direction(models.Model):
    lib_dir = models.CharField(
        max_length=150, verbose_name="nom de la direction")

    def __str__(self):
        return (self.lib_dir)


class Diplome(models.Model):
    lib_dip = models.CharField(max_length=150)

    def __str__(self):
        return (self.lib_dip)


class Grade(models.Model):
    lib_grad = models.CharField(max_length=150, verbose_name="Grade")

    def __str__(self):
        return (self.lib_grad)


class sousDirection(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom de sous direction")
    direction = models.ForeignKey(direction, on_delete=models.CASCADE)

    def __str__(self):
        return (self.name)


class Service(models.Model):
    name = models.CharField(max_length=150, null=True)
    sousdirection = models.ForeignKey(
        sousDirection, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return (self.name)





class Instruction(models.Model):
    intruc = models.CharField(max_length=150, null=True)

    def __str__(self):
        return (self.intruc)


class FicheAnalyse(models.Model):
    Observation=models.CharField(max_length=250,null=True)
    courrier=models.ForeignKey(Courrier,on_delete=models.CASCADE,null=True,related_name="Courrier")
    instru=models.ManyToManyField(Instruction)
    # service = models.ForeignKey(Service,on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)

    def __str__(self):
        return (self.Observation)

















class Person(models.Model):

    SEXE = (
        ('Choix du sexe---', (
            ('Feminin', 'Feminin'),
            ('Masculin', 'masculin'),
        ))),

    TYPE = (
        ('Choisir type personne', (
            ('Civil', 'Civil'),
            ('Corps_habillé', 'Corps_habillé'),
        ))),

    SITUATION = (
        ('Choix du situation matrimoniale', (
            ('Marié', 'Marié(e)'),
            ('celibataire', 'Célibataire'),
        ))),

    nom_per = models.CharField(max_length=150, verbose_name='nom')
    pren_per = models.CharField(max_length=150, verbose_name='prenom')
    photo = models.ImageField(upload_to='static/images', verbose_name="photo",null=True)
    dteNaiss_per = models.DateField(verbose_name="date de naissance")
    lieu = models.CharField(max_length=200, null=True,
                            verbose_name="lieu de naissance")
    Mat_per = models.CharField(
        max_length=150, verbose_name="matricule", blank=True)
    Sex_per = models.CharField(
        max_length=150, null=True, choices=SEXE, verbose_name="sexe")
    post_per = models.CharField(
        max_length=150, verbose_name="FONCTION/OCCUPATION")
    Emai_per = models.EmailField(max_length=254, verbose_name="Email")
    tel_per = models.CharField(max_length=100, verbose_name="Telephone")
    numDec = models.CharField(
        verbose_name="numero de decision", max_length=100, blank=True, null=True)
    dom_per = models.CharField(max_length=150, verbose_name="domicile")
    deco_per = models.CharField(
        max_length=150, null=True, blank=True, verbose_name="decoration")
    Meca_per = models.CharField(
        max_length=150, blank=True, verbose_name="Mecano", null=True)
    stage_per = models.CharField(
        max_length=150, verbose_name="stage effectué", blank=True, null=True)
    Type_per = models.CharField(
        max_length=150, null=True, choices=TYPE, verbose_name="type de personne")
    numAr_per = models.IntegerField(
        blank=True, null=True, verbose_name="numéro d'arme")
    Arme = models.ForeignKey(Arme, on_delete=models.CASCADE, verbose_name="Arme", null=True,blank=True)
    Grades = models.ForeignKey(Grade, on_delete=models.CASCADE,null=True,blank=True, verbose_name="Grades")
    Diplomes = models.ManyToManyField(Diplome,related_name="Diplomes")
    formations = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="formations")
    situa_pers = models.CharField(
        max_length=100, choices=SITUATION, verbose_name="situation matrimoniale")
    person = models.CharField(
        max_length=200, null=True, verbose_name="personne à contacter")
    datePrise = models.DateField(
        null=True, verbose_name="date prise de service")
    dateEnr = models.DateTimeField(
        auto_now=True, verbose_name="date d enregistrement")
    dateE = models.DateField(blank=True, null=True,
                             verbose_name="date d'entree à la police")
    AnSer_per = models.CharField(
        blank=True, null=True, verbose_name="TROIS DERNIERS SERVICE ET POSTE OCCUPES AVANT LA DITT", max_length=300)
    sousdirection = models.ForeignKey(sousDirection,models.SET_NULL,null=True)
    service = models.ForeignKey(Service,models.SET_NULL, verbose_name="service",null=True)

    class Meta:
        ordering = ['dateE']
        permissions = [("view_person_dashboard","peut etre vu uniquement par le tableau de bords")]
       

    def __str__(self):
        return (self.nom_per)

    def __str__(self):
        return (self.pren_per)

    def __str__(self):
        return (self.Mat_per)
    
    def __str__(self):
        return (self.deco_per)
    
    def __str__(self):
        return (self.post_per)

    def __str__(self):
        return (self.numDec)

    def __str__(self):
        return (self.dom_per)

    def __str__(self):
        return (self.Meca_per)

    def __str__(self):
        return (self.stage_per)

    def __str__(self):
        return (self.Type_per)

    def __str__(self):
        return (self.lieu)

    def __str__(self):
        return (self.formations)

    def __str__(self):
        return (self.person)



