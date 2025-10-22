from rest_framework import serializers
from .models import Patient, Appointment, Address, Contact, Anamnesis


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado']


class ContactSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'tipo', 'tipo_display', 'numero', 'is_whatsapp', 'observacao']


class AnamnesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anamnesis
        fields = [
            'id', 'paciente', 'data_atualizacao',
            'problemas_saude', 'medicamentos', 'alergias', 'cirurgias',
            'ultima_consulta_dentista', 'motivo_ultima_consulta', 'experiencia_tratamento',
            'fumante', 'alcool', 'frequencia_escovacao', 'usa_fio_dental',
            'sensibilidade_dental', 'sangramento_gengival', 'ranger_dentes', 'dores_articulacao',
            'gestante', 'diabetes', 'hipertensao', 'problemas_cardiacos',
            'observacoes'
        ]


class PatientSerializer(serializers.ModelSerializer):
    endereco = AddressSerializer(required=False, allow_null=True)
    contatos = ContactSerializer(many=True, read_only=True)
    anamnese = AnamnesisSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'nome', 'cpf', 'rg', 'data_nascimento', 'sexo',
            'email', 'contatos', 'endereco', 'status', 'data_cadastro',
            'anamnese'
        ]

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        endereco = None
        if endereco_data:
            endereco = Address.objects.create(**endereco_data)
        patient = Patient.objects.create(endereco=endereco, **validated_data)
        return patient

    def update(self, instance, validated_data):
        endereco_data = validated_data.pop('endereco', None)
        if endereco_data:
            endereco = instance.endereco
            if endereco is None:
                endereco = Address.objects.create(**endereco_data)
                instance.endereco = endereco
            else:
                for attr, value in endereco_data.items():
                    setattr(endereco, attr, value)
                endereco.save()
        return super().update(instance, validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'paciente', 'paciente_nome', 'data', 'horario', 
                 'tipo', 'status', 'observacoes', 'duracao']
