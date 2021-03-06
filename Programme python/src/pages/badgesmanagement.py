import os
import time

from tkinter import * 
from src.style.funct import *

bm_entry = []
bm_entry_val = []
bm_label = []
bm_button_rectangle = []
bm_button_text = []
bm_button_rect = []
bm_notif_rect = []
bm_notif_text = []
bm_tableau_rectangle = []
bm_tableau_id = []
bm_tableau_code = []
bm_tableau_place = []
bm_tableau_date = []
bm_tableau_del = []
bm_tableau_dela = [0]
bm_tableau_height = 0
bm_tableau_nbline = 0
bm_pagination_rect = []
bm_pagination_rectangle = []
bm_pagination_text = []

bm_notif_posx = 5
bm_notif_posy = 70
bm_tableau_posx = 5
bm_tableau_posy = 120

def bm_init(box):

	set_checking_var("bm_nb_badges", get_autorized_badges('size', 1))
	set_checking_var("bm_page_select", 0)
	set_checking_var("bm_page_select_old", 0)
	set_checking_var("bm_notific", "Aucune notification")
	set_checking_var("seconde", last_places('seconde', 0))

	global bm_entry
	global bm_entry_val
	global bm_label
	global bm_button_rectangle
	global bm_button_text
	global bm_button_rect
	global bm_notif_rect
	global bm_notif_text
	global bm_tableau_rectangle
	global bm_tableau_id
	global bm_tableau_code
	global bm_tableau_place
	global bm_tableau_date
	global bm_tableau_del
	global bm_tableau_dela
	global bm_tableau_height
	global bm_tableau_nbline
	global bm_pagination_rect
	global bm_pagination_rectangle
	global bm_pagination_text
	bm_entry = []
	bm_entry_val = []
	bm_label = []
	bm_button_rectangle = []
	bm_button_text = []
	bm_button_rect = []
	bm_notif_rect = []
	bm_notif_text = []
	bm_tableau_rectangle = []
	bm_tableau_id = []
	bm_tableau_code = []
	bm_tableau_place = []
	bm_tableau_date = []
	bm_tableau_del = []
	bm_tableau_dela = [0]
	bm_tableau_height = box.winfo_height()-120
	bm_tableau_nbline = (bm_tableau_height-100)/20
	bm_pagination_rect = []
	bm_pagination_rectangle = []
	bm_pagination_text = []

	# formulaire
	bm_formulaires_a(box, 0, 5, 5)
	bm_formulaires_b(box, 1, 5, 35) # id 1 et 2
	bm_button(box, 0, 300, 5)
	bm_button(box, 1, 425, 35)

	# notification
	bm_notif(box, bm_notif_posx, bm_notif_posy)

	# tableau
	bm_createline(box, bm_tableau_posx, bm_tableau_posy+20*0, 0, "ID", "Code d'accès", "Place", "Date et heure d'ajout", "Supprimer")
	bm_createtableau(box, bm_tableau_posx, bm_tableau_posy)

	bm_createpagination(box,0 ,bm_tableau_posx, bm_tableau_posy+325, "<")
	bm_createpagination(box,1 ,bm_tableau_posx+35, bm_tableau_posy+325, ">")

'''
--------------------------------------------------------------------------------------
formulaires et notification
'''
def bm_formulaires_a(box, id, x, y):
	global bm_entry_val
	bm_label.append(Label(box, text="Ajouter le badge : ", bd=0, fg='#333333', font="Arial 15 bold"))
	bm_label[id].place(x=x, y=y, anchor=NW)
	bm_entry_val.append(StringVar())
	bm_entry.append(Entry(box, width=10, bd=0, bg='#bdc3c7', fg='#333333', disabledbackground='#bdc3c7', disabledforeground='#333333', font="Arial 15 bold", textvariable=bm_entry_val[id]))
	bm_entry[id].place(x=x+175, y=y, anchor=NW)
	bm_entry[id].insert(0, "0000000000")


