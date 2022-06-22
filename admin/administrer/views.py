from http.client import HTTPResponse
from django.http import HttpResponseNotFound,HttpResponse
from urllib import response
from django.shortcuts import render,get_object_or_404,redirect
from requests import delete
from .models import *
from authentication.models import *

from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import os
from django.db.models import Count
from notifications.signals import notify
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required,permission_required

@login_required
def index(request):
    return render(request,"index.html")


def search(request):
   person = Person.objects.order_by('dateEnr').reverse()
   query = request.GET.get('query')
   if query != '' and query is not None:
       person = Person.objects.filter(Q(nom_per__icontains=query) | Q(pren_per__icontains=query) | Q(
           lieu__icontains=query) | Q(Mat_per__icontains=query) | Q(Meca_per__icontains=query) | Q(Type_per__icontains=query))
   paginator = Paginator(person, 10)
   page = request.GET.get('page')
   page_obj = paginator.get_page(page)
   context = {
       'person': person,
       'page_obj': page_obj
   }
   return render(request, 'personnel/liste_per.html', context)

    


def load_cities(request):
    sousdirection_id = request.GET.get('sousdirection')
    services = Service.objects.filter(
        sousdirection_id=sousdirection_id).order_by('name')
    return render(request, 'personnel/liste.html', {'services': services})


@login_required
@permission_required('administrer.add_person')
def personne(request):
    user = User.objects.get(role="PERSONNEL")
    users = User.objects.get(role="ADMINISTRATION")
    if request.method == 'POST':
        form=PersonForm(request.POST,request.FILES)
        if form.is_valid():
           form.save()
           form = PersonForm()
           messages.success(request, 'les données ont été enregistré.')
           notify.send(user,recipient=users,verb='a enregistré une fiche personnel',target=users)
    else:
        form=PersonForm()
    return render(request, 'personnel/person_form.html',{'form': form})


@login_required
@permission_required('administrer.view_person')
def listePerson(request):
   person = Person.objects.order_by('dateEnr').reverse()
   query = request.GET.get('query')
   if query != '' and query is not None:
       person = Person.objects.filter(Q(nom_per__icontains=query) | Q(pren_per__icontains=query) | Q(
           lieu__icontains=query) | Q(Mat_per__icontains=query) | Q(Meca_per__icontains=query) | Q(Type_per__icontains=query))
   paginator = Paginator(person, 7)
   page = request.GET.get('page')
   page_obj = paginator.get_page(page)
   context = {
       'person': person,
       'page_obj': page_obj

   }
   return render(request, 'personnel/liste_per.html', context)


@login_required
@permission_required('administrer.change_person')
def ModiPers(request, id):
    personne = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=personne)
        if form.is_valid():
           form.save()
           form = PersonForm(instance=personne)
           messages.success(request, 'les données ont été enregistré.')
    else:
        form = PersonForm(instance=personne)
    return render(request, 'Personnel/edit_per.html', {'form': form})




def supPerson(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'le courrier a été supprimé avec success.')
    return redirect('/liste/personne')


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path






def detail(request, *args, **kwargs):
    pk = kwargs.get('pk')
    person = get_object_or_404(Person, pk=pk)
    template_path = 'personnel/pdf.html'
    #pour charger image
    BASE_URL = request.scheme+'://'+request.get_host()
    context = {'person': person, 'base_url': BASE_URL}

    #return HttpResponse(request.scheme+'://'+request.get_host())
   # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
   # to directly download the pdf we need attachment
   # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
   # to view on browser we catDG?n remove attachment
    response['Content-Disposition'] = 'filename="report.pdf"'
   # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
   # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)

   # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# def mark_all_as_read(request):
#     request.user.notifications.mark_all_as_read()

#     _next = request.GET.get('next')

#     if _next:
#         return redirect(_next)
#     return redirect('notifications:unread')

@login_required
@permission_required(['administrer.add_courrier','administrer.add_entite'])
def AddCour(request):
    ent = EntiteForm()
    form = CourrierForm()
    if request.method == 'POST':
        form = CourrierForm(request.POST,request.FILES)
        if form.is_valid():
                form.save()
                form = CourrierForm()
                messages.success(request, 'le courrier a été enregistré!!.')
                # notify.send(users, recipient=user, verb='a enregistré un courrier')
        ent = EntiteForm(request.POST)
        if ent.is_valid():
                ent.save()
                ent = EntiteForm()
                messages.success(request, 'la personne a été enregistré!!.')

    context = {
        'form':form,
        'ent': ent,
    }
    return render(request, 'courrier/ajout.html', context=context)


@login_required
@permission_required('administrer.view_courrier')
def liste(request):
    liste = Courrier.objects.order_by('date_ajout').reverse()
   # return HttpResponse(liste.exists())
    query=request.GET.get('query')
    if query != '' and query is not None:
         liste = Courrier.objects.filter(Q(num_ordre_cour__icontains=query) | Q(obj_cour__icontains=query) | Q(type_cour__icontains=query))
    paginator = Paginator(liste,6)
    page= request.GET.get('page')
    liste=paginator.get_page(page)
    context = {
        'liste': liste,
    }
    return render(request, 'courrier/liste.html', context)



