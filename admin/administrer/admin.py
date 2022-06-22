from django.contrib import admin
from .models import *
# Register your models here.





class AdminPersonne(admin.ModelAdmin):
    list_display = ('nom_per', 'pren_per', 'photo', 'Sex_per', 'post_per', 'Emai_per', 'tel_per', 'numDec', 'dom_per', 'deco_per', 'Meca_per', 'stage_per',
                    'Type_per', 'numAr_per', 'Arme', 'Grades', 'service', 'formations', 'situa_pers', 'datePrise', 'dateEnr', 'AnSer_per', 'sousdirection')
    list_filters =('nom_per')
    search_fields = ('tel_per', 'numDec', 'dom_per', 'deco_per')








admin.site.register(Person,AdminPersonne)
admin.site.register(Service)
admin.site.register(sousDirection)
admin.site.register(direction)
admin.site.register(Arme)
admin.site.register(Grade)
admin.site.register(Diplome)
admin.site.register(FicheAnalyse)
admin.site.register(Instruction)