def bm_formulaires_b(box, id, x, y):
	global bm_entry_val
	bm_label.append(Label(box, text="Lier le badge : ", bd=0, fg='#333333', font="Arial 15 bold"))
	bm_label[id].place(x=x, y=y, anchor=NW)
	bm_entry_val.append(StringVar())
	bm_entry.append(Entry(box, width=10, bd=0, bg='#bdc3c7', fg='#333333', disabledbackground='#bdc3c7', disabledforeground='#333333', font="Arial 15 bold", textvariable=bm_entry_val[id]))
	bm_entry[id].place(x=x+140, y=y, anchor=NW)
	bm_entry[id].insert(0, "0000000000")

	bm_label.append(Label(box, text="à la place N° : ", bd=0, fg='#333333', font="Arial 15 bold"))
	bm_label[id+1].place(x=x+255, y=y, anchor=NW)
	bm_entry_val.append(StringVar())
	bm_entry.append(Entry(box, width=2, bd=0, bg='#bdc3c7', fg='#333333', disabledbackground='#bdc3c7', disabledforeground='#333333', font="Arial 15 bold", textvariable=bm_entry_val[id+1]))
	bm_entry[id+1].place(x=x+390, y=y, anchor=NW)
	bm_entry[id+1].insert(0, "00")

def bm_button(box, id, x, y):
	bm_button_rectangle.append(box.create_rectangle(x, y, x+30, y+26, fill='#2ecc71', width=0))
	bm_button_text.append(box.create_text(x+15, y+13, text=">", fill="#ecf0f1", font="Arial 20"))
	bm_button_rect.append(box.create_rectangle(x, y, x+30, y+25, width=0))

	box.tag_bind(bm_button_rect[id], '<Enter>', lambda event, box=box, id=id: bm_buttonOver(box, id)) 
	box.tag_bind(bm_button_rect[id], '<Leave>', lambda event, box=box, id=id: bm_buttonOutOver(box, id)) 
	box.tag_bind(bm_button_rect[id], '<ButtonRelease-1>', lambda event, box=box, id=id: bm_buttonClick(box, id))

def bm_buttonOver(box, id):
	box.itemconfigure(bm_button_rectangle[id], fill='#27ae60')

def bm_buttonOutOver(box, id):
	box.itemconfigure(bm_button_rectangle[id], fill='#2ecc71')

def bm_buttonClick(box, id):
	if id == 0:
		if len(bm_entry[0].get())==10:
			add_autorized_badges(bm_entry[0].get(), time.strftime('%d/%m/%Y - %H:%M'), "")
		else:
			set_checking_var("bm_notific", "Le code "+str(bm_entry[0].get())+" n'est pas valide.")
			set_checking_var("seconde", "00")
	else:
		if int(bm_entry[2].get())<16 and int(bm_entry[2].get())>=0 and len(bm_entry[1].get())==10:
			add_autorized_badges(bm_entry[1].get(), time.strftime('%d/%m/%Y - %H:%M'), int(bm_entry[2].get()))
		else:
			set_checking_var("seconde", "00")
			set_checking_var("bm_notific", "Le code "+str(bm_entry[1].get())+" n'a pas pu etre ajouté, ni lié à la place N°"+str(bm_entry[2].get())+".")

def bm_notif(box, x, y):
	if box.winfo_width()<640:
		largeur = 640
	else :
		largeur = box.winfo_width()
	bm_notif_rect.append(box.create_rectangle(x, y, largeur-x*2, y+40, fill='#FFB74D', width=0))
	bm_notif_text.append(box.create_text(largeur/2, y+20, text=get_checking_var('bm_notific'), fill="#ecf0f1", font="Arial 16"))

def bm_notif_update(box):
	if box.winfo_width()>640:
		box.itemconfigure(bm_notif_text[0], text=get_checking_var('bm_notific'))
		box.coords(bm_notif_rect[0], bm_notif_posx, bm_notif_posy, box.winfo_width()-bm_notif_posx*2, bm_notif_posy+40)
		box.coords(bm_notif_text[0], box.winfo_width()/2, bm_notif_posy+20)