@login_required
@permission_required(['administrer.change_courrier','administrer.change_entite'])
def Modif(request,id):
    ent = EntiteForm()
    courrier= get_object_or_404(Courrier,id=id)
    form = CourrierForm(instance=courrier)
    if request.method == 'POST':
        form = CourrierForm(request.POST,request.FILES,instance=courrier)
        if form.is_valid():
                form.save()
                form = CourrierForm(instance=courrier)
                messages.success(request, 'le courrier a été enregistré!!.')
        ent = EntiteForm(request.POST)
        if ent.is_valid():
                ent.save()
                ent = EntiteForm()
                messages.success(request, 'la personne a été enregistré!!.')

    context = {
            'form':form,
            'ent': ent,
    }
    return render(request, 'courrier/edit.html', context=context)



def suppression(request,id):
    courrier= get_object_or_404(Courrier,id=id)
    if request.method == 'POST':
        courrier.delete()
        messages.success(request, 'le courrier a été supprimé avec success.')
    return redirect('/liste/courrier')






def pdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    courrier = get_object_or_404(Courrier, pk=pk)
    template_path = 'courrier/details.html'
    context = {'courrier': courrier}
   # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
   # to directly download the pdf we need attachment
   # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
   # to view on browser we catDG?n remove attachment
    response['Content-Disposition'] = 'filename="report.pdf"'
   # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
   # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
   # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response





    
def listeDirec(request):
    liste = Courrier.objects.order_by('date_ajout').filter(type_cour='ENTRANT').reverse() 
   # return HttpResponse(liste.exists())
    query=request.GET.get('query')
    if query != '' and query is not None:
         liste = Courrier.objects.filter(Q(num_ordre_cour__icontains=query) | Q(obj_cour__icontains=query) | Q(type_cour__icontains=query))
    paginator = Paginator(liste,6)
    page= request.GET.get('page')
    liste=paginator.get_page(page)
    context = {
        'liste': liste,
    }
    return render(request, 'fiche_analyse/liste.html', context)


@login_required
@permission_required('administrer.view_courrier_dashboard')
def dashboard(request):
    series = []
    labels = []
    total=Courrier.objects.count()
    courrier = Courrier.objects.order_by('num_ordre_cour').reverse()[0:5]
    data = []
    labelo = []
    data = []
    externe = Entite.objects.filter(service='Externe', personne='Morale').count()
    externes = Entite.objects.filter(service='Externe', personne='Physique').count()
    internes = Entite.objects.filter(service='Interne', personne='Physique').count()
    interne = Entite.objects.filter(service='Interne', personne='Morale').count()
    inter = Courrier.objects.all().filter(type_cour='INTERNE').count()
    ent = Courrier.objects.all().filter(type_cour='ENTRANT').count()
    sor = Courrier.objects.all().filter(type_cour='SORTANT').count()
    trans = Courrier.objects.all().filter(type_cour='TRANSMISSION').count()
    query = Courrier.objects.all().values(
        'date_ajout__year').annotate(totalCourrier=Count('id'))
    value = Entite.objects.all().values(
        'date_creat__year').annotate(total=Count('id'))
    for cour in query:
        labels.append(cour['date_ajout__year'])
        data.append(cour['totalCourrier'])
    for ente in value:
        labelo.append(ente['date_creat__year'])
        series.append(ente['total'])
    context = {
        'trans': trans,
        'sor': sor,
        'ent': ent,
        'inter': inter,
        'labels': labels,
        'data': data,
        'courrier': courrier,
        'total':total,
        'labelo': labelo,
        'series':series,
        'interne':interne,
        'externe':externe,
        'internes': internes,
        'externes': externes,
       
    }
    
    return render(request, 'courrier/dashboard.html', context)





@login_required
@permission_required('administrer.view_person_dashboard')   
def dash(request):
    labels=[]
    data=[]
    person=Person.objects.order_by('dateEnr').reverse()
    feminins = Person.objects.filter(
        Sex_per="Feminin", Type_per="Civil").count()
    feminin = Person.objects.filter(Sex_per="Feminin", Type_per="Corps_habillé").count()
    homme = Person.objects.filter(
        Sex_per="Masculin", Type_per="Corps_habillé").count()
    hommes = Person.objects.filter(
        Sex_per="Masculin", Type_per="Civil").count()
    query = Person.objects.all().values(
        'dateEnr__year').annotate(total=Count('id'))
    for cour in query:
        labels.append(cour['dateEnr__year'])
        data.append(cour['total'])  
    context={
        'feminins':feminins,
        'feminin':feminin,
        'homme':homme,
        'hommes':hommes,
        'labels': labels,
        'data': data,
        'person':person,
    }
    return render(request,'personnel/dashboard.html',context)