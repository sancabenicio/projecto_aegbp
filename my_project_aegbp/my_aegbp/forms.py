from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.validators import EmailValidator, URLValidator
from .models import Member
from django.utils import timezone
from .nationalities import NATIONALITY_CHOICES
from tinymce.widgets import TinyMCE
import mimetypes
import re
from django.utils.translation import gettext_lazy as _
from .models import (Photo, Video, Event, Document, BlogPost, Comment, VolunteerOpportunity, 
                     Volunteer, ContactMessage, Testimonial, FAQ, Project, Registration, 
                     Donation, Sponsor, UserProfile, Category, Message, PrivacyPolicy, ContactInfo, About,
                     GeneralSettings, SocialMedia)

class CustomEmailValidator(EmailValidator):
    def __call__(self, value):
        super().__call__(value)
        if "spam" in value:
            raise ValidationError(_('Este email não é permitido.'))

class CustomURLValidator(URLValidator):
    def __call__(self, value):
        super().__call__(value)
        if "example" in value:
            raise ValidationError(_('Este URL não é permitido.'))

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('Senha'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Confirmar Senha'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Um utilizador com este email já existe."))
        CustomEmailValidator()(email)
        return email

    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.username = self.cleaned_data['email']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
        except IntegrityError as e:
            raise ValidationError(_("Erro ao criar utilizador: ") + str(e))
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_('Nome de Utilizador'), max_length=63, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Palavra-passe'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nome de Utilizador')}), label=_('Nome de Utilizador'))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Palavra-passe')}), label=_('Palavra-passe'))

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['event', 'image', 'caption']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'event': _('Evento'),
            'image': _('Imagem'),
            'caption': _('Legenda'),
        }

    def clean_caption(self):
        caption = self.cleaned_data.get('caption')
        if "proibido" in caption:
            raise ValidationError(_('Esta legenda contém palavras proibidas.'))
        return caption

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file', 'link', 'event']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': _('Título'),
            'description': _('Descrição'),
            'file': _('Ficheiro'),
            'link': _('Link'),
            'event': _('Evento'),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        max_size_mb = 100  
        
        if file:
            file_size_mb = file.size / (1024 * 1024)  
            if file_size_mb > max_size_mb:
                raise ValidationError(_('O tamanho do vídeo não pode exceder {} MB.').format(max_size_mb))
        
        return file

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        link = cleaned_data.get('link')

        if not file and not link:
            raise ValidationError(_('Você deve fornecer um ficheiro de vídeo ou um link.'))

        if file:
            mime_type, encoding = mimetypes.guess_type(file.name)
            valid_mime_types = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska']
            if mime_type not in valid_mime_types:
                raise ValidationError(_('Formato de vídeo não suportado. Por favor, envie um arquivo de vídeo nos formatos: .mp4, .mov, .avi, .mkv.'))

        if link:
            CustomURLValidator()(link)
        
        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'description', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        labels = {
            'name': _('Nome'),
            'date': _('Data'),
            'description': _('Descrição'),
            'start_time': _('Hora de Início'),
            'end_time': _('Hora de Término'),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time < start_time:
            raise ValidationError(_('A hora de término não pode ser anterior à hora de início.'))

        return cleaned_data

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'title': _('Título'),
            'file': _('Ficheiro'),
            'description': _('Descrição'),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        max_size_mb = 5  
        
        if file:
            file_size_mb = file.size / (1024 * 1024)  
            if file_size_mb > max_size_mb:
                raise ValidationError(_('O tamanho do arquivo não pode exceder {} MB.').format(max_size_mb))
        
        return file

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise ValidationError(_('A descrição deve ter pelo menos 10 caracteres.'))
        return description


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'title': _('Título'),
            'content': _('Conteúdo'),
            'author': _('Autor'),
            'image': _('Imagem'),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError(_('O título deve ter pelo menos 5 caracteres.'))
        return title
    
    def clean_author(self):
        author = self.cleaned_data.get('author')
        if not author:
            raise forms.ValidationError(_("O campo Autor é obrigatório."))
        return author

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'author', 'content']
        widgets = {
            'post': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'post': _('Postagem'),
            'author': _('Autor'),
            'content': _('Conteúdo'),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise ValidationError(_('O conteúdo deve ter pelo menos 5 caracteres.'))
        return content

class VolunteerOpportunityForm(forms.ModelForm):
    class Meta:
        model = VolunteerOpportunity
        fields = ['title', 'description', 'location', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': _('Título'),
            'description': _('Descrição'),
            'location': _('Localização'),
            'date': _('Data'),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise ValidationError(_('A descrição deve ter pelo menos 10 caracteres.'))
        return description

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Nome'),
            'email': _('Email'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        CustomEmailValidator()(email)
        return email

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': _('Nome'),
            'email': _('Email'),
            'subject': _('Assunto'),
            'message': _('Mensagem'),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise ValidationError(_('A mensagem deve ter pelo menos 10 caracteres.'))
        return message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'content': _('Mensagem'),
        }


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['address', 'phone1', 'phone2', 'email1', 'email2', 'days_of_week', 'hours']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: A108 Adam Street')}),
            'phone1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: +1 5589 55488 55')}),
            'phone2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: +1 6678 254445 41')}),
            'email1': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Ex: info@example.com')}),
            'email2': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Ex: contact@example.com')}),
            'days_of_week': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: Segunda - Sexta')}),
            'hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ex: 09:00 - 17:00')}),
        }
        labels = {
            'address': _('Endereço'),
            'phone1': _('Telefone 1'),
            'phone2': _('Telefone 2'),
            'email1': _('Email 1'),
            'email2': _('Email 2'),
            'days_of_week': _('Dias da Semana'),
            'hours': _('Horário'),
        }

    
    
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': _('Nome'),
            'content': _('Conteúdo'),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise ValidationError(_('O conteúdo deve ter pelo menos 10 caracteres.'))
        return content

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'question': _('Pergunta'),
            'answer': _('Resposta'),
            'category': _('Categoria'),
        }

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if len(answer) < 5:
            raise ValidationError(_('A resposta deve ter pelo menos 5 caracteres.'))
        return answer

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Nome da Categoria'),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'start_date', 'end_date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'title': _('Título'),
            'start_date': _('Data de Início'),
            'end_date': _('Data de Término'),
            'description': _('Descrição'),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError(_('A data de término não pode ser anterior à data de início.'))

        return cleaned_data

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Nome'),
            'email': _('Email'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        CustomEmailValidator()(email)
        return email

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'amount', 'date', 'description', 'proof']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proof': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Nome'),
            'amount': _('Quantia'),
            'date': _('Data'),
            'description': _('Descrição'),
            'proof': _('Comprovativo de Doação'),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise ValidationError(_('A descrição deve ter pelo menos 10 caracteres.'))
        return description


class GeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = ['iban', 'mb_way_number']
        widgets = {
            'iban': forms.TextInput(attrs={'class': 'form-control'}),
            'mb_way_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'iban': _('IBAN'),
            'mb_way_number': _('Número de MB Way'),
        }

    def clean_mb_way_number(self):
        mb_way_number = self.cleaned_data.get('mb_way_number')

        # Regex para validar números de telemóvel no formato esperado (exemplo para Portugal: começa com 9 e tem 9 dígitos)
        if not re.match(r'^9\d{8}$', mb_way_number):
            raise ValidationError(_("Número de MB Way inválido. Deve ser um número de telemóvel válido."))
        
        return mb_way_number


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['name', 'logo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': _('Nome'),
            'logo': _('Logo'),
            'description': _('Descrição'),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise ValidationError(_('A descrição deve ter pelo menos 10 caracteres.'))
        return description

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), required=False, label=_("Senha antiga"))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), required=False, label=_("Nova senha"))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'city', 'state', 'zip_code', 'description']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'profile_picture': _('Foto de Perfil'),
            'address': _('Endereço'),
            'city': _('Cidade'),
            'state': _('Estado'),
            'zip_code': _('Código Postal'),
            'description': _('Descrição'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        self.user = user
        self.fields['old_password'].initial = ''  # Garante que o campo "Senha antiga" esteja vazio

    def clean_email(self):
        return self.user.email  # Retornar o email atual para garantir que ele não seja alterado

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')

        if new_password:
            if not old_password:
                self.add_error('old_password', _('Este campo é obrigatório.'))
            elif not self.user.check_password(old_password):
                self.add_error('old_password', _('Senha antiga incorreta.'))

        return cleaned_data

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = self.user
        if self.cleaned_data['first_name']:
            user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
            user_profile.save()
        return user_profile

class MemberForm(forms.ModelForm):
    other_gender = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Especifique o gênero')}), label=_('Outro Gênero'))
    prefer_not_to_say = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label=_('Prefiro não dizer'))
    nationality = forms.ChoiceField(choices=NATIONALITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label=_('Nacionalidade'))

    class Meta:
        model = Member
        fields = [
            'full_name', 'birth_date', 'document_number', 'document_type', 'document_validity', 
            'nationality', 'gender', 'other_gender', 'prefer_not_to_say', 'address', 'postal_code', 'city', 
            'phone', 'email', 'is_student', 'school', 'education_type', 'course', 'academic_year', 
            'is_scholar', 'is_working_student', 'occupation'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'document_validity': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.RadioSelect(choices=[('M', _('Masculino')), ('F', _('Feminino')), ('O', _('Outro')), ('N', _('Prefiro não dizer'))]),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_student': forms.RadioSelect(choices=[(True, _('Sim')), (False, _('Não'))]),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'education_type': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_scholar': forms.RadioSelect(choices=[(True, _('Sim')), (False, _('Não'))]),
            'is_working_student': forms.RadioSelect(choices=[(True, _('Sim')), (False, _('Não'))]),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': _('Nome Completo'),
            'birth_date': _('Data de Nascimento'),
            'document_number': _('Número do Documento'),
            'document_type': _('Tipo de Documento'),
            'document_validity': _('Validade do Documento'),
            'nationality': _('Nacionalidade'),
            'gender': _('Gênero'),
            'other_gender': _('Outro Gênero'),
            'prefer_not_to_say': _('Prefiro não dizer'),
            'address': _('Endereço'),
            'postal_code': _('Código Postal'),
            'city': _('Cidade'),
            'phone': _('Telemóvel'),
            'email': _('Email'),
            'is_student': _('Estudante?'),
            'school': _('Escola/Faculdade'),
            'education_type': _('Tipo de Ensino'),
            'course': _('Curso'),
            'academic_year': _('Ano Curricular'),
            'is_scholar': _('Bolseiro(a)?'),
            'is_working_student': _('Estudante Trabalhador?'),
            'occupation': _('Caso não seja estudante, por favor, indique a ocupação atual'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Member.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Este email já está em uso.'))
        CustomEmailValidator()(email)
        return email

    def clean_document_number(self):
        document_number = self.cleaned_data.get('document_number')
        if Member.objects.filter(document_number=document_number).exists():
            raise forms.ValidationError(_('Este número de documento já está em uso.'))
        return document_number

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise forms.ValidationError(_('A data de nascimento não pode ser no futuro.'))
        age = (timezone.now().date() - birth_date).days // 365
        if age < 14:
            raise forms.ValidationError(_('A idade do membro deve ser de pelo menos 14 anos.'))
        return birth_date

    def clean_academic_year(self):
        academic_year = self.cleaned_data.get('academic_year')
        if academic_year and academic_year < 1:
            raise forms.ValidationError(_('O ano curricular deve ser maior que zero.'))
        return academic_year

    def clean(self):
        cleaned_data = super().clean()
        gender = cleaned_data.get('gender')
        other_gender = cleaned_data.get('other_gender')
        if gender == 'O' and not other_gender:
            self.add_error('other_gender', _('Por favor, especifique o gênero.'))
        return cleaned_data

    def save(self, commit=True):
        try:
            member = super().save(commit=False)
            if commit:
                member.save()
        except IntegrityError as e:
            raise ValidationError(_("Erro ao salvar membro: ") + str(e))
        return member

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contact', 'sender', 'content']
        widgets = {
            'contact': forms.HiddenInput(),
            'sender': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'sender': _('Remetente'),
            'content': _('Conteúdo'),
        }

class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicy
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        
class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk and About.objects.exists():
            raise forms.ValidationError(_("Apenas uma seção 'Sobre' é permitida."))
        return cleaned_data
    

class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['platform', 'profile_name', 'url']
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'profile_name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }
