from rest_framework import viewsets, filters, status
from .models import Patient, Appointment, Address, Contact, Anamnesis
from .serializers import (
    PatientSerializer, AppointmentSerializer,
    AddressSerializer, ContactSerializer, AnamnesisSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone

# Authentication helpers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({'user': {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name}})
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['logradouro', 'bairro', 'cidade']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        paciente_id = self.request.query_params.get('paciente')
        if paciente_id:
            qs = qs.filter(pacientes=paciente_id)
        return qs


class AnamnesisViewSet(viewsets.ModelViewSet):
    queryset = Anamnesis.objects.all()
    serializer_class = AnamnesisSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        paciente_id = self.request.query_params.get('paciente')
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        return qs


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('nome')
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email', 'cpf']

    @action(detail=True, methods=['post'])
    def add_contact(self, request, pk=None):
        patient = self.get_object()
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            patient.contatos.add(contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        """Create an Address and assign it to the patient's endereco field."""
        patient = self.get_object()
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.save()
            patient.endereco = address
            patient.save()
            return Response(AddressSerializer(address).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        patient = self.get_object()
        contacts = patient.contatos.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def anamnesis(self, request, pk=None):
        patient = self.get_object()
        try:
            anamnesis = patient.anamnese
            serializer = AnamnesisSerializer(anamnesis)
            return Response(serializer.data)
        except Anamnesis.DoesNotExist:
            return Response({'detail': 'Anamnese não encontrada'}, status=status.HTTP_404_NOT_FOUND)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by("data", "horario")
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        data = self.request.query_params.get("data")
        status = self.request.query_params.get("status")
        busca = self.request.query_params.get("busca")
        if data:
            qs = qs.filter(data=data)
        if status:
            qs = qs.filter(status=status)
        if busca:
            qs = qs.filter(Q(paciente__nome__icontains=busca) | Q(tipo__icontains=busca))
        return qs

    @action(detail=False, methods=["get"])
    def proximas(self, request):
        today = request.query_params.get("data")
        qs = self.get_queryset()
        if today:
            qs = qs.filter(data=today)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def detalhes(self, request, pk=None):
        agendamento = self.get_object()
        paciente = agendamento.paciente

        # Dados do paciente
        dados_paciente = {
            'id': paciente.id,
            'nome': paciente.nome,
            'cpf': paciente.cpf,
            'data_nascimento': paciente.data_nascimento,
            'sexo': paciente.get_sexo_display() if paciente.sexo else None,
            'email': paciente.email,
            'contatos': ContactSerializer(paciente.contatos.all(), many=True).data
        }

        # Dados relevantes da anamnese
        try:
            anamnese = paciente.anamnese
            dados_anamnese = {
                'alergias': anamnese.alergias,
                'medicamentos': anamnese.medicamentos,
                'problemas_saude': anamnese.problemas_saude,
                'diabetes': anamnese.diabetes,
                'hipertensao': anamnese.hipertensao,
                'problemas_cardiacos': anamnese.problemas_cardiacos,
                'gestante': anamnese.gestante
            }
        except Anamnesis.DoesNotExist:
            dados_anamnese = None

        # Dados do agendamento
        dados_agendamento = {
            'id': agendamento.id,
            'data': agendamento.data,
            'horario': agendamento.horario,
            'tipo': agendamento.tipo,
            'status': agendamento.status,
            'status_display': dict(agendamento.STATUS_CHOICES).get(agendamento.status, agendamento.status),
            'duracao': agendamento.duracao,
            'observacoes': agendamento.observacoes
        }

        data = {
            'agendamento': dados_agendamento,
            'paciente': dados_paciente,
            'anamnese': dados_anamnese
        }

        return Response(data)

    @action(detail=True, methods=['patch'], url_path='update_status')
    def update_status(self, request, pk=None):
        """Update only the status field of an appointment (partial update).

        Expects JSON: {"status": "confirmado"}
        """
        agendamento = self.get_object()
        new_status = request.data.get('status')
        if new_status is None:
            return Response({'detail': 'Campo "status" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate against defined choices
        valid_choices = {choice[0] for choice in agendamento.STATUS_CHOICES}
        if new_status not in valid_choices:
            return Response({'detail': f'Status inválido. Valores válidos: {sorted(valid_choices)}'}, status=status.HTTP_400_BAD_REQUEST)

        agendamento.status = new_status
        agendamento.save()
        serializer = self.get_serializer(agendamento)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='totais-diarios')
    def totais_diarios(self, request):
        """Return daily totals:
        - total_agendamentos_no_dia
        - total_pacientes
        - total_pendentes_no_dia

        Optional query param: ?data=YYYY-MM-DD (defaults to today)
        """
        data_str = request.query_params.get('data')
        if data_str:
            try:
                day = timezone.datetime.fromisoformat(data_str).date()
            except Exception:
                return Response({'detail': 'Formato de data inválido. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            day = timezone.localdate()

        # total appointments on the day
        total_agendamentos = Appointment.objects.filter(data=day).count()

        # total patients in the system
        total_pacientes = Patient.objects.count()

        # pending appointments (status equals 'agendado' or other pending statuses) on the day
        pending_statuses = ['agendado', 'confirmado']
        total_pendentes = Appointment.objects.filter(data=day, status__in=pending_statuses).count()

        return Response({
            'data': str(day),
            'total_agendamentos_no_dia': total_agendamentos,
            'total_pacientes': total_pacientes,
            'total_pendentes_no_dia': total_pendentes,
        })
