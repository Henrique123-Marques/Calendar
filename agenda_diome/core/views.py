from django.shortcuts import render, redirect
from core.models import evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta

def login_user(request):
	return render(request, 'login.html')

def logout_user(request):
	logout(request)
	return redirect('/')

def submit_login(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		usuario = authenticate(username=username, password=password)
		if usuario is not None:
			login(request, usuario)
			return redirect('/')
		else:
			messages.error(request, 'Usuário ou senha invalido')
	return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
	usuario = request.user
	data_atual = datetime.now() - timedelta(hours=1)
	eventos = evento.objects.filter(usuario=usuario) #para filtrar os eventos de cada usuario
	dados = {'eventos':eventos}
	return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def pag_evento(request):
	id_evento = request.GET.get('id')
	dados = {}
	if id_evento:
		dados['evento'] = evento.objects.get(id=id_evento)
	return render(request, 'pag_evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
	if request.POST:
		titulo = request.POST.get('titulo')
		data_evento = request.POST.get('data_evento')
		descricao = request.POST.get('descricao')
		#local = request.POST.get('local')
		usuario = request.user
		id_evento = request.POST.get('id_evento')
		if id_evento:
			evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento, descricao=descricao)
		else:
			evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario)


	return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
	usuario = request.user
	eventos_delete = evento.objects.get(id=id_evento)
	if usuario == eventos_delete.usuario:
		eventos_delete.delete()
	return redirect('/')

