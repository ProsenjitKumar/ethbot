# from django.shortcuts import render, redirect
# from .admin import EmailLoginForm, PhoneNumberForm
#
#
# def EmailView(request):
#     form = EmailLoginForm(request.POST or None)
#
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         form.save()
#
#         return redirect('/phone/')
#
#     return render(request, 'index2.html', context)
#
#
# def PhoneNumberView(request):
#     form = PhoneNumberForm(request.POST or None)
#
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         form.save()
#         return render(request, 'thanks.html')
#     return render(request, 'index.html', context)
#
#
#
#