'''
--------------------------------------------------------------------------------------
tableau
'''
def bm_createline(box, x, y, style, id, code, place, date, supp):
	if box.winfo_width()<640:
		largeur = 640
	else :
		largeur = box.winfo_width()
	if style==0:
		bm_tableau_rectangle.append(box.create_rectangle(x, y, largeur-x*2, y+20, fill='#9E9E9E', width=0))
	elif style==1:
		bm_tableau_rectangle.append(box.create_rectangle(x, y, largeur-x*2, y+20, fill='#EEEEEE', width=0))
	elif style==2:
		bm_tableau_rectangle.append(box.create_rectangle(x, y, largeur-x*2, y+20, fill='#E0E0E0', width=0))
	else:
		pass
	bm_tableau_id.append(box.create_text(x+5, y+10, text=id, fill="#333333", font="Arial 10 bold", anchor='w'))
	bm_tableau_code.append(box.create_text(largeur*0.25, y+10, text=code, fill="#333333", font="Arial 10 bold"))
	bm_tableau_place.append(box.create_text(largeur*0.5, y+10, text=place, fill="#333333", font="Arial 10 bold"))
	bm_tableau_date.append(box.create_text(largeur*0.75, y+10, text=date, fill="#333333", font="Arial 10 bold"))
	bm_tableau_del.append(box.create_text(largeur-50, y+10, text=supp, fill="#333333", font="Arial 10 bold"))
	if id!='ID':
		bm_tableau_dela.append(box.tag_bind(bm_tableau_del[id+1], '<ButtonRelease-1>', lambda event, box=box, code=code, id=id: bm_delClick(box, code, id)))

def bm_updateline(box, style, id, code, place, date, supp):
	ida = id+1-15*get_checking_var('bm_page_select')
	if style==0:
		box.itemconfigure(bm_tableau_rectangle[ida], fill='#9E9E9E', width=0)
	elif style==1:
		box.itemconfigure(bm_tableau_rectangle[ida], fill='#EEEEEE', width=0)
	elif style==2:
		box.itemconfigure(bm_tableau_rectangle[ida], fill='#E0E0E0', width=0)
	else:
		pass
	box.itemconfigure(bm_tableau_id[ida], text=id)
	box.itemconfigure(bm_tableau_code[ida], text=code)
	box.itemconfigure(bm_tableau_place[ida], text=place)
	box.itemconfigure(bm_tableau_date[ida], text=date)
	box.itemconfigure(bm_tableau_del[ida], text=supp)
	try:
		box.unbind("<ButtonRelease-1>", bm_tableau_dela[ida])
	except:
		print("un bug a eu lieu avec unbind can't delete tcl command ( badgesmanagement.py )")
	bm_tableau_dela[ida] = box.tag_bind(bm_tableau_del[ida], '<ButtonRelease-1>', lambda event, box=box, code=code, id=id: bm_delClick(box, code, id))

def bm_createtableau(box, x, y):
	bm_page_select = get_checking_var('bm_page_select')
	a = 15*bm_page_select 
	b = 15*(bm_page_select+1)
	while a<b:
		if a<get_autorized_badges('size', 1):
			if a%2==0:
				bm_createline(box, x, y+20*(a+1), 1, a, get_autorized_badges('code', a), get_autorized_badges('place', a), get_autorized_badges('dateheure', a), "X")
			else:
				bm_createline(box, x, y+20*(a+1), 2, a, get_autorized_badges('code', a), get_autorized_badges('place', a), get_autorized_badges('dateheure', a), "X")
		else:
			if a%2==0:
				bm_createline(box, x, y+20*(a+1), 1, a, "", "", "", "")
			else:
				bm_createline(box, x, y+20*(a+1), 2, a, "", "", "", "")
		a += 1

def bm_updatedatatableau(box, nbbadges):
	bm_page_select = get_checking_var('bm_page_select')
	a = 15*bm_page_select 
	b = 15*(bm_page_select+1)
	while a<b:
		if a<get_autorized_badges('size', 1):
			if a%2==0:
				bm_updateline(box, 1, a, get_autorized_badges('code', a), get_autorized_badges('place', a), get_autorized_badges('dateheure', a), "X")
			else:
				bm_updateline(box, 2, a, get_autorized_badges('code', a), get_autorized_badges('place', a), get_autorized_badges('dateheure', a), "X")
		else:
			if a%2==0:
				bm_updateline(box, 1, a, "", "", "", "")
			else:
				bm_updateline(box, 2, a, "", "", "", "")
		a += 1

