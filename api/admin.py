from django.contrib import admin
from .models import Patient, Appointment, Address, Contact, Anamnesis

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "status")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "data", "horario", "status")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "logradouro", "cidade", "estado", "cep")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "numero", "is_whatsapp")

@admin.register(Anamnesis)
class AnamnesisAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "data_atualizacao")
    readonly_fields = ("data_atualizacao",)

