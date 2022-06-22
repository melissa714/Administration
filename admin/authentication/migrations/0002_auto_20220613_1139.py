from django.core.management.sql import emit_post_migrate_signal


from django.db import migrations


def create_groups(apps, schema_migration):
    emit_post_migrate_signal(verbosity=1, interactive=False, db='default')

    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    add_courrier = Permission.objects.get(codename='add_courrier')
    change_courrier = Permission.objects.get(codename='change_courrier')
    delete_courrier = Permission.objects.get(codename='delete_courrier')
    view_courrier = Permission.objects.get(codename='view_courrier')
    add_entite = Permission.objects.get(codename='add_entite')
    change_entite = Permission.objects.get(codename='change_entite')
    delete_entite = Permission.objects.get(codename='delete_entite')
    view_entite = Permission.objects.get(codename='view_entite')
    view_courrier_dashboard = Permission.objects.get(codename='view_courrier_dashboard')
    add_personne = Permission.objects.get(codename='add_person')

    change_person = Permission.objects.get(codename='change_person')
    delete_person = Permission.objects.get(codename='delete_person')
    view_person = Permission.objects.get(codename='view_person')



    view_person_dashboard = Permission.objects.get(codename='view_person_dashboard')

   

    administration_permissions = [
        add_personne,
        change_person,
        view_person,
        delete_person,
        add_courrier,
        change_courrier,
        delete_courrier,
        view_courrier,
        add_entite,
        change_entite,
        delete_entite,
        view_entite,
        view_courrier_dashboard,
        view_person_dashboard,
    ]

    personnel_permissions = [
        add_personne,
    ]

    secretariat_permissions = [
        add_courrier,
        change_courrier,
        delete_courrier,
        view_courrier,
        add_entite,
        change_entite,
        delete_entite,
        view_entite,
        view_courrier_dashboard,
        # add_demande,
        # view_courrier_dashboard,
        # view_demande,
    ]

    secretariat = Group(name='secretariat')
    secretariat.save()
    secretariat.permissions.set(secretariat_permissions)

    personnel = Group(name='personnel')
    personnel.save()
    personnel.permissions.set(personnel_permissions)

    administration = Group(name='administration')
    administration.save()
    administration.permissions.set(administration_permissions)

 

    for user in User.objects.all():
       if user.role == 'SECRETARIAT':
          secretariat.user_set.add(user)
       if user.role == 'PERSONNEL':
          personnel.user.set.add(user)
       if user.role == 'ADMINISTRATION':
          administration.user.set.add(user)
     

class Migration(migrations.Migration):

    dependencies = [
            ('authentication', '0001_initial'),
            ('administrer', '0001_initial')



    ]

    operations = [

        migrations.RunPython(create_groups)

    ]