def bm_updatetableau(box):
	if box.winfo_width()>640:
		a = 0
		while a<len(bm_tableau_rectangle):
			box.coords(bm_tableau_rectangle[a], bm_tableau_posx, bm_tableau_posy+20*a, box.winfo_width()-bm_tableau_posx*2, bm_tableau_posy+20*a+20)
			box.coords(bm_tableau_id[a], bm_tableau_posx+5, bm_tableau_posy+20*a+10)
			box.coords(bm_tableau_code[a], box.winfo_width()*0.25, bm_tableau_posy+20*a+10)
			box.coords(bm_tableau_place[a], box.winfo_width()*0.5, bm_tableau_posy+20*a+10)
			box.coords(bm_tableau_date[a], box.winfo_width()*0.75, bm_tableau_posy+20*a+10)
			box.coords(bm_tableau_del[a], box.winfo_width()-50, bm_tableau_posy+20*a+10)
			a += 1


def bm_delClick(box, code, id):
	del_autorized_badges(code, id)
	set_checking_var("bm_notific", "Le code "+str(code)+" a été supprimé.")

def bm_createpagination(box, id, x, y, text):	
	bm_pagination_rectangle.append(box.create_rectangle(x, y, x+30, y+26, fill='#2ecc71', width=0))
	bm_pagination_text.append(box.create_text(x+15, y+13, text=text, fill="#ecf0f1", font="Arial 20"))
	bm_pagination_rect.append(box.create_rectangle(x, y, x+30, y+25, width=0))

	box.tag_bind(bm_pagination_rect[id], '<Enter>', lambda event, box=box, id=id: bm_paginationOver(box, id)) 
	box.tag_bind(bm_pagination_rect[id], '<Leave>', lambda event, box=box, id=id: bm_paginationOutOver(box, id)) 
	box.tag_bind(bm_pagination_rect[id], '<ButtonRelease-1>', lambda event, box=box, id=id: bm_paginationClick(box, id))

def bm_paginationOver(box, id):
	box.itemconfigure(bm_pagination_rectangle[id], fill='#27ae60')

def bm_paginationOutOver(box, id):
	box.itemconfigure(bm_pagination_rectangle[id], fill='#2ecc71')

def bm_paginationClick(box, id):
	if id==0:
		if get_checking_var('bm_page_select')==0 or get_autorized_badges('nbpage', 1)==0:
			pass
		else:
			set_checking_var("bm_page_select", get_checking_var('bm_page_select')-1)
	else:
		if get_checking_var('bm_page_select')+1==get_autorized_badges('nbpage', 1) or get_autorized_badges('nbpage', 1)==0:
			pass
		else:
			set_checking_var("bm_page_select", get_checking_var('bm_page_select')+1)

'''
--------------------------------------------------------------------------------------
update
'''
def bm_update(box, command=1):
	if command==1: # une variable change
		if get_checking_var("seconde") != None:
			if get_checking_var('seconde')!=get_autorized_badges('seconde', 0) or get_checking_var('bm_nb_badges')!=get_autorized_badges('size', 1) or get_checking_var('bm_page_select')!=get_checking_var('bm_page_select_old'): # update de la listbox
				set_checking_var("seconde", get_autorized_badges('seconde', 0))
				a = get_checking_var('bm_nb_badges')
				set_checking_var("bm_nb_badges", get_autorized_badges('size', 1))
				bm_updatedatatableau(box, a)
				bm_notif_update(box)
				set_checking_var("bm_page_select_old", get_checking_var('bm_page_select'))
		else:
			set_checking_var("seconde", get_autorized_badges('seconde', 0))
			set_checking_var("bm_nb_badges", get_autorized_badges('size', 1))
			set_checking_var("bm_page_select", 0)
			set_checking_var("bm_page_select_old", 0)
	elif command==2: # la taille de la fenetre change
		bm_notif_update(box)
		bm_updatetableau(box)
	else:
		pass

'''
--------------------------------------------------------------------------------------
delete
'''
def bm_delete(box):
	a = 0
	while a<len(bm_label):
		bm_label[a].destroy()
		bm_entry[a].destroy()
		a += 1